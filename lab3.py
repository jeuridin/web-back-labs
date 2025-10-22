from flask import Blueprint, render_template, request, make_response, redirect
lab3 = Blueprint('lab3', __name__)


@lab3.route('/lab3/')
def lab():
    name = request.cookies.get('name')
    name_color = request.cookies.get('name_color')
    age = request.cookies.get('age')
    return render_template('lab3/lab3.html', name=name, name_color=name_color, age=age)


@lab3.route('/lab3/cookie')
def cookie():
    resp = make_response(redirect('/lab3'))
    resp.set_cookie('name', 'Alex', max_age=5)
    resp.set_cookie('age', '20')
    resp.set_cookie('name_color', 'magenta')
    return resp


@lab3.route('/lab3/del_cookie')
def del_cookie():
    resp = make_response(redirect('/lab3'))
    resp.delete_cookie('name')
    resp.delete_cookie('age')
    resp.delete_cookie('name_color')
    return resp


@lab3.route('/lab3/form1')
def form1():
    errors = {}
    user = request.args.get('user')
    if user == '':
        errors['user'] = 'Заполните поле!'
    age = request.args.get('age')
    if age == '':
        errors['age'] = 'Заполните поле!'
    sex = request.args.get('sex')
    return render_template('lab3/form1.html', user=user, age=age, sex=sex, errors=errors)


@lab3.route('/lab3/order')
def order():
    return render_template('lab3/order.html')


@lab3.route('/lab3/pay')
def pay():
    price = 0
    drink = request.args.get('drink')
    if drink == 'coffee':
        price = 120
    elif drink == 'black-tea':
        price = 80
    else:
        price = 70
    if request.args.get('milk') == 'on':
        price += 30
    if request.args.get('sugar') == 'on':
        price += 10
    return render_template('lab3/pay.html', price=price)



@lab3.route('/lab3/success')
def success():
    price = request.args.get('price', 0)
    return render_template('lab3/success.html', price=price)


@lab3.route('/lab3/settings')
def settings():
    color = request.args.get('color')
    bg_color = request.args.get('bg_color')
    font_size = request.args.get('font_size')
    font_family = request.args.get('font_family')
    if any([color, bg_color, font_size]):
        resp = make_response(redirect('/lab3/settings'))
        if color:
            resp.set_cookie('color', color)
        if bg_color:
            resp.set_cookie('bg_color', bg_color)
        if font_size:
            resp.set_cookie('font_size', font_size)
        if font_family:
            resp.set_cookie('font_family', font_family)
        return resp
    color = request.cookies.get('color')
    bg_color = request.cookies.get('bg_color')
    resp = make_response(render_template('lab3/settings.html', color=color, bg_color=bg_color, font_size=font_size, font_family=font_family))
    return resp
    
@lab3.route('/lab3/ticket')
def ticket():
    fio = request.args.get('fio')
    polka = request.args.get('polka')
    belie = request.args.get('belie') == 'on'
    bagazh = request.args.get('bagazh') == 'on'
    age = request.args.get('age')
    viezd = request.args.get('viezd')
    naznachenie = request.args.get('naznachenie')
    data = request.args.get('data')
    strahovka = request.args.get('strahovka') == 'on'

    if not fio:
        return render_template('/lab3/ticket.html')
    if age:
        age_int = int(age)
    else:
        age_int = 0

    if age_int < 18:
        base_price = 700
    else:
        base_price = 1000
    
    if polka == 'bottom' or polka == 'bottom-bok':
        polka_price = 100
    else:
        polka_price = 0
    
    total_price = base_price + polka_price
    if belie:
        total_price += 75
    if bagazh:
        total_price += 250
    if strahovka:
        total_price += 150
    return render_template('/lab3/ticket_result.html', fio=fio, polka=polka, belie=belie, bagazh=bagazh, age=age_int, 
                        viezd=viezd, naznachenie=naznachenie, data=data, strahovka=strahovka, base_price=base_price,
                        polka_price=polka_price, total_price=total_price)

@lab3.route("/lab3/settings/reset")
def reset_settings():
    resp = make_response(redirect('/lab3/settings'))
    resp.delete_cookie('color')
    resp.delete_cookie('bg_color')
    resp.delete_cookie('font_size')
    resp.delete_cookie('font_family')
    return resp
from flask import request, make_response, render_template

