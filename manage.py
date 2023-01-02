from flask_script import Manager
from app import create_app
from models.user import UserModel
from flask import session, g

app = create_app()
manager = Manager(app)


@app.before_request
def before_request():
    """
    该钩子函数会在请求视图之前执行，用于判定是否登录
    首先从session中取user_id值，如果有值，说明已登录，根据获取到的user_id获取用户信息，并绑定到全局变量user上
    :return:
    """
    user_id = session.get("user_id")
    if user_id:
        try:
            user = UserModel.query.get(user_id)
            setattr(g, "user", user)
        except:
            g.user = None


@app.context_processor
def context_processor():
    """
    将全局变量g.user传入到所有模板文件的上下文中
    :return:
    """
    if hasattr(g, "user"):
        return {"user": g.user}
    else:
        return {}


if __name__ == '__main__':
    manager.run()
