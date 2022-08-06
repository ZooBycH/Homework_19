import jwt
from flask import request, current_app, abort

"""
Декораторы для ограничения доступа к эндпоинтам и доступа с правами администратора
"""


def auth_required(func):
    def wrapper(*args, **kwargs):
        data = request.headers['Authorization']
        token = data.split("Bearer ")[-1]

        if not token:
            raise abort(401)

        try:
            jwt.decode(token, key=current_app.config['SECRET_HERE'],
                       algorithms=current_app.config['ALGORITHM'])

            return func(*args, **kwargs)

        except Exception:
            raise Exception

    return wrapper


def admin_required(func):
    def wrapper(*args, **kwargs):
        data = request.headers['Authorization']
        token = data.split("Bearer ")[-1]
        role = None

        if not token:
            raise abort(401)

        try:
            data = jwt.decode(token, key=current_app.config['SECRET_HERE'],
                              algorithms=current_app.config['ALGORITHM'])
            role = data.get("role")

        except Exception as e:
            print("JWT Decode Exception", e)

        if role != "admin":
            abort(403)

        return func(*args, **kwargs)

    return wrapper
