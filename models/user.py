### 用户模块相关ORM

from .extension import db
from datetime import datetime, date


# 验证码模型
class EmailCaptchaModel(db.Model):
    __tablename__ = "email_captcha"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False, unique=True, comment='邮箱')
    captcha = db.Column(db.String(10), nullable=False, comment='验证码')
    create_time = db.Column(db.DateTime, default=datetime.now, comment='验证码创建时间')


# 用户模型
class UserModel(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False, unique=True, comment='邮箱')
    username = db.Column(db.String(50), nullable=False, unique=True, comment='用户名')
    password = db.Column(db.String(200), nullable=False, comment='密码')
    register_time = db.Column(db.DateTime, default=datetime.now, comment='注册时间')

    questions = db.relationship('QuestionModel', backref='user')
    answers = db.relationship('AnswerModel', backref='user')
