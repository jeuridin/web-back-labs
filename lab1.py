from flask import Blueprint, url_for, request, redirect
import datetime
lab1 = Blueprint('lab1', __name__)

@lab1.route("/lab1/web")
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


@lab1.route("/lab1/")
def lab():
    
    return """<!doctype html>
        <html>
            <body>
                <p>Студент: """ + name + """</p>
                <p>Группа: """ + group + """</p>
                <p>Факультет """ + faculty + """</p>
                <a href="/lab1/web">web</a>
            </body>
        </html>"""


@lab1.route('/lab1/image')
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


@lab1.route('/lab1/counter')
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


@lab1.route('/cleaner')
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


@lab1.route('/lab1/info')
def info():
    return redirect('/lab1/author')


@lab1.route('/lab1/created')
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


@lab1.route('/lab1')
def lab1_main():
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


@lab1.route('/lab1/err400')
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


@lab1.route("/lab1/err401")
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


@lab1.route('/lab1/err402')
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


@lab1.route('/lab1/err403')
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


@lab1.route('/lab1/err405')
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


@lab1.route('/lab1/err418')
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

