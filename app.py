from flask import Flask


def create_app(config=None):
    app = Flask(__name__)

    # 导入配置文件
    app.config.from_object('config.settings')
    app.config.from_object('config.secure')

    return app