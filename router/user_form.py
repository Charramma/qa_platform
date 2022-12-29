# 用户模块表单类

import wtforms
from wtforms.validators import length, email, EqualTo
from models.user import EmailCaptchaModel, UserModel


# 注册表单类
class RegisterForm(wtforms.Form):
    username = wtforms.StringField(validators=[length(min=4, max=20)])
    email = wtforms.StringField(validators=[email()])
    password1 = wtforms.StringField(validators=[length(min=8, max=16)])
    password2 = wtforms.StringField(validators=[EqualTo("password1")])
    captcha = wtforms.StringField(validators=[length(min=6, max=6)])

    def validate_captcha(self, field):
        """
        验证表单中获取的验证码是否与数据库中的一致
        :param field:
        :return:
        """
        captcha = field.data
        email = self.email.data
        captcha_model = EmailCaptchaModel.query.filter_by(email=email).first()
        if not captcha_model or captcha_model.captcha.lower() != captcha.lower():
            raise wtforms.ValidationError("Unknow captcha!")

    def validate_email(self, field):
        """
        判断数据的邮箱是否已存在于数据库
        :param field:
        :return:
        """
        email_field = field.data
        user_model = UserModel.query.filter_by(email=email_field).first()
        if user_model:
            raise wtforms.ValidationError("This email is used!")


# 登录表单类
class LoginForm(wtforms.Form):
    email = wtforms.StringField(validators=[email()])
    password = wtforms.StringField(validators=[length(min=8, max=16)])

    def validate_email(self, field):
        """
        对邮箱字段进行验证，判断表单输入的邮箱是否已存在数据库中
        :param field:
        :return:
        """
        email_field = field.data
        user_model = UserModel.query.filter_by(email=email_field).first()
        if not user_model:
            raise wtforms.ValidationError('该邮箱未注册！')