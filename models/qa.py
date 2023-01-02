from .extension import db
from datetime import datetime, date


# 问题模型
class QuestionModel(db.Model):
    __tablename__ = "question"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False, comment="问题标题")
    content = db.Column(db.Text, nullable=False, comment="问题描述")
    create_time = db.Column(db.Date, default=date.today, comment="问题创建时间")

    author_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), comment="提问者")
    # 按从大到小排序
    answers = db.relationship('AnswerModel', backref=db.backref('question', order_by=create_time.desc()))


# 回答模型
class AnswerModel(db.Model):
    __tablename__ = "answer"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False, comment="回答内容")
    create_time = db.Column(db.Date, default=date.today(), comment="回答创建时间")

    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
