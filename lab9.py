from flask import Blueprint, render_template, request, make_response, redirect, session, current_app, abort, jsonify
import psycopg2
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash
from psycopg2.extras import RealDictCursor
import sqlite3
from os import path
import random

lab9 = Blueprint('lab9', __name__)

users = {}

messages = [
    "С Новым годом!", "Счастья!", "Здоровья!", "Удачи!",
    "Любви!", "Радости!", "Успехов!", "Тепла!", "Мира!", "Денег!"
]

BOX_COUNT = 10
MAX_OPEN = 3

def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
                host = '127.0.0.1',
                database = 'janna_azaryan_knowledge_base',
                user = 'janna_azaryan_knowledge_base',
                password = '123'
            )
        cur = conn.cursor(cursor_factory= RealDictCursor)
    else:
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "database.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
    return conn, cur

def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()

@lab9.route('/lab9/')
def index():
    if 'positions' not in session:
        session['positions'] = [
            {
                'id': i,
                'top': f"{random.randint(5,70)}%",
                'left': f"{random.randint(5,90)}%"
            } for i in range(BOX_COUNT)
        ]

    if 'opened_boxes' not in session:
        session['opened_boxes'] = []

    return render_template('lab9/index.html')

@lab9.route('/lab9/state')
def state():
    opened = session.get('opened_boxes', [])
    opened_count = len(opened)

    return jsonify({
        'logged_in': session.get('logged_in', False),
        'opened_boxes': opened,
        'opened_count': opened_count,
        'positions': session.get('positions', [])
    })



@lab9.route('/lab9/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Заполните все поля'})

    conn, cur = db_connect()
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM users WHERE login = %s", (username,))
    else:
        cur.execute("SELECT * FROM users WHERE login = ?", (username,))
    user = cur.fetchone()
    if user:
        db_close(conn, cur)
        return jsonify({'error': 'Пользователь уже существует'})

    hashed = generate_password_hash(password)
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("INSERT INTO users (login, password) VALUES (%s, %s)", (username, hashed))
    else:
        cur.execute("INSERT INTO users (login, password) VALUES (?, ?)", (username, hashed))
    db_close(conn, cur)
    return jsonify({'ok': True})

@lab9.route('/lab9/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # Подключение к БД
    conn, cur = db_connect()
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM users WHERE login = %s", (username,))
    else:
        cur.execute("SELECT * FROM users WHERE login = ?", (username,))
    user = cur.fetchone()
    db_close(conn, cur)

    if not user:
        return jsonify({'error': 'Неверный логин или пароль'})

    # Получаем хеш пароля
    db_password = user['password']  # одинаково для Postgres и SQLite
    if not check_password_hash(db_password, password):
        return jsonify({'error': 'Неверный логин или пароль'})

    # Авторизация
    session['logged_in'] = True
    session['username'] = username
    session['opened_boxes'] = []

    return jsonify({'ok': True})



@lab9.route('/lab9/open', methods=['POST'])
def open_box():
    data = request.json
    box_id = data.get('id')

    if not isinstance(box_id, int) or box_id < 0 or box_id >= BOX_COUNT:
        return jsonify({'error': 'Некорректный номер коробки'})

    opened = session.get('opened_boxes', [])
    if box_id in opened:
        return jsonify({'error': 'Коробка уже открыта'})
    if len(opened) >= MAX_OPEN:
        return jsonify({'error': 'Можно открыть только 3 коробки'})
    if box_id >= 7 and not session.get('logged_in'):
        return jsonify({'error': 'Этот подарок доступен только авторизованным'})

    opened.append(box_id)
    session['opened_boxes'] = opened
    opened_count = len(opened)

    return jsonify({
        'ok': True,
        'message': messages[box_id],
        'opened_count': opened_count
    })

@lab9.route('/lab9/logout', methods=['POST'])
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    session['opened_boxes'] = []
    return jsonify({'ok': True})

@lab9.route('/lab9/santa_reset', methods=['POST'])
def santa_reset():
    if not session.get('logged_in'):
        return jsonify({'error': 'Требуется авторизация'})
    session['opened_boxes'] = []
    return jsonify({'ok': True})


