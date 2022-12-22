from flask import Flask
import router
import models


def create_app(config=None):
    app = Flask(__name__)

    # 导入配置文件
    app.config.from_object('config.settings')
    app.config.from_object('config.secure')

    # 初始化数据模型
    models.init_app(app)

    # 初始化蓝图
    router.init_app(app)

    return app
