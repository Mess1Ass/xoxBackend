from flask import Flask
from flask_cors import CORS
from flasgger import Swagger
from pymongo import MongoClient
from config import Config
import config
import os

# from controllers.login_controller import login_blueprint
# from controllers.shop_controller import shop_bp
# from controllers.file_controller import file_bp

app = Flask(__name__)


# 初始化 Swagger 文档
swagger = Swagger(app)

# 初始化 MongoDB 客户端
client = MongoClient(config.MONGO_URI)
db = client[config.MONGO_DB]

# 可选：把 db 存入 Flask 的全局上下文s
app.config["MONGO_CLIENT"] = client
app.config["MONGO_DB"] = db

app.config.from_object(Config)
app.config["UPLOAD_FOLDER"] = os.path.join(app.root_path, Config.UPLOAD_FOLDER_NAME)

# 注册接口蓝图
# app.register_blueprint(login_blueprint)
# app.register_blueprint(file_bp)
# app.register_blueprint(shop_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
