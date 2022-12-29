# 用户模块相关蓝图

from flask import Blueprint, request, render_template, flash, redirect, url_for, jsonify
from models.extension import db
from .user_form import LoginForm, RegisterForm
from models.user import UserModel, EmailCaptchaModel
from werkzeug.security import generate_password_hash, check_password_hash
from .extension import mail
from flask_mail import Message
import random
import string
from datetime import datetime

user_bp = Blueprint("user_blueprint", __name__, url_prefix="/user")


@user_bp.route('/login/', methods=['GET', 'POST'])
def login():
    """
    用户登录
    :return:
    """
    if request.method == 'GET':
        # 如果是GET请求，直接渲染login.html模板
        return render_template('user/login.html')
    else:
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            user_model = UserModel.query.filter_by(email=email).first()

            # 验证用户信息是否已存在数据库中，并将表单获取的密码与数据库中的密码进行比对
            if user_model and check_password_hash(user_model.password,password):
                return redirect("/")
            else:
                flash("密码输入错误！")
                return redirect(url_for("user_blueprint.login"))
        else:
            flash("邮箱或密码输入错误")
            return redirect(url_for("user_blueprint.login"))


@user_bp.route('/register/', methods=['GET', 'POST'])
def register():
    """
    用户注册
    :return:
    """
    if request.method == 'GET':
        return render_template("user/register.html")
    else:
        form = RegisterForm(request.form)
        if form.validate():
            email = form.email.data
            username = form.username.data
            # 密码加密
            hash_password = generate_password_hash(form.password1.data)

            # 将表单内容存入数据库
            user_model = UserModel(email=email, username=username, password=hash_password)
            db.session.add(user_model)
            db.session.commit()

            return redirect(url_for("user_blueprint.login"))
        else:
            return redirect(url_for("user_blueprint.register"))


@user_bp.route('/captcha/', methods=['POST'])
def get_captcha():
    """
    从用户注册视图中获取邮箱地址，向该邮箱发送验证码
    :return:
    """
    email = request.form.get('email')
    if email:
        # 生成长度为6包含大小写字母和数字的验证码
        captcha = "".join(random.choices(string.ascii_letters+string.digits, k=6))

        # 构建邮件消息体
        message = Message(
            subject="验证码",
            recipients=[email],
            body=f"{captcha}"
        )
        # 发送邮件
        mail.send(message)

        # 将验证码存入数据库，并判断数据库中是否已有该邮箱对应的验证码，如果有，更新
        captcha_model = EmailCaptchaModel.query.filter_by(email=email).first()
        if captcha_model:
            captcha_model.captcha = captcha
            captcha_model.create_time = datetime.now()
            db.session.commit()
        else:
            captcha_model = EmailCaptchaModel(email=email, captcha=captcha)
            db.session.add(captcha_model)
            db.session.commit()

        return jsonify({
            "code": 200
        })
    else:
        return jsonify({
            "code": 400,
            "message": "请先传递邮箱"
        })

