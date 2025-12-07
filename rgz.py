from flask import Blueprint, render_template, request, session, current_app, jsonify, abort
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2
from datetime import date
from psycopg2.extras import RealDictCursor
import sqlite3
from os import path
from datetime import datetime
import re


rgz = Blueprint('rgz', __name__)

def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
            host='127.0.0.1',
            database='janna_azaryan_rgz',
            user='janna_azaryan_rgz',
            password='123'
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
    else:
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "databasergz.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
    return conn, cur

def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()

@rgz.route('/rgz/')
def main_page():
    return render_template('rgz/rgz.html')

@rgz.route('/rgz/register')
def register_page():
    return render_template('rgz/register.html')

@rgz.route('/rgz/login')
def login_page():
    return render_template('rgz/login.html')

import string

# Функция проверки логина и пароля
def is_valid_credential(text):
    if not text or text.strip() == "":
        return False
    allowed_chars = string.ascii_letters + string.digits + string.punctuation
    return all(char in allowed_chars for char in text)

@rgz.route('/rgz/rest-api/register', methods=['POST'])
def register():
    data = request.get_json()
    fullname = data.get('fullname')
    username = data.get('username')
    password = data.get('password')

    if not fullname or not username or not password:
        return jsonify({'error': 'Все поля обязательны'}), 400

    # Проверка логина и пароля
    if not is_valid_credential(username):
        return jsonify({'error': 'Логин содержит недопустимые символы'}), 400
    if not is_valid_credential(password):
        return jsonify({'error': 'Пароль содержит недопустимые символы'}), 400

    password_hash = generate_password_hash(password)
    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM users WHERE username=%s;", (username,))
        existing = cur.fetchone()
        if existing:
            db_close(conn, cur)
            return jsonify({'error': 'Имя пользователя уже занято'}), 400
        cur.execute(
            "INSERT INTO users (username, password, full_name) VALUES (%s, %s, %s) RETURNING id;",
            (username, password_hash, fullname)
        )
        user_id = cur.fetchone()['id']
    else:
        cur.execute("SELECT id FROM users WHERE username=?;", (username,))
        existing = cur.fetchone()
        if existing:
            db_close(conn, cur)
            return jsonify({'error': 'Имя пользователя уже занято'}), 400

        cur.execute(
            "INSERT INTO users (username, password, full_name) VALUES (?, ?, ?);",
            (username, password_hash, fullname)
        )
        
        user_id = cur.lastrowid


    db_close(conn, cur)
    return jsonify({'message': 'Пользователь зарегистрирован', 'user_id': user_id}), 201


@rgz.route('/rgz/rest-api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Логин и пароль обязательны'}), 400

    conn, cur = db_connect()
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM users WHERE username=%s;", (username,))
    else:
        cur.execute("SELECT * FROM users WHERE username=?;", (username,))
    user = cur.fetchone()
    db_close(conn, cur)

    if not user or not check_password_hash(user['password'], password):
        return jsonify({'error': 'Неверный логин или пароль'}), 401

    session['user_id'] = user['id']
    session['username'] = user['username']
    return jsonify({'message': f'Привет, {user["username"]}'}), 200


