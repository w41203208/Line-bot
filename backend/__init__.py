from flask import Flask
from flask_cors import CORS
from .views import views


def create_app():
    app = Flask(__name__)
    app.config['DEBUG'] = True
    CORS(app)

    app.register_blueprint(views, url_prefix="/")

    return app
