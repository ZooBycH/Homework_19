from flask import request
from flask_restx import Resource, Namespace

from dao.model.user import UserSchema
from implemented import user_service
from service.auth import generate_token, approve_token

auth_ns = Namespace('auth')


@auth_ns.route('/')
class AuthView(Resource):

    def post(self):
        """
        получает логин и пароль из Body запроса в виде JSON, далее проверяет соотвествие с данными в БД
        (есть ли такой пользователь, такой ли у него пароль)
        и если всё оk — генерит пару access_token и refresh_token и отдает их в виде JSON
        :return:
        """
        data = request.json
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return "Нет логина или пароля", 400

        user = user_service.get_by_username(username=username)

        return generate_token(username=user.username,
                              password=password,
                              password_hash=user.password,
                              role=user.role,
                              is_refresh=False), 201

    def put(self):
        """
        получает refresh_token из Body запроса в виде JSON,
        далее проверяет refresh_token и если он не истек и валиден — генерит пару
        access_token и refresh_token и отдает их в виде JSON
        :return:
        """
        data = request.json
        if not data.get('refresh_token'):
            return "", 400

        return approve_token(data.get('refresh_token')), 200
