from .views import bp
from .user import user_bp
from .extension import mail


def init_app(app):
    app.register_blueprint(bp)
    app.register_blueprint(user_bp)
    mail.init_app(app)
