# 用户模块表单类

import wtforms
from wtforms.validators import length, email, EqualTo
from models.user import EmailCaptchaModel, UserModel


# 注册表单类
class RegisterForm(wtforms.Form):
    pass


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