@lab3.route('/lab3/dop', methods=['GET', 'POST'])
def dop():
    phones = [
        {"name": "iPhone 15 Pro", "price": 129990, "brand": "Apple", "color": "Титановый синий", "storage": 256, "screen": 6.1},
        {"name": "iPhone 15", "price": 89990, "brand": "Apple", "color": "Черный", "storage": 128, "screen": 6.1},
        {"name": "Galaxy S24 Ultra", "price": 119990, "brand": "Samsung", "color": "Серый", "storage": 512, "screen": 6.8},
        {"name": "Galaxy A54", "price": 34990, "brand": "Samsung", "color": "Белый", "storage": 128, "screen": 6.4},
        {"name": "Redmi Note 13 Pro", "price": 29990, "brand": "Xiaomi", "color": "Синий", "storage": 256, "screen": 6.67},
        {"name": "Poco X6 Pro", "price": 27990, "brand": "Xiaomi", "color": "Желтый", "storage": 256, "screen": 6.67},
        {"name": "Pixel 8 Pro", "price": 79990, "brand": "Google", "color": "Черный", "storage": 128, "screen": 6.7},
        {"name": "Nothing Phone 2", "price": 49990, "brand": "Nothing", "color": "Белый", "storage": 256, "screen": 6.7},
        {"name": "OnePlus 12", "price": 69990, "brand": "OnePlus", "color": "Зеленый", "storage": 256, "screen": 6.82},
        {"name": "Realme GT 5", "price": 45990, "brand": "Realme", "color": "Серебристый", "storage": 512, "screen": 6.74},
        {"name": "Vivo X100", "price": 59990, "brand": "Vivo", "color": "Синий", "storage": 256, "screen": 6.78},
        {"name": "Oppo Find X6", "price": 74990, "brand": "Oppo", "color": "Зеленый", "storage": 512, "screen": 6.74},
        {"name": "Honor Magic 5", "price": 52990, "brand": "Honor", "color": "Фиолетовый", "storage": 256, "screen": 6.73},
        {"name": "Huawei P60", "price": 64990, "brand": "Huawei", "color": "Черный", "storage": 256, "screen": 6.67},
        {"name": "ASUS ROG Phone 8", "price": 89990, "brand": "ASUS", "color": "Черный", "storage": 512, "screen": 6.78},
        {"name": "Nokia G42", "price": 19990, "brand": "Nokia", "color": "Фиолетовый", "storage": 128, "screen": 6.56},
        {"name": "Motorola Edge 40", "price": 42990, "brand": "Motorola", "color": "Синий", "storage": 256, "screen": 6.55},
        {"name": "Sony Xperia 5 V", "price": 79990, "brand": "Sony", "color": "Черный", "storage": 256, "screen": 6.1},
        {"name": "Tecno Camon 20", "price": 15990, "brand": "Tecno", "color": "Зеленый", "storage": 128, "screen": 6.67},
        {"name": "Infinix Note 30", "price": 17990, "brand": "Infinix", "color": "Золотой", "storage": 256, "screen": 6.78}
    ]
    
    all_prices = [phone['price'] for phone in phones]
    min_price_all = min(all_prices)
    max_price_all = max(all_prices)

    if request.method == 'POST':
        min_price = request.form.get('min_price', '')
        max_price = request.form.get('max_price', '')
    else:
        min_price = request.cookies.get('min_price', '')
        max_price = request.cookies.get('max_price', '')

    if request.form.get('reset'):
        min_price = ''
        max_price = ''

    filtered_phones = phones
    if min_price or max_price:
        if min_price and max_price:
            if float(min_price) > float(max_price):
                min_price, max_price = max_price, min_price
        
        if min_price:
            filtered_phones = [phone for phone in filtered_phones if phone['price'] >= float(min_price)]
        if max_price:
            filtered_phones = [phone for phone in filtered_phones if phone['price'] <= float(max_price)]

    resp = make_response(render_template(
        'lab3/dop.html', phones=filtered_phones, min_price=min_price, max_price=max_price,
        min_price_all=min_price_all, max_price_all=max_price_all, count=len(filtered_phones)
    ))

    if not request.form.get('reset'):
        if min_price:
            resp.set_cookie('min_price', min_price)
        if max_price:
            resp.set_cookie('max_price', max_price)
    else:
        resp.set_cookie('min_price', '', expires=0)
        resp.set_cookie('max_price', '', expires=0)

    return resp
