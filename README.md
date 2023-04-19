# image-processing-server
Server for image processing.

### Local Setup

```console
py -m venv env
```
Edit pyconfig in env to use python 3.10

*Note: requirements command here?
still had to install manually
-django, djangorestframework, matplotlib, imutils, scipy, 
celery, opencv-python, rembg, firebase_admin
*

```console
env/Scripts/activate
cd src
py manage.py makemigrations
py manage.py migrate
py manage.py createsuperuser
```

Enter user info

```console
py manage.py runserver
```

Use `pip` to install your development dependencies.

```console
python3 -m pip install -r requirements/requirements.txt
```
Celery scheduling
```
celery -A src worker --loglevel=INFO
celery -A src beat --loglevel=INFO
```
