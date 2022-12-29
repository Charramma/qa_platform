from flask import Blueprint
from flask_mail import Message
from .extension import mail

bp = Blueprint("demo_blueprint", __name__, url_prefix='/')

@bp.route('/')
def index():
    return "lalala"


@bp.route('/test/')
def mail_send():
    message = Message(
        subject="测试邮件",
        recipients=["1005702087@qq.com"],
        body="""
        这是一个测试邮件
        """
    )
    mail.send(message)
    return '邮件发送成功'
