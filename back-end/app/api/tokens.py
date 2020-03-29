from flask import jsonify, g
from app.extensions import db
from app.api import bp
from app.api.auth import basic_auth


@bp.route('/tokens', methods=['POST'])
@basic_auth.login_required
def get_token():
    token = g.current_user.get_jwt()
    # once get JWT successfully, update last_seen
    g.current_user.ping()
    db.session.commit()
    return jsonify({'token': token})