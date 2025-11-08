from flask import Flask, url_for, request, redirect, abort, render_template
import datetime
from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4
from lab5 import lab5

app = Flask(__name__)
app.secret_key = 'секретно-секретный секрет'
app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)
app.register_blueprint(lab5)

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
