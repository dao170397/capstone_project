import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Movie, Actor
from auth import AuthError, requires_auth

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  if test_config is None:
    setup_db(app)
  else:
    setup_db(app, test_config['SQLALCHEMY_DATABASE_URI'])
  CORS(app)
  
  @app.after_request
  def after_request(response):
    response.headers.add(
        "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
    )
    response.headers.add(
        "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
    )
    return response
  
  @app.route("/actors")
  @requires_auth('get:actors')
  def get_all_actors(payload):
    actors = Actor.query.order_by(Actor.id).all()
    return jsonify(
      {
          "success": True,
          "actors": [actor.format() for actor in actors],
          "total_actors": len(actors),
      }
    )
  
  @app.route("/movies")
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
  
  @app.route("/actors/<int:actor_id>", methods=["DELETE"])
  @requires_auth('delete:actor')
  def delete_actor(payload, actor_id):
    actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
    if actor is None:
      abort(404)
    actor.delete()
    return jsonify(
        {
            "success": True,
            "deleted": actor_id,
        }
    )
      
  @app.route("/movies/<int:movie_id>", methods=["DELETE"])
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

  @app.route("/actors", methods=['POST'])
  @requires_auth('post:actor')
  def create_new_actor(payload):
    body=request.get_json()
    name = body.get("name", None)
    age = body.get("age", None)
    gender = body.get("gender", None)
    movie_id=body.get("movie_id",None)
    try:
        actor = Actor(name=name, age=age, gender=gender, movie_id=movie_id)
        actor.insert()

        return jsonify({
        'success': True,
    }), 200
    except:
      abort(422)

  @app.route("/movies", methods=['POST'])
  @requires_auth('post:movie')
  def create_new_movie(payload):
    body=request.get_json()
    title = body.get("title", None)
    releaseDate = body.get("releaseDate", None)
    try:
        movie = Movie(title=title, releaseDate=releaseDate)
        movie.insert()

        return jsonify({
        'success': True,
    }), 200
    except:
        abort(422)

  @app.route("/actor/<id>", methods=["PATCH"])
  @requires_auth('path:actors')
  def update_actor(payload, id):
      actor = Actor.query.filter(Actor.id == id).one_or_none()
      if actor is None:
          abort(404)
      body=request.get_json()
      actor.name = body.get("name", None)
      actor.age = body.get("age", None)
      actor.gender = body.get("gender", None)
      actor.movie_id = body.get("movie_id",None)
      actor.update()
      return jsonify({
          'success': True,
          'actor': actor.format()
      }), 200
  
  @app.route("/movie/<id>", methods=["PATCH"])
  @requires_auth('path:movie')
  def update_movie(payload,id):
      movie = Movie.query.filter(Movie.id == id).one_or_none()
      if movie is None:
          abort(404)
      body=request.get_json()
      movie.title = body.get("title", None)
      movie.releaseDate = body.get("releaseDate", None)
      movie.update()
      return jsonify({
          'success': True,
          'movie': movie.format()
      }), 200
  
  @app.route('/')
  def get_greeting():
    excited = os.environ['EXCITED']
    greeting = '<a href="https://dev-dlteq0b34yxblndo.us.auth0.com/authorize?audience=capstone&response_type=token&client_id=dLT2Rj79FHep3d5dsji393zxqU3DKDzX&redirect_uri=http://192.168.1.101:8080">Login</a>'
    return greeting

  @app.errorhandler(422)
  def unprocessable(error):
    return (
        jsonify({"success": False, "error": 422, "message": "unprocessable"}),
        422,
    )

  @app.errorhandler(400)
  def bad_request(error):
    return (
      jsonify({"success": False, "error": 400, "message": "bad request"}),
      400,
    )
  
  @app.errorhandler(404)
  def not_found(error):
    return (
      jsonify({"success": False, "error": 404, "message": "not found"}),
      404,
    )
  
  @app.errorhandler(AuthError)
  def auth_error(error):
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error['description']
    }), error.status_code
  return app

app = create_app()
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)