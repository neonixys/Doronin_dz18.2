from marshmallow import Schema, fields

# Описание модели и схемы "Жанр"


from setup_db import db


class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class GenreSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String()
