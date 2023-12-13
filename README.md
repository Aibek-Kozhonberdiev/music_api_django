# MUSIC API DJANGO :musical_note:
___
![Python version](https://img.shields.io/badge/python-v3.11.3-blue?logo=python)
![PyPI - Django](https://img.shields.io/pypi/pyversions/django?logo=django&link=https%3A%2F%2Fdocs.djangoproject.com%2Fen%2F5.0%2F)
![PyPI - Google auth](https://img.shields.io/pypi/pyversions/google-auth?logo=google&link=https%3A%2F%2Fpypi.org%2Fproject%2Fgoogle-auth%2F2.0.1%2F)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-v15.4-blue?logo=postgresql&link=https%3A%2F%2Fwww.postgresql.org%2Fdocs%2Frelease%2F15.4%2F)
![PyPI - Rest Framework](https://img.shields.io/pypi/pyversions/djangorestframework?logo=django&color=gren&link=https%3A%2F%2Fpypi.org%2Fproject%2Fdjangorestframework%2F)

## Application functionality :bulb:
+ User:
  + Authorization via Google
  + Adding favorites
  + Password recovery via gmail
  + Sending a welcome message to gmail after authorization
+ Music:
  + Listening installation and view counter
  + Create a category(via admin)
+ Broadcasting:
  + Installing, listen and view counter for a podcast
+ Base:
  + Gmail functions
  + Path media(img, music file)
  + Default image for user profile
  
## History of changes :page_facing_up:

- **1.0.0** (2023-12-11)
  - First release of the project
  - Added basic functions
  
## Requirements 
+ Python (>=3.10, <3.12)
+ Django (5.0)
+ Djangorestframework (3.14.0)
+ Djangorestframework-simplejwt (5.3.0)
+ Psycopg2 (2.9.8)
+ Python-dotenv (1.0.0)
+ Drf-yasg (1.21.7)
+ Django-cors-headers (4.3.1)
+ Requests (2.31.0)
+ PostgreSql (15.4)

## Installation :computer:
```bash
git clone https://github.com/Aibek-Kozhonberdiev/music_api_django.git
```
```bash
python -m venv venv && source venv/bin/activate
```
```bash
pip install -r requirements.txt
```
+ You need to enter these values into the `.env` file :key: :
```.env
# Django
SECRET_KEY=
DEBUG=True
MY_HOST=

# Email
EMAIL_USE_TLS=True
EMAIL_HOST='smtp.gmail.com'
EMAIL_PORT=587
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=

# Google auth
GOOGLE_CLIENT_ID=''
GOOGLE_SECRET_KEY=''

# Swagger
DOCS_EMAIL='#'
DOCS_LICENSE='#'
DOCS_TERMS_OF_SERVISE='#'

# PostgreSQL
DB_NAME=postgres
USERNAME=postgres
PASSWORD=postgres
SERVER=dm_db
PORT=5432
```
+ If you want to use postgresql, you need to change the `DATABASES` value in the `settings.py` file to the following:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('DB_NAME', os.getenv('USERNAME')),
        'USER': os.getenv('USERNAME'),
        'PASSWORD': os.getenv('PASSWORD'),
        'HOST': os.getenv('SERVER'),
        'PORT': os.getenv('PORT'),
    }
}
```

## Docker :whale:

+ Launching a docker container:
```bash
docker-compose build
```
+ Launch of the project:
```bash
docker-compose up
```
