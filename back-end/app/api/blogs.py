from flask import request, jsonify, url_for, g, current_app
from app.api import bp
from app.api.auth import token_auth
from app.api.errors import error_response, bad_request
from app.extensions import db
from app.models import Blog, Comment


@bp.route('/blogs/', methods=['POST'])
@token_auth.login_required
def create_blog():
    # 创建博客
    data = request.get_json()
    if not data:
        return bad_request('You must post JSON data.')
    message = {}
    if 'title' not in data or not data.get('title').strip():
        message['title'] = 'Title is required.'
    elif len(data.get('title')) > 255:
        message['title'] = 'Title must less than 255 characters.'
    if 'content' not in data or not data.get('content').strip():
        message['content'] = 'Content is required.'
    if message:
        return bad_request(message)

    blog = Blog()
    blog.from_dict(data)
    blog.author = g.current_user  # 通过 auth.py 中 verify_token() 传递过来的（同一个request中，需要先进行 Token 认证）
    db.session.add(blog)
    # 给文章作者的所有粉丝发送新文章通知
    for user in blog.author.followers:
        user.add_notification('unread_followeds_blogs_count',
                              user.new_followeds_blogs())
    db.session.commit()
    response = jsonify(blog.to_dict())
    response.status_code = 201
    # HTTP协议要求201响应包含一个值为新资源URL的Location头部
    response.headers['Location'] = url_for('api.get_blog', id=blog.id)
    return response


@bp.route('/blogs/', methods=['GET'])
def get_blogs():
    '''返回文章集合，分页'''
    page = request.args.get('page', 1, type=int)
    per_page = min(
        request.args.get('per_page',
                         current_app.config['BLOGS_PER_PAGE'],
                         type=int), 100)
    data = Blog.to_collection_dict(Blog.query.order_by(Blog.timestamp.desc()),
                                   page, per_page, 'api.get_blogs')
    return jsonify(data)


@bp.route('/blogs/<int:id>', methods=['GET'])
def get_blog(id):
    '''返回一篇文章'''
    blog = Blog.query.get_or_404(id)
    blog.views += 1
    db.session.add(blog)
    db.session.commit()
    data = blog.to_dict()
    # 下一篇文章
    next_basequery = Blog.query.order_by(
        Blog.timestamp.desc()).filter(Blog.timestamp > blog.timestamp)
    if next_basequery.all():
        data['next_id'] = next_basequery[-1].id
        data['next_title'] = next_basequery[-1].title
        data['_links']['next'] = url_for('api.get_blog',
                                         id=next_basequery[-1].id)
    else:
        data['_links']['next'] = None
    # 上一篇文章
    prev_basequery = Blog.query.order_by(
        Blog.timestamp.desc()).filter(Blog.timestamp < blog.timestamp)
    if prev_basequery.first():
        data['prev_id'] = prev_basequery.first().id
        data['prev_title'] = prev_basequery.first().title
        data['_links']['prev'] = url_for('api.get_blog',
                                         id=prev_basequery.first().id)
    else:
        data['_links']['prev'] = None
    return jsonify(data)


@bp.route('/blogs/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_blog(id):
    '''修改一篇文章'''
    blog = Blog.query.get_or_404(id)
    if g.current_user != blog.author:
        return error_response(403)

    data = request.get_json()
    if not data:
        return bad_request('You must post JSON data.')
    message = {}
    if 'title' not in data or not data.get('title').strip():
        message['title'] = 'Title is required.'
    elif len(data.get('title')) > 255:
        message['title'] = 'Title must less than 255 characters.'
    if 'content' not in data or not data.get('content').strip():
        message['content'] = 'Content is required.'
    if message:
        return bad_request(message)

    blog.from_dict(data)
    db.session.commit()
    return jsonify(blog.to_dict())


@bp.route('/blogs/<int:id>', methods=['DELETE'])
@token_auth.login_required
def delete_blog(id):
    # 删除一篇文章
    blog = Blog.query.get_or_404(id)
    if g.current_user != blog.author:
        return error_response(403)
    db.session.delete(blog)
    # 给文章作者的所有粉丝发送新文章通知(需要自动减1)
    for user in blog.author.followers:
        user.add_notification('unread_followeds_blogs_count',
                              user.new_followeds_blogs())
    db.session.commit()
    return '', 204


###
# 与博客文章资源相关的资源
##
@bp.route('/blogs/<int:id>/comments/', methods=['GET'])
def get_blog_comments(id):
    '''返回当前文章下面的一级评论'''
    blog = Blog.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    per_page = min(
        request.args.get('per_page',
                         current_app.config['COMMENTS_PER_PAGE'],
                         type=int), 100)
    # 先获取一级评论
    data = Comment.to_collection_dict(blog.comments.filter(
        Comment.parent == None).order_by(Comment.timestamp.desc()),
                                      page,
                                      per_page,
                                      'api.get_blog_comments',
                                      id=id)
    # 再添加子孙到一级评论的 descendants 属性上
    for item in data['items']:
        comment = Comment.query.get(item['id'])
        descendants = [child.to_dict() for child in comment.get_descendants()]
        # 按 timestamp 排序一个字典列表
        from operator import itemgetter
        item['descendants'] = sorted(descendants, key=itemgetter('timestamp'))
    return jsonify(data)


###
# 文章被喜欢/收藏 或 被取消喜欢/取消收藏
###
@bp.route('/blogs/<int:id>/like', methods=['GET'])
@token_auth.login_required
def like_blog(id):
    '''喜欢文章'''
    blog = Blog.query.get_or_404(id)
    blog.liked_by(g.current_user)
    db.session.add(blog)
    # 切记要先提交，先添加喜欢记录到数据库，因为 new_blogs_likes() 会查询 blogs_likes 关联表
    db.session.commit()
    # 给文章作者发送新喜欢通知
    blog.author.add_notification('unread_blogs_likes_count',
                                 blog.author.new_blogs_likes())
    db.session.commit()
    return jsonify({
        'status': 'success',
        'message': 'You are now liking this blog.'
    })


@bp.route('/blogs/<int:id>/unlike', methods=['GET'])
@token_auth.login_required
def unlike_blog(id):
    '''取消喜欢文章'''
    blog = Blog.query.get_or_404(id)
    blog.unliked_by(g.current_user)
    db.session.add(blog)
    # 切记要先提交，先添加喜欢记录到数据库，因为 new_blogs_likes() 会查询 blogs_likes 关联表
    db.session.commit()
    # 给文章作者发送新喜欢通知(需要自动减1)
    blog.author.add_notification('unread_blogs_likes_count',
                                 blog.author.new_blogs_likes())
    db.session.commit()
    return jsonify({
        'status': 'success',
        'message': 'You are not liking this blog anymore.'
    })
