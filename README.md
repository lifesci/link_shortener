# link_shortener

## Requirements
- Python 3
- PostgreSQL

## Setup (with sample commands for linux users)

1. Navigate to project directory
2. Create `instance` folder: `mkdir instance`
3. Create `config.py` file in `instance` folder, and set `SECRET_KEY` and `SQLALCHEMY_DATABASE_URI` variables. For example
```
$ cat instance/config.py
SECRET_KEY = "<key>"
SQLALCHEMY_DATABASE_URI = "postgresql://<username>:<password>@<host>/<database>"
```
4. Create virtual environment: `python3 -m venv venv`
5. Activate virtual environment: `source venv/bin/activate`
6. Install requirements: `pip install -r requirements.txt`
7. Run application in debug mode: `flask --app app run --debug`
8. Navigate to `http://127.0.0.1:5000/` to view application
