import os
from flask import Flask
#import pymysql
#from flask_sqlalchemy import SQLAlchemy
#from flask_migrate import Migrate

#pymysql.install_as_MySQLdb()
#db = SQLAlchemy()
#migrate = Migrate()

def create_app(test_config=None):
    app = Flask(__name__)
    app.config['DEBUG'] = True
    app.config['SECRET_KEY'] = 'JustDemonstrating'
    app.config['JWT_SECRET_KEY'] = 'this-should-be-change'

    ######## Register Database ########
    #app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://root:joyce50635@127.0.0.1:3306/kcs_database'
    #app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    #db.init_app(app)
    #migrate.init_app(app, db)
    #db.create_all(app=app)


    from .views import views
    app.register_blueprint(views, url_prefix="/")



    return app