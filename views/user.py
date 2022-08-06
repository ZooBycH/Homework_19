from flask import request
from flask_restx import Resource, Namespace

from dao.model.user import UserSchema
from implemented import user_service
from service.decorators import admin_required

user_ns = Namespace('users')

"""
Вьюха для добавления  пользователя
"""


@user_ns.route('/')
class UserView(Resource):

    def post(self):
        data = request.json
        user_service.create(data)
        return UserSchema().dump(data), 201
