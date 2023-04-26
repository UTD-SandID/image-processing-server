# image-processing-server
Server for image processing.

### Local Setup

```console
python3 -m venv env
```
Edit pyconfig in env to use python 3.10

```console
python3 -m pip install -r requirements/requirements.txt
```

still had to install manually
-django, djangorestframework, matplotlib, imutils, scipy, 
celery, opencv-python, rembg, firebase_admin
*

```console
env/Scripts/activate
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
celery -A src worker --loglevel=INFO
celery -A src beat --loglevel=INFO
```
