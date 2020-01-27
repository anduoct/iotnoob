from flask import jsonify
from app.api import bp

@bp.route('/ping', methods = ['GET'])

def ping():
    # test connection between front-end and back-end
    return jsonify('Pong!')