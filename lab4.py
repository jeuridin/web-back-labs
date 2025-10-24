from flask import Blueprint, render_template, request, make_response, redirect
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
    {'login': 'alex', 'password': '123'},
    {'login': 'bob', 'password': '555'},
    {'login': 'janna', 'password': '777'},
    {'login': 'alice', 'password': '444'},
    {'login': 'lily', 'password': '888'},
    {'login': 'john', 'password': '444'}
]


@lab4.route('/lab4/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab4/login.html', authorized=False)
    
    login = request.form.get('login')
    password = request.form.get('password')
    for user in users:
        if login == user['login'] and password == user['password']:
            return render_template('lab4/login.html', login=login, authorized=True)
    error = 'Не верный логин и/или пароль'
    return render_template('lab4/login.html', error=error, authorized=False)