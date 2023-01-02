from flask_mail import Mail
from flask import g, redirect, url_for
from functools import wraps

mail = Mail()


# 此装饰器用于做权限控制，被此装饰器修饰的方法只有登录后才能访问
def log_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # 检测是否有user这个全局变量
        if hasattr(g, 'user'):
            return func(*args, **kwargs)
        else:
            # 没有就说明没登录，跳转到登录页面
            return redirect(url_for('user_blueprint.login'))
    return wrapper
