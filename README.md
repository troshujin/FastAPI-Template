# FastAPI Template by TijmenSimons

:D

## Setup the project

`virtualenv env`

`env/scripts/activate`

`pip install -r requirements.txt`

## Run the project

`uvicorn main:app --host 0.0.0.0 --port 8000 --reload`

## Manage database

`python manage_db.py` has possible 3 arguments:

- `init`
- `delete`
- `reset`

`init` creates all tables, if they do not exist and seeds the database

`delete` deletes all tables

`reset` delete + init
