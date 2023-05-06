# image-processing-server v1.0.0
Server for sand image processing.
# The current version(v1.0.0) is not configured for production instances
## What's missing?


### Local Setup (Linux)
**REQUIRES PYTHON VERSION [3.9, 3.10]**
Requires redis

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
How to start celery workers/beat.
```console
celery -A config worker --loglevel=INFO
celery -A config beat --loglevel=INFO
```

AWS Instance Information
