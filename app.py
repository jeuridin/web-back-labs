from flask import Flask, url_for, request, redirect, abort, render_template
import datetime
app = Flask(__name__)

@app.route("/lab1/web")
def web():
    return """<!doctype html> 
        <html> 
           <body>
               <h1>web-сервер на flask </h1>
                <a href="/lab1/author">author</a>

           </body> 
        </html>""", 200, {
            "X-Server" : "sample",
            "Content-type" : 'text/plain; charset=utf-8'            
                         }

@app.route("/lab1/author")
def author():
    name = "Азарян Жанна Арамовна"
    group = "ФБИ-32"
    faculty = "ФБ"
    
    return """<!doctype html>
        <html>
            <body>
                <p>Студент: """ + name + """</p>
                <p>Группа: """ + group + """</p>
                <p>Факультет """ + faculty + """</p>
                <a href="/lab1/web">web</a>
            </body>
        </html>"""

@app.route('/lab1/image')
def image():
    path = url_for("static", filename="priroda.jpg")
    css_path = url_for('static', filename='main.css')
    return '''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" href="''' + css_path + '''">
    </head>
    <body>
        <h1>Вид</h1>
        <img src="''' + path + '''">
    </body>
</html>
    ''', 200, {
        'Content-Language': 'ru',
        'X-My-Zagolovok': 'priroda',
        'X-Another-Zagolovok': 'prirodaPhoto'
    }

count = 0
@app.route('/lab1/counter')
def counter():
    global count
    count += 1
    time = datetime.datetime.today()
    url = request.url
    client_ip = request.remote_addr

    return '''
<!doctype html>
<html>
    <body>
        Сколько раз вы сюда заходили: ''' + str(count) +'''
        <hr> 
        Дата и время: ''' + str(time) + '''<br>
        Запрошенный адрес: ''' + url + '''<br>
        Ваш IP-адрес: ''' + client_ip +'''<br>
        <a href="/cleaner">Очистка</a>
    </body>
</html>
'''

@app.route('/cleaner')
def cleaner():
        global count
        count = 0  
        return '''
<!doctype html>
<html>
    <body>
        <h1>Счётчик очищен. Можете перейти обратно на страницу счётчика.</h1>
        <a href="/lab1/counter">Назад к счётчику</a>
    </body>
</html>
'''



@app.route('/lab1/info')
def info():
    return redirect('/lab1/author')

@app.route('/lab1/created')
def created():
    return '''
<!doctype html>
<html>
    <body>
    <h1>Создано успешно</h1>
    <div><i>что-то создано</i></div>
    </body>
</html>
''', 201


visit_log = []
@app.errorhandler(404)
def not_found(err):
    error404 = url_for("static", filename="error.jpg")
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
        </ol>
        </main>
        <footer>
            Азарян Жанна Арамовна, ФБИ-32, 3 курс, 2025
        </footer>
    </body>
</html>
'''

@app.route('/lab1')
def lab1():
    return '''
<!doctype html>
<html>
    <head>
        <title>Лабораторная 1</title>
    </head>
    <body>
    <p>
            Flask — фреймворк для создания веб-приложений на языке
        программирования Python, использующий набор инструментов
        Werkzeug, а также шаблонизатор Jinja2. Относится к категории так
        называемых микрофреймворков — минималистичных каркасов
        веб-приложений, сознательно предоставляющих лишь самые базовые возможности.
    </p>
    <a href='/'>Главная страница</a>
    <h2>Список роутов:</h2>
        <ul>
            <li>
                <a href='/lab1/web'>Web-serber на Flask</a>
            </li>
            <li>
                <a href='/lab1/author'>Автор</a>
            </li>
            <li>
                <a href='/lab1/image'>Картинка</a>
            </li>
            <li>
                <a href='/lab1/counter'>Счетчик</a>
            </li>
            <li>
                <a href='/lab1/info'>Информация</a>
            </li>
            <li>
                <a href='/lab1/created'>Создание</a>
            </li>
            <li>
                <a href='/lab1'>Лабораторная 1</a>
            </li>
            <li>
                <a href='/lab1/err400'>Ошибка 400</a>
            </li>
            <li>
                <a href='/lab1/err401'>Ошибка 401</a>
            </li>
            <li>
                <a href='/lab1/err402'>Ошибка 402</a>
            </li>
            <li>
                <a href='/lab1/err403'>Ошибка 403</a>
            </li>
            <li>
                <a href='/lab1/err405'>Ошибка 405</a>
            </li>
            <li>
                <a href='/lab1/err418'>Ошибка 418</a>
            </li>
            <li>
                <a href='/lab1/500'>Ошибка 500</a>
            </li>
            <li>
                <a href='/lab1/blablabla'>Страница не сущетсвует</a>
            </li>
        </ul>
    </body>
