from flask import jsonify
from app.api import bp


@bp.route('/ping', methods=['GET'])
def ping():
    # test connection between front-end and back-end
    return jsonify('Pong!')


@bp.route('/test-email', methods=['GET'])
def test_email():
    from flask import current_app
    from app.utils.email import send_email
    send_email('[Madblog] Test Email',
               sender=current_app.config['MAIL_SENDER'],
               recipients=['910359910@qq.com'],
               text_body='text body',
               html_body='<h1>HTML body</h1>')
    return jsonify('Send Email OK!')
