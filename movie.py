
from flask import (Blueprint, request, abort, jsonify)
from models import Movie
from auth import requires_auth
import sys
import logging

# Configure the logging
logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(message)s')

movies_bp = Blueprint('movies_bp', __name__,static_url_path='movies')

'''
Return all movies in the server
Response: Message success, total movies
'''
@movies_bp.route("/")
@requires_auth('get:movies')
def get_all_movies(payload):
    movies = Movie.query.order_by(Movie.id).all()
    return jsonify(
      {
          "success": True,
          "movies": [movie.format() for movie in movies],
          "total_movies": len(movies),
      }
    )
      
'''
Delete movie by id
Parameter: int:movie_id
Response: Return the id of deleted movie
'''

@movies_bp.route("/<int:movie_id>", methods=["DELETE"])
@requires_auth('delete:movie')
def delete_movie(payload, movie_id):
    movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
    if movie is None:
      abort(404)
    movie.delete()
    return jsonify(
        {
            "success": True,
            "deleted": movie_id,
        }
    )
'''
Create a new movie
parameter: Model input movie include title, releaseDate
Response: A record is created and return Message success
'''
@movies_bp.route("/", methods=['POST'])
@requires_auth('post:movie')
def create_new_movie(payload):
    body=request.get_json()
    title = body.get("title")
    releaseDate = body.get("releaseDate")
    try:
        movie = Movie(title=title, releaseDate=releaseDate)
        movie.insert()

        return jsonify({
        'success': True,
    }), 200
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        logging.warning(f"Exception type: {exc_type}")
        logging.warning(f"Exception value: {exc_value}")
        logging.warning(f"Traceback: {exc_traceback}")
        abort(422)

'''
Update a movie record by Id
Parameter: Model input movie include id and some info of movie
Response: Return movie with new info and message success
'''
@movies_bp.route("/<id>", methods=["PATCH"])
@requires_auth('path:movie')
def update_movie(payload,id):
    movie = Movie.query.filter(Movie.id == id).one_or_none()
    if movie is None:
        abort(404)
    try:
        body=request.get_json()
        movie.title = body.get("title")
        movie.releaseDate = body.get("releaseDate")
        movie.update()
        return jsonify({
            'success': True,
            'movie': movie.format()
        }), 200
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        logging.warning(f"Exception type: {exc_type}")
        logging.warning(f"Exception value: {exc_value}")
        logging.warning(f"Traceback: {exc_traceback}")
        abort(422)