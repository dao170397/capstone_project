
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
        self.token_casting_assistant='Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImpWeFk1ekJsNDdGazYtbFpVemtXSiJ9.eyJpc3MiOiJodHRwczovL2Rldi1kbHRlcTBiMzR5eGJsbmRvLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2Njc0NzU0NWUzNzYzNGVjMjFkMTA4YzkiLCJhdWQiOiJjYXBzdG9uZSIsImlhdCI6MTcxOTUwMDM0NiwiZXhwIjoxNzE5NTA3NTQ2LCJzY29wZSI6IiIsImF6cCI6ImRMVDJSajc5RkhlcDNkNWRzamkzOTN6eHFVM0RLRHpYIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.hw1yngmHBOTq_2mSg-RY-Ic-urDUTMJMU-xKGXNp-rP2Xk832lXmzqNR1D-dwBIVi20hzTfd9OCGjxNCMqbX_xoG_4OKcfAyKyG7_MX-JbpENUdME9Ox_ayuXPrVku4w3TfG_JbyveO8cU1Wr3AtBnxswTzq65hYWroEnAjZhvN9H9H9G-XxUlaJtKEN3FQrx2yL-iRUNZSkjeOYOezAIuezVN7qhSMrVXWPmt-X2iYM_I8sFWDALxKIFWEkQP-hVH6C1wWQ4xjCkCh9HXlpWfzkModTwV5bnFZGUtHWk0tWj-nFtxFEURikwbsrt7QMKduw8p6l4TY6Fqp810f-Mg'
        self.token_casting_director='Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImpWeFk1ekJsNDdGazYtbFpVemtXSiJ9.eyJpc3MiOiJodHRwczovL2Rldi1kbHRlcTBiMzR5eGJsbmRvLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2Njc0NzVhMmI5NDQ2YTM3YjVmNDAzODciLCJhdWQiOiJjYXBzdG9uZSIsImlhdCI6MTcxOTUwMDQ2NSwiZXhwIjoxNzE5NTA3NjY1LCJzY29wZSI6IiIsImF6cCI6ImRMVDJSajc5RkhlcDNkNWRzamkzOTN6eHFVM0RLRHpYIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9yIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRoOmFjdG9ycyIsInBhdGg6bW92aWUiLCJwb3N0OmFjdG9yIl19.ckhkSvXG6J25uiYrckZ2FxWvI83YVE-m1GzexBPNGwCBOVNaG6Z2titGgpDPOz2EDHPwzlslxOTjFnLi_qDH9luWn73Yk4cJatK1V6k1TFucKlI6vSg-q0u29PixMjM5Oy7jJ6UmY4RbcMbajELh7Cem0X5jHgVoFKTd7JZ9tqrkntxw5DAXgbfpLEkhHAMgb3bvLhV-3Rr52o5weLbnUONWX7ittApdpGvQOAwai0gLBaTpKxMqNWRmfFYEMbB7mXmMj_xz0ynzPtL3XyVHVt87LnnrdrtS92qjVujl7zqGkEnNls6jec1dUWmHzzY9JHjZdaIMezH-FwvUTL3Q7g'
        self.token_executive_producer='Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImpWeFk1ekJsNDdGazYtbFpVemtXSiJ9.eyJpc3MiOiJodHRwczovL2Rldi1kbHRlcTBiMzR5eGJsbmRvLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2Njc0NzVmMmUzNzYzNGVjMjFkMTA5YTUiLCJhdWQiOiJjYXBzdG9uZSIsImlhdCI6MTcxOTYyOTcxNSwiZXhwIjoxNzE5NjM2OTE1LCJzY29wZSI6IiIsImF6cCI6ImRMVDJSajc5RkhlcDNkNWRzamkzOTN6eHFVM0RLRHpYIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9yIiwiZGVsZXRlOm1vdmllIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRoOmFjdG9ycyIsInBhdGg6bW92aWUiLCJwb3N0OmFjdG9yIiwicG9zdDptb3ZpZSJdfQ.giN_T3na02dwUeZvMcK-1wOF3YygRzzqzefSH9wkMvXQnOs2mK00CYzOAuGgGEXhbiwrMxSnjvtgay6ky2qwwQw-gUky3LfTHtIBC52bvpvxpudB8EDMMlKX__kZyy5wYJc4CwR9SFb_OMMGC4EnpYG_fYWru_5rd0rbaZc3Ro1u01Uv8TK6iBM4HxA34EHW-22I5UTOhPaNC1aXsRxJVpbzA0J8E7sIFHWPd_OG4sXrbLWmwjYN1K5oi9tK2bLLW3yEzp8BYb5s_of1fWAwWPX7sKuZRNB4EaVdu5D4NVsdMg7HO7BrM2tmC6xJvoCIoIVM9QRDQ-AUgEc5ZBZPIw'
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
        res = self.client().patch("/actor/1", json=new_actor, headers=header_obj)
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
        res = self.client().patch("/movie/1", json=new_movie,headers=header_obj)
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
