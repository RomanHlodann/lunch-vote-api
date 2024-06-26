# Lunch Vote Api

Internal service for its employees which helps them to make a decision at the lunch place.
Each restaurant will upload menus using the system every day over API.
You can see images of menus or dishes and choose what place you`d like to eat with you colleagues.

## Installing using GitHub
    
```bash
git clone https://github.com/RomanHlodann/lunch-vote-api.git
cd lunch-vote-api
python -m venv venv
On mac: source venv/bin/activate Windows: venv/Scripts/activate
pip install -r requirements.txt
set DB_HOST=<your db hostname>
set DB_NAME=<your db name>
set DB_USER=<your db user>
set PASSWORD=<your db user password>
set SECRET_KEY=<your secret key>
set PGDATA=<PGDATA>
python manage.py migrate
python manage.py runserver
```

## Run with Docker
To run the project with Docker, follow these steps:

```bash
docker-compose up
```

## Features
* JWT authenticated
* Documentation is located at `/api/doc/swagger-ui/`
* Docker
* Postgresql
* Managing votes
* Managing menu or dishes images
* Filtering menus, votes
* Email as a username

## Access the API endpoints via 
`http://localhost:8000/`
* **Restaurants** `api/restaurant/all/`
* **Menus** `api/restaurant/menus/`
* **Vote** `api/votes/`

To operate with tokens:
* **Get tokens** `api/users/token/`
* **Refresh token** `api/users/token/refresh/`
* **Verify token** `api/users/token/verify/`
* **Register** `api/users/register/`
* **Get profile** `api/users/me/`
