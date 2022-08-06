from marshmallow import Schema, fields

from setup_db import db

"""
Это код из репозитория Skypro, он работает как надо :)
"""


class Director(db.Model):
    __tablename__ = 'director'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class DirectorSchema(Schema):
    id = fields.Int()
    name = fields.Str()
