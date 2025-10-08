from flask import Flask, url_for, request, redirect, abort, render_template
import datetime
from lab1 import lab1

app = Flask(__name__)
app.register_blueprint(lab1)


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
            <li>
            <a href='/lab2'>Лабораторная работа 2</a>
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


@app.route('/lab2/a')
def a():
    return 'без слеша'

@app.route('/lab2/a/')
def a2():
    return 'с слешом'


flower_list = [
        {'name': 'роза', 'price': 300},
        {'name': 'тюльпан', 'price': 310},
        {'name': 'незабудка', 'price': 320},
        {'name': 'ромашка', 'price': 330},
        {'name': 'георгин', 'price': 340},
        {'name': 'гладиолус', 'price': 350}
    ]
@app.route('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    if flower_id < 0 or flower_id >= len(flower_list):
        abort(404)
    else:
        return render_template('flower_detail.html',
                                flower=flower_list[flower_id], flower_id=flower_id)
    
@app.route('/lab2/add_flower/<name>/<int:price>')
def add_flower(name, price):
    flower_list.append({'name': name, 'price': price})
    return render_template('add_flower.html', name=name, price=price)

@app.route('/lab2/flowers/all')
def flowers_all():
    return render_template('flowers_all.html', flower_list=flower_list)

@app.route('/lab2/add_flower')
def add_flower_simple():
    name = request.args.get('name')
    price = request.args.get('price', type=int)
    if not name or price is None:
        return render_template('add_error.html')
    flower_list.append({'name': name, 'price': price})
    return redirect(url_for('flowers_all'))


@app.route('/lab2/f_cleaner')
def f_cleaner():
        flower_list.clear()
        return render_template('clear_flowers.html')

@app.route('/lab2/delete_flower/<int:flower_id>')
def delete_flower(flower_id):
    if flower_id < 0 or flower_id >= len(flower_list):
        abort(404)
    flower_list.pop(flower_id) 
    return redirect(url_for('flowers_all'))

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

@app.route('/lab2/calc/<int:a>/<int:b>')
def calc(a, b):
    return render_template('calc.html', a=a, b=b)

@app.route('/lab2/calc/')
def calc2():
    return redirect('/lab2/calc/1/1')

@app.route('/lab2/calc/<int:a>/')
def calc3(a):
    return redirect(url_for('calc', a=a, b=1))

books = [
    {'author': 'Лев Толстой', 'title': 'Война и мир', 'genre': 'Роман-эпопея', 'pages': 1300},
    {'author': 'Фёдор Достоевский', 'title': 'Преступление и наказание', 'genre': 'Психологический роман', 'pages': 670},
    {'author': 'Александр Пушкин', 'title': 'Евгений Онегин', 'genre': 'Роман', 'pages': 240},
    {'author': 'Михаил Булгаков', 'title': 'Мастер и Маргарита', 'genre': 'Роман', 'pages': 480},
    {'author': 'Харуки Мураками', 'title': 'Послемрак', 'genre': 'Роман', 'pages': 240},
    {'author': 'Юкио Мисима', 'title': 'Жизнь на продажу', 'genre': 'Художественная проза', 'pages': 288},
    {'author': 'Дж. Р. Р. Толкин', 'title': 'Властелин колец: Братство Кольца', 'genre': 'Фэнтези', 'pages': 530},
    {'author': 'Даниэль Дефо', 'title': 'Робинзон Крузо', 'genre': 'Приключенческий роман', 'pages': 320},
    {'author': 'Артур Конан Дойл', 'title': 'Собака Баскервилей', 'genre': 'Детектив', 'pages': 256},
    {'author': 'Джейн Остин', 'title': 'Гордость и предубеждение', 'genre': 'Роман', 'pages': 400}
]

@app.route('/lab2/books/')
def book_list():
    return render_template('book.html', books=books)

@app.route('/lab2/cars/')
def cars():
        cars = [
            {'name': 'Toyota Corolla', 'description': 'надёжный и экономичный седан для города', 'image': 'toyota.jpg'},
            {'name': 'Honda Civic', 'description': 'спортивный и практичный компактный автомобиль', 'image': 'civic.jpg'},
            {'name': 'Ford Mustang', 'description': 'легендарный американский мускул-кар с мощным двигателем', 'image': 'mustang.jpg'},
            {'name': 'Chevrolet Camaro', 'description': 'спортивное купе с агрессивным дизайном', 'image': 'camaro.jpg'},
            {'name': 'BMW 3 Series', 'description': 'премиальный седан с отличной управляемостью', 'image': 'bmw.jpg'},
            {'name': 'Mercedes-Benz C-Class', 'description': 'комфортный и стильный бизнес-седан', 'image': 'mercedes.jpg'},
            {'name': 'Audi A4', 'description': 'элегантный и технологичный немецкий седан', 'image': 'audi.jpg'},
            {'name': 'Volkswagen Golf', 'description': 'компактный хэтчбек с хорошей практичностью', 'image': 'golf.jpg'},
            {'name': 'Hyundai Tucson', 'description': 'надёжный кроссовер для семьи', 'image': 'tucson.jpg'},
            {'name': 'Kia Sportage', 'description': 'стильный и функциональный городской SUV', 'image': 'sportage.jpg'},
            {'name': 'Nissan Rogue', 'description': 'удобный кроссовер с просторным салоном', 'image': 'nissan.jpg'},
            {'name': 'Tesla Model 3', 'description': 'электромобиль с высокой автономностью и современными технологиями', 'image': 'tesla.jpg'},
            {'name': 'Porsche 911', 'description': 'спортивный автомобиль с легендарной историей', 'image': 'porsche.jpg'},
            {'name': 'Lamborghini Huracán', 'description': 'суперкар с мощным двигателем и впечатляющей скоростью', 'image': 'lambo.jpg'},
            {'name': 'Ferrari F8 Tributo', 'description': 'итальянский спорткар с динамичным дизайном', 'image': 'ferrari.jpg'},
            {'name': 'Mitsubishi Outlander', 'description': 'надёжный семейный кроссовер', 'image': 'mitsubishi.jpg'},
            {'name': 'Subaru Forester', 'description': 'внедорожник с отличной проходимостью и безопасностью', 'image': 'subaru.jpg'},
            {'name': 'Jeep Wrangler', 'description': 'легендарный внедорожник для бездорожья', 'image': 'jeep.jpg'},
            {'name': 'Volvo XC90', 'description': 'премиальный SUV с высоким уровнем безопасности', 'image': 'volvo.jpg'},
            {'name': 'Renault Clio', 'description': 'компактный и экономичный городской хэтчбек', 'image': 'clio.jpg'}
        ]
        return render_template('car.html', cars=cars)
