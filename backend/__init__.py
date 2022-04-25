import os
from flask import Flask
from flask_cors import CORS

def create_app(test_config=None):
    app = Flask(__name__)
    app.config['DEBUG'] = True
    app.config['SECRET_KEY'] = 'JustDemonstrating'
    CORS(app)
    ######## Register Database ########


    from .views import views
    app.register_blueprint(views, url_prefix="/")



    return app
