import base64
import calendar
import datetime
import hashlib

import jwt
from flask import current_app, abort

"""
Сервис для авторизации и генерации токенов
"""


def __generate_passwort_digest(password: str):  # генерируем хеш пароля
    return hashlib.pbkdf2_hmac(
        hash_name="sha256",
        password=password.encode('utf-8'),
        salt=current_app.config['PWD_HASH_SALT'],
        iterations=current_app.config['PWD_HASH_ITERATIONS']
    )


def generate_password_hash(password: str):  # хеш -> строка
    return base64.b64encode(__generate_passwort_digest(password)).decode('utf-8')


def compare_password_hash(password_hash, other_password) -> bool:  # проверяет одинаковость хешей паролей
    return password_hash == generate_password_hash(other_password)


def generate_token(username, password_hash, password, role, is_refresh=False):  # генерируем два вида токенов
    if username is None:
        raise abort(404)

    if not is_refresh:
        if not compare_password_hash(password_hash=password_hash, other_password=password):
            abort(400)

    data = {
        "username": username,
        "password": password,
        "role": role
    }
    # Краткосрочный access_token
    min_30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=current_app.config['TOKEN_EXPIRE_MINUTES'])
    data['exp'] = calendar.timegm(min_30.timetuple())
    access_token = jwt.encode(data, key=current_app.config['SECRET_HERE'],
                              algorithm=current_app.config['ALGORITHM'])

    # Длительный refresh_token
    day_30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=current_app.config['TOKEN_EXPIRE_DAY'])
    data['exp'] = calendar.timegm(day_30.timetuple())
    refresh_token = jwt.encode(data, key=current_app.config['SECRET_HERE'],
                               algorithm=current_app.config['ALGORITHM'])

    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }


# Обновление токена
def approve_token(refresh_token):
    data = jwt.decode(refresh_token, key=current_app.config['SECRET_HERE'], algorithms=current_app.config['ALGORITHM'])
    username = data.get("username")
    password = data.get("password")
    role = data.get("role")
    return generate_token(username=username, password=password, password_hash=None, role=role,
                          is_refresh=True)