@rgz.route('/rgz/rest-api/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return jsonify({'message': 'Выход выполнен'}), 200




@rgz.route('/rgz/add')
def add_page():
    return render_template('rgz/add.html')

from flask import session, jsonify

@rgz.route('/rgz/rest-api/employees/', methods=['GET'])
def get_all_employee():
    conn, cur = db_connect()
    cur.execute(f"SELECT * FROM employees ORDER BY id;")
    emps = cur.fetchall()
    db_close(conn, cur)
    
    is_authenticated = session.get('user_id') is not None
    
    employees = []
    for emp in emps:
        employees.append({
            "id": emp["id"],
            "full_name": emp["full_name"],
            "position": emp["position"],
            "gender": emp["gender"],
            "phone": emp.get('phone', ''),
            "email": emp["email"],
            "trial": emp["trial"],
            "hire_date": str(emp["hire_date"]),
            "can_edit": is_authenticated  # новый флаг
        })
    
    return jsonify(employees)

@rgz.route('/rgz/rest-api/employees/<int:id>', methods=['GET'])
def get_employee(id):
    conn, cur = db_connect()
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM employees WHERE id = %s;", (id,))
    else:
        cur.execute("SELECT * FROM employees WHERE id = ?;", (id,))
    emp = cur.fetchone()
    db_close(conn, cur)

    if emp is None:
        abort(404)

    empl = {
        "id": emp["id"],
        "full_name": emp["full_name"],
        "position": emp["position"],
        "gender": emp["gender"],
        "phone": emp.get('phone', ''),
        "email": emp["email"],
        "trial": emp["trial"],
        "hire_date": str(emp["hire_date"])
    }

    return jsonify(empl)


@rgz.route('/rgz/rest-api/employees/', methods=['POST'])
def add_employee():
    employee = request.get_json()
    if not employee.get('full_name') or not employee.get('position') or not employee.get('gender') \
        or not employee.get('phone') or not employee.get('email') or not employee.get('trial') \
        or not employee.get('hire_date'):
            return jsonify({'error': 'Заполните все поля!'}), 400

    hire_date = employee['hire_date']
    day, month, year = hire_date.split('-')
    hire_date_db = f"{year}-{month}-{day}"

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("INSERT INTO employees (full_name, position, gender, phone, email, trial, hire_date) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id;", 
                    (employee['full_name'], employee['position'], employee['gender'], 
                    employee['phone'], employee['email'], employee['trial'], hire_date_db))
        new_id = cur.fetchone()['id']
        conn.commit()
    else:
        cur.execute("INSERT INTO employees (full_name, position, gender, phone, email, trial, hire_date) VALUES (?, ?, ?, ?, ?, ?, ?);", 
                    (employee['full_name'], employee['position'], employee['gender'], 
                     employee['phone'], employee['email'], employee['trial'], hire_date_db))

        conn.commit()
        new_id = cur.lastrowid

    db_close(conn, cur)

    return jsonify({'id': new_id}), 201


@rgz.route('/rgz/rest-api/employees/<int:id>', methods=['DELETE'])
def del_film(id):
    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM employees WHERE id = %s;", (id,))
    else:
        cur.execute("SELECT id FROM employees WHERE id = ?;", (id,))
    
    exists = cur.fetchone()
    if not exists:
        db_close(conn, cur)
        abort(404)

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("DELETE FROM employees WHERE id = %s;", (id,))
    else:
        cur.execute("DELETE FROM employees WHERE id = ?;", (id,))

    db_close(conn, cur)

    return '', 204


@rgz.route('/rgz/rest-api/employees/<int:id>', methods=['PUT'])
def put_employee(id):
    employee = request.get_json()

    # Проверка обязательных полей
    if not employee.get('full_name', '').strip():
        return jsonify({'full_name': 'Введите ФИО'}), 400
    if not employee.get('position', '').strip():
        return jsonify({'position': 'Введите должность'}), 400
    if not employee.get('gender', '').strip() or employee['gender'] not in ['М', 'Ж']:
        return jsonify({'gender': 'Выберите пол'}), 400
    if not employee.get('email', '').strip():
        return jsonify({'email': 'Введите email'}), 400
    if 'trial' not in employee or not isinstance(employee['trial'], bool):
        return jsonify({'trial': 'Выберите испытательный срок'}), 400
    if not employee.get('hire_date', '').strip():
        return jsonify({'hire_date': 'Введите дату устройства'}), 400

    # Проверка формата даты YYYY-MM-DD через регулярное выражение
    date_pattern = r'^\d{4}-\d{2}-\d{2}$'
    if not re.match(date_pattern, employee['hire_date']):
        return jsonify({'hire_date': 'Дата должна быть в формате YYYY-MM-DD'}), 400

    conn, cur = db_connect()
    if current_app.config.get('DB_TYPE') == 'postgres':
        cur.execute(
            "UPDATE employees SET full_name=%s, position=%s, gender=%s, phone=%s, email=%s, trial=%s, hire_date=%s WHERE id=%s RETURNING *;",
            (employee['full_name'], employee['position'], employee['gender'], employee.get('phone', ''),
            employee['email'], employee['trial'], employee['hire_date'], id)
        )
        updated = cur.fetchone()
        conn.commit()  # commit после получения данных
    else:
        cur.execute(
            "UPDATE employees SET full_name=?, position=?, gender=?, phone=?, email=?, trial=?, hire_date=? WHERE id=?;",
            (employee['full_name'], employee['position'], employee['gender'], employee.get('phone', ''),
            employee['email'], employee['trial'], employee['hire_date'], id)
        )
        conn.commit()  # commit перед запросом SELECT
        cur.execute("SELECT * FROM employees WHERE id=?;", (id,))
        updated = cur.fetchone()
    if updated is None:
        abort(404)

    return jsonify({
        "id": updated["id"],
        "full_name": updated["full_name"],
        "position": updated["position"],
        "gender": updated["gender"],
        "phone": updated.get("phone", ""),
        "email": updated["email"],
        "trial": updated["trial"],
        "hire_date": str(updated["hire_date"])
    })
