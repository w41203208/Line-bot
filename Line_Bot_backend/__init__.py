import os
from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__)
    app.config['DEBUG'] = True
    app.config['SECRET_KEY'] = 'JustDemonstrating'
    app.config['JWT_SECRET_KEY'] = 'this-should-be-change'


    from .views import views
    app.register_blueprint(views, url_prefix="/")

    return app