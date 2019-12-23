# Maible EventMan
Event Manager application

Django 3.0.1 / Python 3.8

# Install
* Virtual environment: `virtualenv venv -p python3` and activate: `source venv/bin/activate`
* Dependencies: `pip install -r requirements.txt`
* Settings file: `cp local_settings.template.py local_settings.py` (update values in the file)
* Static files: `python manage.py collectstatic`
* Staff user (for admin): `python manage.py createsuperuser`
* Run the application: `python manage.py runserver`
