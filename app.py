from flask import Flask
from flask_cors import CORS
from flasgger import Swagger
from pymongo import MongoClient
from config import Config
from flask_cors import CORS
import config
import os

from neruko.controllers.focuslink_controller import focuslink_bp
from neruko.controllers.videowatch_controller import videowatch_bp
from public.controllers.iplogs_controller import iplogs_bp
from neruko.controllers.showtimetable_controller import showlogs_bp

app = Flask(__name__)
CORS(app)  # 允许所有来源访问

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
app.register_blueprint(focuslink_bp)
app.register_blueprint(videowatch_bp)
app.register_blueprint(iplogs_bp)
app.register_blueprint(showlogs_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
