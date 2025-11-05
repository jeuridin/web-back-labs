from flask import Blueprint, render_template, request, make_response, redirect, session
lab4 = Blueprint('lab4', __name__)

@lab4.route('/lab4/')
def lab():
    return render_template('lab4/lab4.html')


@lab4.route('/lab4/div-form')
def div_form():
    return render_template('lab4/div_form.html')

@lab4.route('/lab4/div', methods = ['post'])
def div():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('lab4/div.html', error='Оба поля должны быть заполнены!')
    x1 = int(x1)
    x2 = int(x2)
    result = x1 / x2
    return render_template('lab4/div.html', x1=x1, x2=x2, result=result)

@lab4.route('/lab4/sl-form')
def sl_form():
    return render_template('lab4/sl_form.html')


@lab4.route('/lab4/sl', methods=['POST'])
def sl():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' and x2 == '':
        result = 0
        return render_template('lab4/sl.html', x1=0, x2=0, result=result)
    if x1 == '':
        result = int(x2)
        return render_template('lab4/sl.html', x1=0, x2=x2, result=result)
    if x2 == '':
        result = int(x1)
        return render_template('lab4/sl.html', x2=0, x1=x1, result=result)
    x1 = int(x1)
    x2 = int(x2)
    result = x1 + x2
    return render_template('lab4/sl.html', x1=x1, x2=x2, result=result)
    
@lab4.route('/lab4/umn-form')
def umn_form():
    return render_template('lab4/umn_form.html')

@lab4.route('/lab4/umn', methods=['POST'])
def umn():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' and x2 == '':
        result = 0
        return render_template('lab4/umn.html', x1=0, x2=0, result=result)
    if x1 == '':
        result = int(x2)
        return render_template('lab4/umn.html', x1=1, x2=x2, result=result)
    if x2 == '':
        result = int(x1)
        return render_template('lab4/umn.html', x2=1, x1=x1, result=result)
    x1 = int(x1)
    x2 = int(x2)
    result = x1 * x2
    return render_template('lab4/umn.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/vch-form')
def vch_form():
    return render_template('lab4/vch_form.html')


@lab4.route('/lab4/vch', methods = ['POST'])
def vch():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('lab4/vch.html', error='Оба поля должны быть заполнены!')
    x1 = int(x1)
    x2 = int(x2)
    result = x1 - x2
    return render_template('lab4/vch.html', x1=x1, x2=x2, result=result)

@lab4.route('/lab4/step-form')
def step_form():
    return render_template('lab4/step_form.html')

@lab4.route('/lab4/step', methods= ['POST'])
def step():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('lab4/step.html', error='Оба поля должны быть заполнены!')
    x1 = int(x1)
    x2 = int(x2)
    if x1 == 0 and x2 == 0:
        return render_template('lab4/step.html', error='Оба поля должны быть заполнены!')
    result = x1 ** x2
    return render_template('lab4/step.html', x1=x1, x2=x2, result=result)


tree_count = 0 

@lab4.route('/lab4/tree', methods=['GET', 'POST'])
def tree():
    global tree_count
    if request.method == 'GET':
        return render_template('lab4/tree.html', tree_count=tree_count)
    
    operation = request.form.get('operation')
    if operation == 'cut':
        if tree_count > 0:
            tree_count -= 1
    elif operation == 'plant':
        if tree_count < 10:
            tree_count += 1
    return redirect('/lab4/tree')


users = [
    {'login': 'alex', 'name': 'Алекс', 'sex': 'мужской', 'password': '123',},
    {'login': 'bob', 'name': 'Боб', 'sex': 'мужской', 'password': '555'},
    {'login': 'janna', 'name': 'Жанна', 'sex': 'женский', 'password': '777'},
    {'login': 'alice', 'name': 'Элис', 'sex': 'женский', 'password': '444'},
    {'login': 'lily', 'name': 'Лили', 'sex': 'женский', 'password': '888'},
    {'login': 'john', 'name': 'Джон', 'sex': 'мужской', 'password': '444'}
]


