# image-processing-server v1.0.0
Server for sand image processing.
# The current version(v1.0.0) is not configured for production instances
## What's missing?
- Production configuration of settings.py
- WSGI configuration if using different WSGI server
- Configuration related to chosen production environment

## TEST

### Linux Installtion of Server Files
May require knowledge of pip and apt-get to ensure dependencies are met.
**REQUIRES PYTHON VERSION [3.9, 3.10]**
Requires redis

Virtual Environment Setup
```console
python3 -m venv env
. env/Scripts/activate
```

Use `pip` to install your development dependencies. Note opencv-python is recommended to be installed first to ensure proper installation
```console
pip install opencv-python
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

Running the server

```console
python3 manage.py runserver
```

Celery scheduling
How to start celery workers/beat.
```console
celery -A config worker --loglevel=INFO
celery -A config beat --loglevel=INFO
```

## AWS Instance Information
Redis can be installed within the AWS instance this server is installed on. This removes the need for additional AWS configurations(MemoryDB or ElastiCache). Given the opportunity, it is best practice to isolate the main server instance using services.

The server also requires a higher compute instance utilizing a graphics processing unit (GPU). The recommended instance is an AWS Accelerated Computing instance (P3), though this is untested.

Depending on use case, it is recommended to run on a local machine if cost is an issue. If this is taken as an option, the local machine running the server instance must must be configured with the UTD Office of Information Technology to properly route requests to the local machine on UTD WiFi.

### Locally installing Redis
Should Redis be run on the same instance as the Django server, this link can be used for installation
https://redis.io/docs/getting-started/installation/install-redis-on-linux/

The default configuration uses port: 6379 on local host (127.0.0.1). Should the Redis server be installed in another instance, the Redis configuration file needs to be updated with the routing information provided by AWS MemoryDB or ElastiCache.

## Configuring Django for Deployment
Follow the guidelines outlined by Django Documentation for deployment guidelines.
https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

Additional configurations my include the use of different WSGI servers such as Gunicorn with NGINX. These resources offer additional benefits but require their own configurations to work with the Django server.
