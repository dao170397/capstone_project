Casting Agency Project
-----

# Motivation for the project
The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process.

# Database Setup
```bash
    create database capstone;
    psql -U postgres -d capstone -f capstone_dump.sql
```
# Database test setup
```bash
    create database capstone_test;
    psql -U postgres -d capstone_test -f capstone_dump.sql
```
# Create a virtual environment
```bash
    python3 -m venv myvenv
    myvenv\Scripts\activate
```

# Installing Dependencies
```bash
    pip3 install -r requirements.txt
```
# Run project on local
    ```bash
    python3 app.py
    ```
You can run end point with [Postman](https://getpostman.com).
Login with the account and password in 'Setup Auth0' part
You will get the token from the link after you log in. Then use the token to run each endpoint

# Running test on local

Login with the account and password in 'Setup Auth0' part
You will get the token from the link after you log in. Then replace the token into the following line code in test_app.py
    export ASSISTANT='Bearer <your token>'
    export DIRECTOR='Bearer <your token>'
    export PRODUCER='Bearer <your token>'
Then:
```bash
    python3 test_app.py
```


# Setup Auth0

Link login: https://dev-dlteq0b34yxblndo.us.auth0.com/authorize?audience=capstone&response_type=token&client_id=dLT2Rj79FHep3d5dsji393zxqU3DKDzX&redirect_uri=http://192.168.1.101:8080

## Casting Assistant: Can view actors and movies
- Account: assistant@outlook.com
- Pass: assistant@123
- Permission 
   + "get:actors"
   + "get:movies"
## Casting Director:
All permissions a Casting Assistant has and…
Add or delete an actor from the database
Modify actors or movies
- Account: director@outlook.com
- Pass director@123
- Permission 
   + "get:actors"
   + "get:movies"
   + "delete:actor"
   + "path:actors"
   + "path:movie"
   + "post:actor"
## Executive Producer:
All permissions a Casting Director has and…
Add or delete a movie from the database
- Account: producer@outlook.com
- Pass: producer@123
- Permission 
   + "get:actors"
   + "get:movies"
   + "delete:actor"
   + "delete:movie"
   + "path:actors"
   + "path:movie"
   + "post:actor"
   + "post:movie"
# My Application 

    https://capstone-2024-d432697adb92.herokuapp.com/

# API Document
Replace {INSERT_TOKEN_HERE} to your token to test
## Error handling
    Error return as JSON format like
        {
        "error": 401,
        "message": "Token expired.",
        "success": false
        }
    The Api will return error when request fail, There are some types of error
     400: Bad request
     404: Not found
     422: Unprocessable
     403: Permission not found.
     401: Unauthorized
## End point
### GET/actors
- Return all actors, total actors and a success value.
- Sample curl: 
    curl -i -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" http://192.168.1.101:5000/actors 
- Sample response output:
    {
    "actors": [
        {
            "age": 61,
            "gender": "M",
            "id": 2,
            "movie_id": 1,
            "name": "Tom Cruise"
        }
    ],
    "success": true,
    "total_actors": 1
    }

### GET/movies
- Return all movies, total movies, and all actors of movie and a success value.
- Sample curl: 
    curl -i -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" http://192.168.1.101:5000/movies 
- Sample response output:
    {
    "movies": [
        {
            "actors": [
                {
                    "age": 61,
                    "gender": "M",
                    "id": 2,
                    "movie_id": 1,
                    "name": "Tom Cruise"
                },
                {
                    "age": 61,
                    "gender": "M",
                    "id": 3,
                    "movie_id": 1,
                    "name": "Tom Cruise"
                }
            ],
            "id": 1,
            "releaseDate": "Sat, 08 Jan 2022 17:00:00 GMT",
            "title": "New Movie"
        }
    ],
    "success": true,
    "total_movies": 1
    }

### POST/actors
- Create a new actor
- Sample curl:
    curl -L "http://192.168.1.101:5000/actors/" -X POST -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" -d "{\"name\":\"Emma Watson\", \"age\": 34, \"gender\": \"F\"}"
- Sample response output:
    {
        "success": true
    }

### POST/movies
- Create a new movie
- Sample curl:
    curl -L "http://192.168.1.101:5000/movies/" -X POST -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" -d "{\"title\":\"Little women\", \"releaseDate\": \"10/10/2019\"}"
- Sample response output:
    {
    "success": true
    }

### PATCH/movies/<id>
- Update a movie by movie_id
- Sample curl:
    curl "http://192.168.1.101:5000/movies/1" -X PATCH -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" -d "{\"title\":\"New Movie\",\"releaseDate\": \"10/10/2019\"}"
- Sample response output:
    {
  "movie": {
    "actors": [],
    "id": 1,
    "releaseDate": "10/10/2019",
    "title": "New Movie"
  },
  "success": true
    }
    

### PATCH/actors/<id>
- Update a actor by actor_id
- Sample curl:
    curl "http://192.168.1.101:5000/actors/1" -X PATCH -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" -d "{"name":"New Actor","age":"62","gender":"M", "movie_id":1}"
- Sample response output:
    {
    "actor": {
        "age": 62,
        "gender": "M",
        "id": 2,
        "movie_id": 1,
        "name": "New Actor"
    },
    "success": true
    }

### DELETE/movies/<id>
- Delete a movie by movie_id
- Sample curl:
    curl "http://192.168.1.101:5000/movies/1" -X DELETE -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" 
- Sample response output:
    {
    "deleted": 1,
    "success": true
}

### DELETE/actors/<id>
- Delete a new actor by actor_id
- Sample curl:
    curl "http://192.168.1.101:5000/actors/1" -X DELETE -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}"
- Sample response output:
    {
    "deleted": 1,
    "success": true
}