@lab4.route('/lab4/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        authorized = 'login' in session
        login = session.get('login', '')
        name = session.get('name', '')
        error = session.pop('error', None)
        sex = request.form.get('sex', '')
        return render_template('lab4/login.html', authorized=authorized, login=login, name=name, error=error, sex=sex)    
    login = request.form.get('login')
    name = request.form.get('name')
    password = request.form.get('password')
    sex = request.form.get('sex')
    name = request.form.get('name')
    if not login and not password:
        session['error'] = 'Не введён логин и пароль!'
        return redirect('/lab4/login')
    elif not password:
        session['error'] = 'Не введен пароль!'
        return redirect('/lab4/login')
    elif not login:
        session['error'] = 'Не введен логин!'
        return redirect('/lab4/login')
    for user in users:
        if login == user['login'] and password == user['password']:
            session['login'] = login
            session['name'] = user['name']
            return redirect('/lab4/login')
    session['error'] = 'Неверный логин и/или пароль!'
    return redirect('/lab4/login')


@lab4.route('/lab4/logout', methods=['POST'])
def logout():
    session.pop('login', None)
    return redirect('/lab4/login')


@lab4.route('/lab4/fridge', methods=['GET', 'POST'])
def fridge():
    if request.method == 'POST':
        temp = request.form.get('temp')
        if not temp:
            error = 'Ошибочка'
            return render_template('lab4/fridge.html', error=error)
        else:
            temp = int(temp)
            if temp <= -12:
                error = "Не удалось установить температуру — слишком низкое значение."
            elif temp >= -1:
                error = "Не удалось установить температуру — слишком высокое значение."
            else:
                if temp >= -12 and temp <= -9:
                    error = f"Установлена температура: { temp }°С"
                    snowflakes = 3
                elif temp >= -8 and temp <= -5:
                    error = f"Установлена температура: { temp }°С"
                    snowflakes = 2
                else:
                    error = f"Установлена температура: { temp }°С"
                    snowflakes = 1
            return render_template('lab4/fridge.html', error=error, snowflakes=snowflakes)
    return render_template('lab4/fridge.html', error=error, snowflakes=snowflakes)


@lab4.route('/lab4/zerno')
def zerno():
    return render_template('lab4/zerno.html')

@lab4.route('/lab4/pay', methods=['GET', 'POST'])
def pay():
    error = None
    price = None
    zerno_name = None
    ves = None
    skidka = None
    razmer_skidki = 0

    if request.method == 'POST':
        zerno = request.form.get('zerno')
        ves = request.form.get('ves')
        if not zerno:
            return render_template('lab4/pay.html', error='Не выбрано зерно!!')
        elif not ves:
            return render_template('lab4/pay.html', error='Не введен вес!!')
        else:
            ves = int(ves)
            prices = {'yachmen':12000, 'ovyos':8500, 'pshenitsa':9000, 'rozh':15000}
            names = {'yachmen':'Ячмень', 'ovyos':'Овёс', 'pshenitsa':'Пшеница', 'rozh':'Рожь'}
            price = ves * prices[zerno]
            zerno_name = names[zerno]

            if ves <= 0:
                return render_template('lab4/pay.html', error='Не корректно указан!!')
            if ves > 100:
                return render_template('lab4/pay.html', error='Такого объёма сейчас нет в наличии')
            if ves > 10:
                razmer_skidki = (price * 10) / 100
                price = price - razmer_skidki
                skidka = 'Применена скидка за большой объём'
    return render_template('lab4/pay.html', price=price, zerno_name=zerno_name, ves=ves, error=error, skidka=skidka, razmer_skidki=razmer_skidki)


@lab4.route('/lab4/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'GET':
        error = session.pop('error', None)
        return render_template('lab4/registration.html', error=error)
    
    name = request.form.get('name')
    login = request.form.get('login')
    password = request.form.get('password')
    password_confirm = request.form.get('password_confirm')
    sex = request.form.get('sex')


    if not name or not login or not password or not password_confirm:
        session['error'] = 'Все поля обязательны!'
        return redirect('/lab4/registration')
    
    if password != password_confirm:
        session['error'] = 'Пароли не совпадают!'
        return redirect('/lab4/registration')
    
    for u in users:
        if u['login'] == login:
            session['error'] = 'Такой логин уже существует!'
            return redirect('/lab4/registration')

    users.append({
        'login': login,
        'name': name,
        'sex': sex,
        'password': password
    })

    session['login'] = login
    session['name'] = name

    return redirect('/lab4/login')

@lab4.route('/lab4/list', methods=['GET', 'POST'])
def user_list():
    if 'login' not in session:
        return redirect('/lab4/login')

    current_user = session['login']

    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'delete':
            global users
            users = [u for u in users if u['login'] != current_user]
            session.pop('login', None)
            session.pop('name', None)
            session['info'] = 'Ваш аккаунт удалён'
            return redirect('/lab4/login')
        elif action == 'edit':
            new_login = request.form.get('login')
            new_name = request.form.get('name')
            new_password = request.form.get('password')
            new_password_confirm = request.form.get('password_confirm')

            for user in users:
                if user['login'] == current_user:
                    if new_password or new_password_confirm:
                        if new_password != new_password_confirm:
                            session['error'] = 'Пароли не совпадают!'
                            return redirect('/lab4/list')
                        user['password'] = new_password
                    user['login'] = new_login
                    user['name'] = new_name
                    session['login'] = new_login
                    session['name'] = new_name
                    break
            return redirect('/lab4/list')

    error = session.pop('error', None)
    return render_template('/lab4/list.html', users=users, current_user=current_user, error=error)