</html>
'''

@app.route('/lab1/err400')
def err400():
    return '''
<!doctype html>
<html>
    <head>
        <style>
            h1 {
            font-weight: bold;
            color: red;
            }
        </style>
    </head>
    <body>
        <h1>Неверный запрос!!!!!</h1>
    </body>
</html>
''', 400

@app.route("/lab1/err401")
def err401():
    return '''
<!doctype html>
<html>
    <head>
        <style>
            h1 {
            font-size: 50px;
            color: red;
            }
        </style>
    </head>
    <body>
        <h1><i>Ой.. Для продолжения нужно войти в систему</i></h1>
    </body>
</html>
''', 401

@app.route('/lab1/err402')
def err402():
    return '''
<!doctype html>
<html>
    <head>
        <style>
            h1 {
            font-size: 50px;
            color: red;
            }
        </style>
    </head>
    <body>
        <h1>Необходима оплата!!</h1>
    </body>
</html>
''', 402

@app.route('/lab1/err403')
def err403():
    return '''
<!doctype html>
<html>
    <head>
        <style>
            h1 {
            font-size: 50px;
            color: red;
            }
        </style>
    </head>
    <body>
    <h1>У вас нет доступа к этому ресурсу</h1>
    </body>
</html>
''', 403


@app.route('/lab1/err405')
def err405():
    return '''
<!doctype html>
<html>
    <head>
    <style>
        h1 {
            font-size: 50px;
            color: red;
        }
    </style>
    </head>
    <body>
        <h1>Метод запроса запрещён для данного ресурса!!</h1>
    </body>
</html>
''', 405

@app.route('/lab1/err418')
def err418():
    return '''
<!doctype html>
<html>
    <head>
    <style>
        h1 {
            font-size: 50px;
            color: red;
        }
    </style>
    </head>
    <body>
        <h1>Я - чайник..</h1>
    </body>
</html>
''', 418

@app.route('/lab1/500')
def error500():
    return 1 / 0

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


@app.route('/lab2/a')
def a():
    return 'без слеша'

@app.route('/lab2/a/')
def a2():
    return 'с слешом'


flower_list =['роза', 'тюльпан', 'незабудка', 'ромашка']
@app.route('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    if flower_id >= len(flower_list):
        abort(404)
    else:
        return "цветок: " + flower_list[flower_id]
    
@app.route('/lab2/add_flower/<name>')
def add_flower(name):
    flower_list.append(name)
    return f'''
<!doctype html>
<html>
    <body>
    <h1>Добавлен новый цветок</h1>
    <p>Название нового цветка {name}</p>
    <p>Всего цветов: {len(flower_list)}</p>
    <p>Всего цветов {flower_list}</p>
    </body>
</html>
'''

@app.route('/lab2/example')
def example():
    name, lab_num, kurs, group = 'Жанна Азарян', 2, '3 курс', 'ФБИ-32'
    fruits = [
        {'name': 'яблоки', 'price': 100},
        {'name': 'груши', 'price': 120},
        {'name': 'апельсины', 'price': 80},
        {'name': 'мандарины', 'price': 95},
        {'name': 'манго', 'price': 321}
    ]
    return render_template('example.html', name=name, lab_num=lab_num, kurs=kurs, 
                           group=group, fruits=fruits)

@app.route('/lab2/')
def lab2():
    return render_template('lab2.html')

@app.route('/lab2/filters')
def filters():
    phrase = 'О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных..'
    return render_template('filter.html', phrase=phrase)