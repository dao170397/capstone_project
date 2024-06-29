Casting Agency Project
-----

# Motivation for the project
The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process.

# Installing Dependencies
```bash
    pip install -r requirements.txt
```
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
# Run project on local
    ```bash
    python app.py
    ```
You can run end point with [Postman](https://getpostman.com).
Login with the account and password in 'Setup Auth0' part
You will get the token from the link after you log in. Then use the token to run each endpoint

# Running test on local

Login with the account and password in 'Setup Auth0' part
You will get the token from the link after you log in. Then replace the token into the following line code in test_app.py
    self.token_casting_assistant='Bearer <your token>'
    self.token_casting_director='Bearer <your token>'
    self.token_executive_producer='Bearer <your token>'
Then:
```bash
    python test_app.py
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



