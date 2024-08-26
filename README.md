# Foro de metal

Forum about heavy metal. Built with Flask, Jinja, Bootstrap and PostgreSQL

## Features

- User Session
- Create topics
- Answer topics

## Run locally

1. Clone this repository:
```
git clone https://github.com/emmariescurrena/foro-metal
```

2. Create .venv

```
python<version> -m venv .venv
```

3. Activate venv

```
source env/bin/activate
```

4. Install dependencies

```
pip install -r requirements.txt
```

5. Create database:

```
createdb foro_metal
```

6. Create .env in root directory and set variables:

```
FLASK_APP=src
SECRET_KEY = "secret_key"
SQLALCHEMY_DATABASE_URI = "postgresql://username:password@localhost:5432/foro_metal"
```

Replace `secret_key`, `username` and `password` with yours

7. Run app

```
flask --app src/__init__.py  run
```