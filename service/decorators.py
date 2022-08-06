import jwt
from flask import request, current_app, abort


def auth_required(func):
    def wrapper(*args, **kwargs):
        token = request.headers.environ.get('HTTP_AUTHORIZATION').replace('Bearer', "")

        if not token:
            raise abort(401)

        try:
            jwt.decode(token, key=current_app.config['SECRET_HERE'],
                       algorithm=current_app.config['ALGORITHM'])

            return func(*args, **kwargs)

        except Exception:
            raise Exception

    return wrapper


def admin_required(func):
    def wrapper(*args, **kwargs):
        token = request.headers.environ.get('HTTP_AUTHORIZATION').replace('Bearer', "")

        if not token:
            raise abort(401)

        try:
            data = jwt.decode(token, key=current_app.config['SECRET_HERE'],
                              algorithm=current_app.config['ALGORITHM'])

            if data['role'] == "admin":
                return func(*args, **kwargs)

        except Exception:
            raise Exception

        return wrapper
