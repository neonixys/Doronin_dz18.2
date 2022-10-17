# Вьюха для жанра

from flask_restx import Namespace, Resource

from dao.model.genre import GenreSchema, Genre
from setup_db import db

genre_ns = Namespace('genres')
genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)


@genre_ns.route('/')
class GenreView(Resource):
    def get(self):
        all_genres = db.session.query(Genre).all()
        return genres_schema.dump(all_genres), 200


@genre_ns.route('/<int:gid>')
class GenreView(Resource):
    def get(self, gid: int):  # Получение данных
        genre = db.session.query(Genre).filter(Genre.id == gid).one()
        return genre_schema.dump(genre), 200
