# image-processing-server
Server for image processing.

Steps to setup virtual enviroment in Windows terminal in folder containing the project folder:
  1. Create and enable python virtual environment
  ```cmd
  py -m venv env
  env/Scripts/activate
  ```
  2. Install Django
  ```cmd
  py -m pip install Django
  ```

How to run server
  ```cmd
  py manage.py makemigrations
  py manage.py migrate
  py manage.py runserver
  ```
