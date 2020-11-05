from flask import Flask
from app.api import api
from app.views import views
from conf.settings import TEMPLATE_DIR, STATIC_DIR


def create_app():
    # 创建 Flask app 实例
    app = Flask(__name__, template_folder=TEMPLATE_DIR,
                static_folder=STATIC_DIR)
    # 注册蓝图
    app.register_blueprint(views)
    app.register_blueprint(api, url_prefix='/api')
    # 配置config
    # app.config.from_object(Config)
    # 绑定数据库
    # db.init_app(app)
    # 声明运行环境为开发环境
    app.env = 'development'
    # 开启调试模式
    app.debug = True

    return app
