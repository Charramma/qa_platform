# 用户模块相关蓝图

from flask import Blueprint, request, render_template
from models.extension import db

user_bp = Blueprint("user_blueprint")


@user_bp.route('/login/', methods=['GET', 'POST'])
def login():
    """
    登录视图
    :return:
    """
    if request.method == 'GET':
        # 如果是GET请求，直接渲染login.html模板
        return render_template('user/login.html')
    else:
        pass