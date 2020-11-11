# django-restframework-with-jwt

Below are the step by step process to setup this project

Step-1: First clone this project

Step-2: Install below dependencies

pip install django==3.1

pip install djangorestframework==3.12.2

pip install mysqlclient

pip install djangorestframework_simplejwt

Step-3: For intial databse setup

Step-4: create database

Step-5: add database details in settings file.

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dbname',
        'USER': 'username',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

step-6: move to wallet project

step-7: python manage.py makemigrations

step-8: python manage.py migrate

step-9: python manage.py runserver

Below are the apis detail of this project:

1. Api token

POST localhost:8000/api/token/
request body:{
	"username": "username",
	"password": "password"
}

response:{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYwNTI0NzkwMSwianRpIjoiNTk5MjlkZmI4MGYyNDU2MDgyNThjYWFiN2UzMWE3ZWYiLCJ1c2VyX2lkIjoxfQ.RUX6kLCH4EacnBBjLKFgqxZJ1Sqv8BCEy4A4GPFqqh0",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjA1MTYxNTAxLCJqdGkiOiIyZDdlY2Y2MzA2YmQ0YTdlYWQ2MTcwZjQyZjkxM2JlYSIsInVzZXJfaWQiOjF9.jsqmsuv63h8WiQ7O14uQeEkI-rvqZJhKZjfFJWd1kN8"
}


2.get  current balance

header{
Authorization: Bearer token
Content-Type: "application/json"
}

GET localhost:8000/wallet/money
Response:{
    "current_balance": 50



3. Add Balance to Wallet

header{
Authorization: Bearer token
Content-Type: "application/json"
}

request body:{
	"amount":50
}

Response:{
    "message": "added successfully",
    "current_balance": 50
    }
    
4. Pay to other user wallet

POST: localhost:8000/wallet/pay/

header{
Authorization: Bearer token
Content-Type: "application/json"
}

request:{
	"amount":50,
	"user":2
}

response:{
    "message": "send successfully",
    "current_balance": 0
}

5. All transcation of current user

GET: localhost:8000/wallet/transcations/

header{
Authorization: Bearer token
Content-Type: "application/json"
}

response:{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "wallet": 1,
            "txntype": true,
            "txnamount": 50,
            "user_to": null,
            "user_from": null,
            "addSource": "CC/DC/NB",
            "txndate": "2020-11-11T06:35:39.532008Z"
        },
        {
            "id": 2,
            "wallet": 1,
            "txntype": false,
            "txnamount": 50,
            "user_to": null,
            "user_from": null,
            "addSource": "",
            "txndate": "2020-11-11T07:14:37.104421Z"
        }
    ]
}

5. get total creadited and debiated  amount of current user

GET localhost:8000/wallet/userwallet/

header{
Authorization: Bearer token
Content-Type: "application/json"
}

response:{
    "walletId": 1,
    "username": "prahlad",
    "current_balance": 0,
    "amount_added": 50,
    "amount_paid": 50
}
