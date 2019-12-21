import re
from flask import request, jsonify, url_for
from app import db
from app.api import bp
from app.api.errors import bad_request
from app.models import User
from app.api.auth import token_auth

@bp.route('/users', methods=['POST'])
def create_user():
    # register a new user
    data = request.get_json()
    if not data:
        return bad_request('must post JSON data.')

    message = {}
    if 'username' not in data or not data.get('username', None):
        message['username'] = 'wrong username.'
    pattern = '^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$'
    if 'email' not in data or not re.match(pattern, data.get('email', None)):
        message['email'] = 'Please provide a valid email address.'
    if 'password' not in data or not data.get('password', None):
        message['password'] = 'Please provide a valid password.'

    if User.query.filter_by(username=data.get('username', None)).first():
        message['username'] = 'Please use a different username.'
    if User.query.filter_by(email=data.get('email', None)).first():
        message['email'] = 'Please use a different email address.'
    if message:
        return bad_request(message)

    user = User()
    user.from_dict(data, new_user=True)
    db.session.add(user)
    db.session.commit()
    response = jsonify(user.to_dict())
    response.status_code = 201
    # HTTP协议要求201响应包含一个值为新资源URL的Location头部
    response.headers['Location'] = url_for('api.get_user', id=user.id)
    return response

@bp.route('/users', methods=['GET'])
@token_auth.login_required
def get_users():
    # return all users' unit, divide page
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = User.to_collection_dict(User.query, page, per_page, 'api.get_users')
    return jsonify(data)

@bp.route('/users/<int:id>', methods=['GET'])
@token_auth.login_required
def get_user(id):
    # return a user
    return jsonify(User.query.get_or_404(id).to_dict())

@bp.route('/users/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_user(id):
    # update a user
    user =User.query.get_or_404(id)
    data = request.get_json()
    if not data:
        return bad_request('must post JSON data.')

    message = {}
    if 'username' not in data or not data.get('username', None):
        message['username'] = 'wrong username.'
    pattern = '^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$'
    if 'email' not in data or not re.match(pattern, data.get('email', None)):
        message['email'] = 'Please provide a valid email address.'

    if 'username' in data and data['username'] != user.username and \
         User.query.filter_by(username=data['username']).first():
        message['username'] = 'Please use a different username.'
    if 'email' in data and data['email'] != user.email and \
        User.query.filter_by(email=data['email']).first():
        message['email'] = 'Please use a different email address.'
   
    if message:
        return bad_request(message)

    user.from_dict(data, new_user=False)
    db.session.commit()
    return jsonify(user.to_dict())

@bp.route('/users', methods=['DELETE'])
@token_auth.login_required
def delete_user():
    # delete a user
    pass
