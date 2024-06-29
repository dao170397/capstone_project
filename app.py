import os
from flask import (Flask, request, abort, jsonify)
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db
from auth import AuthError, requires_auth
from actor import actors_bp
from movie import movies_bp

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  if test_config is None:
    setup_db(app)
  else:
    setup_db(app, test_config['SQLALCHEMY_DATABASE_URI'])
  
  cors_options = {
    "origins": ["http://192.168.1.101:5000","https://capstone-2024-d432697adb92.herokuapp.com"],
    "methods": ["GET", "POST","PATCH", "DELETE"],
    "allow_headers": ["Content-Type", "Authorization"],
  }
  CORS(app, resources={r"/*": cors_options})
  
  @app.after_request
  def after_request(response):
    response.headers.add(
        "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
    )
    response.headers.add(
        "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
    )
    return response
  
  app.register_blueprint(movies_bp, url_prefix='/movies')
  app.register_blueprint(actors_bp, url_prefix='/actors')

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