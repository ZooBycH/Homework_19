from flask import request
from flask_restx import Resource, Namespace

from dao.model.genre import GenreSchema
from implemented import genre_service
from service.decorators import auth_required, admin_required

genre_ns = Namespace('genres')

"""
Вьюха для жанров. Добавлено: методы  POST, PUT, DELETE, а так же декораторы для ограничения доступа 
"""


@genre_ns.route('/')
class GenresView(Resource):
    @auth_required
    def get(self):
        rs = genre_service.get_all()
        res = GenreSchema(many=True).dump(rs)
        return res, 200

    @admin_required
    def post(self):
        data = request.json
        return genre_service.create(data), 201


@genre_ns.route('/<int:gid>')
class GenreView(Resource):
    @auth_required
    def get(self, gid):
        r = genre_service.get_one(gid)
        sm_d = GenreSchema().dump(r)
        return sm_d, 200

    @admin_required
    def put(self, gid):
        data = request.json
        if not data.get('id') or (data.get('id') != gid):
            data['id'] = gid
        return genre_service.update(data), 200

    @admin_required
    def delete(self, gid):
        return genre_service.delete(gid)
