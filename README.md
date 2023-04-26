# image-processing-server
Server for image processing.

### Local Setup (Linux)
**REQUIRES PYTHON VERSION [3.9, 3.10]**
Requires redis server

Virtual Environment Setup
```console
python3 -m venv env
. env/Scripts/activate
```

Install dependencies
```console
python3 -m pip install -r requirements/requirements.txt
```

Make migrations
```console
cd src
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py createsuperuser
```

Enter user info

```console
python3 manage.py runserver
```

Use `pip` to install your development dependencies.

Celery scheduling
```
celery -A config worker --loglevel=INFO
celery -A config beat --loglevel=INFO
```
