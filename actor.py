from flask import (Blueprint, request, abort, jsonify)
from models import Actor
from auth import requires_auth
import sys
import logging

# Configure the logging
logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(message)s')

actors_bp = Blueprint('actors_bp', __name__,static_url_path='actors')
'''
Return all actors in the server
Response: Message success, total actors, details of each actor
'''
@actors_bp.route('/')
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

'''
Delete actor by id
Parameter: int:actor_id
Response: Return the id of deleted actor
'''
@actors_bp.route("/<int:actor_id>", methods=["DELETE"])
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
'''
Create a new actor
parameter: Model input actor include name, age, gender, [optional] movie_id
Response: A record is created and return Message success
'''
@actors_bp.route("/", methods=['POST'])
@requires_auth('post:actor')
def create_new_actor(payload):
    body=request.get_json()
    name = body.get("name")
    age = body.get("age")
    gender = body.get("gender")
    movie_id=body.get("movie_id")
    try:
        actor = Actor(name=name, age=age, gender=gender, movie_id=movie_id)
        actor.insert()

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
Update a actor record by Id
Parameter: Model input actor include id and some info of actor
Response: Return actor with new info and message success
'''
@actors_bp.route("/<id>", methods=["PATCH"])
@requires_auth('path:actors')
def update_actor(payload, id):
    actor = Actor.query.filter(Actor.id == id).one_or_none()
    if actor is None:
        abort(404)
    try:
        body=request.get_json()
        actor.name = body.get("name")
        actor.age = body.get("age")
        actor.gender = body.get("gender")
        actor.movie_id = body.get("movie_id")
        actor.update()
        return jsonify({
            'success': True,
            'actor': actor.format()
        }), 200
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        logging.warning(f"Exception type: {exc_type}")
        logging.warning(f"Exception value: {exc_value}")
        logging.warning(f"Traceback: {exc_traceback}")
        abort(422)
        abort(422)