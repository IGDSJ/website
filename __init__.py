from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from pymongo import MongoClient
import os

db = SQLAlchemy()
DB_NAME = 'database.db'

client = MongoClient('localhost', 27017)
banco = client.projeto_final_teste
aluno = banco.solar

upload_folder = "/website/uploads/"
image_folder = "/website/imagens/"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '123'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    if not os.path.exists(upload_folder):
        os.mkdir(upload_folder)
        
    if not os.path.exists(image_folder):
        os.mkdir(image_folder)

    app.config['UPLOAD_FOLDER'] = upload_folder
    
    db.init_app(app)

    from views import views
    from auth import auth

    app.register_blueprint(views, url_prefix ='/')
    app.register_blueprint(auth, url_prefix ='/')

    from models import User, Notes

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    if not path.exists('website/'+ DB_NAME):
        db.create_all(app=app)
        print('BD Criado!')
