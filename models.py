
import os
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from flask_sqlalchemy import SQLAlchemy
import json
from flask_migrate import Migrate

database_path = os.environ['DATABASE_URL']
if database_path.startswith("postgres://"):
  database_path = database_path.replace("postgres://", "postgresql://", 1)

db = SQLAlchemy()

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)
    with app.app_context():
        db.create_all()

class inheritedClassName(db.Model):
    __abstract__ = True

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()


class Movie(inheritedClassName):
    id:int
    title:String
    releaseDate:DateTime
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String,nullable=False)
    releaseDate = Column(DateTime)
    actors = db.relationship('Actor', backref="movie", lazy=True)

    def __init__(self, title, releaseDate):
        self.title = title
        self.releaseDate = releaseDate

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'releaseDate': self.releaseDate,
            'actors':[actor.format() for actor in self.actors]
            }

class Actor(inheritedClassName):
    id:int
    name:String
    age:int
    gender:String
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    name = Column(String,nullable=False)
    age = Column(Integer)
    gender=Column(String)
    movie_id = Column(Integer, ForeignKey('movies.id'), nullable=True)


    def __init__(self, name, age, gender, movie_id):
        self.name = name
        self.age = age
        self.gender = gender
        self.movie_id = movie_id


    def format(self):
        return {
            'id' : self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'movie_id':self.movie_id
            }
