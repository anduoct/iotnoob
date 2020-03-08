from flask import request, jsonify, url_for, g, current_app
from app.api import bp
from app.api.auth import token_auth
from app.api.errors import error_response, bad_request
from app.extensions import db
from app.models import Blog

@bp.route('/blogs', methods=['POST'])
@token_auth.login_required
def create_blog():
    # 创建博客
    data = request.get_json()
    if not data:
        return bad_request('Must post JSON data.')
    message = {}
    if 'title' not in data or not data.get('title'):
        message['title'] = 'Title is required.'
    elif len(data.get('title')) > 255:
        message['title'] = 'Title must less than 255 characters.'
    if 'content' not in data or not data.get('content'):
        message['content'] = 'Content is required.'
    if message:
        return bad_request(message)

    blog = Blog()
    blog.from_dict(data)
    blog.author = g.current_user  # 通过 auth.py 中 verify_token() 传递过来的（同一个request中，需要先进行 Token 认证）
    db.session.add(blog)
    db.session.commit()
    response = jsonify(blog.to_dict())
    response.status_code = 201
    # HTTP协议要求201响应包含一个值为新资源URL的Location头部
    response.headers['Location'] = url_for('api.get_blog', id=blog.id)
    return response


@bp.route('/blogs/', methods=['GET'])
def get_blogs():
    # 返回文章集合
    page = request.args.get('page', 1, type=int)
    per_page = min(
        request.args.get(
            'per_page', current_app.config['BLOGS_PER_PAGE'], type=int), 100)
    data = Blog.to_collection_dict(
        Blog.query.order_by(Blog.timestamp.desc()), page, per_page,
        'api.get_blogs')
    return jsonify(data)

@bp.route('/blogs/<int:id>', methods=['GET'])
def get_blog(id):
    # 返回一篇文章
    blog = Blog.query.get_or_404(id)
    blog.views += 1
    db.session.add(blog)
    db.session.commit()
    return jsonify(blog.to_dict())

@bp.route('/blogs/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_blog(id):
    # 修改一篇文章
    blog = Blog.query.get_or_404(id)
    if g.current_user != blog.author:
        return error_response(403)

    data = request.get_json()
    if not data:
        return bad_request('must post JSON data.')
    message = {}
    if 'title' not in data or not data.get('title'):
        message['title'] = 'Title is required.'
    elif len(data.get('title')) > 255:
        message['title'] = 'Title must less than 255 characters.'
    if 'content' not in data or not data.get('content'):
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
    db.session.commit()
    return '', 204