# Вьюха для фильма

from flask import request
from flask_restx import Namespace, Resource

from container import movie_service
from dao.model.movie import MovieSchema, Movie
from setup_db import db

movie_ns = Namespace('movies')
movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)


@movie_ns.route('/')
class MoviesView(Resource):
    def get(self):
        director_request = request.args.get('director_id')
        genre_request = request.args.get('genre_id')
        year_request = request.args.get('year')

        if director_request:
            movies = movie_service.get_by_director(director_request)
            return movies_schema.dump(movies), 200
        if genre_request:
            movies = movie_service.get_by_genre(genre_request)
            return movies_schema.dump(movies), 200
        if year_request:
            movies = movie_service.get_by_year(year_request)
            return movies_schema.dump(movies), 200

        all_movies = db.session.query(Movie).all()
        return movies_schema.dump(all_movies), 200

    def post(self):
        req_json = request.json
        new_movie = Movie(**req_json)

        with db.session.begin():
            db.session.add(new_movie)

        return "", 201


@movie_ns.route('/<int:mid>')
class MoviesView(Resource):
    def get(self, mid: int):  # Получение всех фильмов
        movie = db.session.query(Movie).filter(Movie.id == mid).one()
        return movie_schema.dump(movie), 200


    def put(self, mid):  # замена данных
        movie = db.session.query(Movie).get(mid)
        req_json = request.json

        movie.title = req_json.get("title")
        movie.description = req_json.get("description")
        movie.trailer = req_json.get("trailer")
        movie.year = req_json.get("year")
        movie.rating = req_json.get("rating")

        db.session.add(movie)
        db.session.commit()

        return "", 204

    def patch(self, mid):  # частичное обновление
        movie = db.session.query(Movie).get(mid)
        req_json = request.json

        if "title" in req_json:
            movie.title = req_json.get("title")
        if "description" in req_json:
            movie.description = req_json.get("description")
        if "trailer" in req_json:
            movie.trailer = req_json.get("trailer")
        if "year" in req_json:
            movie.year = req_json.get("year")
        if "rating" in req_json:
            movie.rating = req_json.get("rating")

        db.session.add(movie)
        db.session.commit()

        return "", 204

    def delete(self, mid):  # замена данных
        movie = db.session.query(Movie).get(mid)

        db.session.delete(movie)
        db.session.commit()
        return "", 204
