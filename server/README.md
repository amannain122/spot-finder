# Spot Finder Server / Backend

## Tech Stack

- Django, Django Rest Framework

## To Run the application

```bash
virtualenv venv
venv\Scripts\activate
pip install -r requirements.txt
```

```bash
python manage.py makemigrations
python manage.py makemigrations api
python manage.py migrate
python manage.py runserver
```

## Create Super user for Admin

```bash
python manage.py createsuperuser
docker-compose up --build -d

```
