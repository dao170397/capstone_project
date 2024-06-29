
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db,db
class CapstoneTestCase(unittest.TestCase):

    def setUp(self):
        database_name = 'capstone_test'
        database_path = 'postgresql://{}:{}@{}/{}'.format(
    'postgres', 'sys', 'localhost:5432', database_name)
        """Define test variables and initialize app."""
        self.app = create_app({'SQLALCHEMY_DATABASE_URI': database_path})
        self.client = self.app.test_client

        self.new_actor = {
        "name":"Tom Cruise",
        "age":61,
        "gender":"M",
        "movie_id":1
        }
        self.new_movie = {
        "title":"Endless Love",
        "releaseDate":"01/24/2022"
        }
        self.token_casting_assistant=os.environ['ASSISTANT']
        self.token_casting_director=os.environ['DIRECTOR']
        self.token_executive_producer=os.environ['PRODUCER']
        # binds the app to the current context
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        # with self.app.app_context():
        #   db.session.remove()
        #   db.drop_all()
        pass
    def test_post_movie_casting_assistant(self):
        header_obj = {
            "Authorization":self.token_casting_assistant
        }
        res = self.client().post("/movies", json=self.new_movie, headers=header_obj)
        data = res.get_json()
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)

    def test_post_movie_casting_director(self):
        header_obj = {
            "Authorization":self.token_casting_director
        }
        res = self.client().post("/movies", json=self.new_movie, headers=header_obj)
        data = res.get_json()
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)
        
    def test_post_movie_executive_producer(self):
        header_obj = {
            "Authorization":self.token_executive_producer
        }
        res = self.client().post("/movies",json=self.new_movie, headers=header_obj)
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_post_movie_return_error_422(self):
        header_obj = {
            "Authorization":self.token_executive_producer
        }
        new_movie = {
        "title":"My world",
        "releaseDate":"to day"
        }
        res = self.client().post("/movies",json=new_movie, headers=header_obj)
        data = res.get_json()
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)

    def test_post_actor_casting_assistant(self):
        header_obj = {
            "Authorization":self.token_casting_assistant
        }
        res = self.client().post("/actors", json=self.new_actor, headers=header_obj)
        data = res.get_json()
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)

    def test_post_actor_casting_director(self):
        header_obj = {
            "Authorization":self.token_casting_director
        }
        res = self.client().post("/actors", json=self.new_actor, headers=header_obj)
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        
    def test_post_actor_executive_producer(self):
        header_obj = {
            "Authorization":self.token_executive_producer
        }
        res = self.client().post("/actors",json=self.new_actor, headers=header_obj)
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_post_actor_return_error_422(self):
        header_obj = {
            "Authorization":self.token_executive_producer
        }
        new_actor={
            "name":"Tom Cruise",
            "age":"hello",
            "gender":"M",
            "movie_id":1
        }
        res = self.client().post("/actors",json=new_actor, headers=header_obj)
        data = res.get_json()
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
    
    

    def test_get_all_movies(self):
        header_obj = {
            "Authorization":self.token_casting_assistant
        }
        res = self.client().get("/movies", headers=header_obj)
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_get_all_movies_error(self):
        res = self.client().get("/movies")
        data = res.get_json()
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)

    def test_get_all_actor_autho(self):
        header_obj = {
            "Authorization":self.token_casting_assistant
        }
        res = self.client().get("/actors", headers=header_obj)
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_get_all_actors_error_autho(self):
        res = self.client().get("/actors")
        data = res.get_json()
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)
    
    def test_update_actor(self):
        header_obj = {
            "Authorization":self.token_executive_producer
        }
        new_actor={
            "name":"New Actor",
            "age":"62",
            "gender":"M"
        }
        res = self.client().patch("/actors/1", json=new_actor, headers=header_obj)
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
    
    def test_update_movie(self):
        header_obj = {
            "Authorization":self.token_executive_producer
        }
        new_movie = {
        "title":'New Movie',
        "releaseDate":"01/9/2022"
        }
        res = self.client().patch("/movies/1", json=new_movie,headers=header_obj)
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_delete_actor(self):
        header_obj = {
            "Authorization":self.token_executive_producer
        }
        res = self.client().delete("/actors/1",headers=header_obj)
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted"], 1)

    def test_delete_actor_error_404(self):
        header_obj = {
            "Authorization":self.token_executive_producer
        }
        res = self.client().delete("/actors/999",headers=header_obj)
        data = res.get_json()
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)

    def test_delete_movie(self):
        header_obj = {
            "Authorization":self.token_executive_producer
        }
        res = self.client().delete("/movies/1",headers=header_obj)
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted"], 1)

    def test_delete_movie(self):
        header_obj = {
            "Authorization":self.token_executive_producer
        }
        res = self.client().delete("/movies/999",headers=header_obj)
        data = res.get_json()
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
