from flask import Flask, url_for, request, redirect, abort, render_template
import datetime
from flask_sqlalchemy import SQLAlchemy
from db import db
from os import path
import os
from db.models import users
from flask_login import LoginManager

from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4
from lab5 import lab5
from lab6 import lab6
from lab7 import lab7
from lab8 import lab8
from lab9 import lab9
from rgz import rgz

app = Flask(__name__)

login_manager = LoginManager()
login_manager.login_view = 'lab8.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(login_id):
    return users.query.get(int(login_id))


app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'секретно секретный-секрет').encode('utf-8')
app.config['DB_TYPE'] = os.getenv('DB_TYPE', 'postgres')
if app.config['DB_TYPE'] == 'postgres':
    db_name = 'janna_azaryan_orm'
    db_user = 'janna_azaryan_orm'
    db_password = '123'
    host_ip = '127.0.0.1'
    host_port = 5432

    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@{host_ip}:{host_port}/{db_name}'
else:
    dir_path = path.dirname(path.realpath(__file__))
    db_path = path.join(dir_path, 'janna_azaryan_orm.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

db.init_app(app)



app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)
app.register_blueprint(lab5)
app.register_blueprint(lab6)
app.register_blueprint(lab7)
app.register_blueprint(lab8)
app.register_blueprint(lab9)
app.register_blueprint(rgz)

visit_log = []
@app.errorhandler(404)
def not_found(err):
    error404 = url_for("static", filename="/lab1/error.jpg")
    time = datetime.datetime.today()
    client_ip = request.remote_addr
    url = request.url
    visit_log.append(f"{str(time)}, пользователь {client_ip} зашел на адрес <a href='{url}'>{url}</a>")
    log_html = ""
    for vhod in visit_log:
        log_html += vhod + "<br>"
    return '''
<!doctype html>
<html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Ошибка 404</title>
        <style>
            body {
                background-color: rgb(195, 222, 239);
            }
            h1 {
                font-size: 80px;
                color: blue;
                text-align: center;
            }
            img {
                display: block; 
                margin: 0 auto;
            }
            .log-container {
                max-width: 800px;
                margin: 20px auto;
                background-color: #DBE9FA;
                border: 6px solid #0277bd;
                padding: 15px;
                border-radius: 10px;
                box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
            }
        </style>
    </head>
    <body>
        <div class="log-container">
            <h2>Журнал посещений:</h2>
            ''' + log_html + '''
        </div>
        <h1>Блин... такой страницы не существует</h1>
        <img src="''' + error404 + '''">
    </body>
</html>
''', 404

@app.route('/')
@app.route('/index')
def index():
    return '''
<!doctype html>
<html>
    <body>
        <header>
            НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных
        </header>
        <main>
        <h1>Лабораторные работы</h1>
        <ol>
            <li>
            <a href='/lab1'>Лабораторная работа 1</a>
            </li>
            <li>
            <a href='/lab2'>Лабораторная работа 2</a>
            </li>
            <li>
            <a href='/lab3'>Лабораторная работа 3</a>
            </li>
            <li>
            <a href='/lab4'>Лабораторная работа 4</a>
            </li>
            <li>
            <a href='/lab5'>Лабораторная работа 5</a>
            </li>
            <li>
            <a href='/lab6'>Лабораторная работа 6</a>
            </li>
            <li>
            <a href='/lab7'>Лабораторная работа 7</a>
            </li>
            <li>
            <a href='/lab8'>Лабораторная работа 8</a>
            </li>
            <li>
            <a href='/lab9'>Лабораторная работа 9</a>
            </li>
        </ol>
        </main>
        <footer>
            Азарян Жанна Арамовна, ФБИ-32, 3 курс, 2025
        </footer>
    </body>
</html>
'''
@app.errorhandler(500)
def not_found(err):
    return '''
<!doctype html>
<html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Ошибка 500</title>
        <style>
            h1 {
                font-size: 50px;
                color: red;
            }
        </style>
    </head>
    <body>
    <h1>Whoops.. Внутренняя ошибка сервера</h1>
    </body>
</html>
''', 500
