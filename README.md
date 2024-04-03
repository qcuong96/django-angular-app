# Demo app

## APP infomation
- APP name: Demo app
- APP version: v0.0.0
- APP description: This demo app using for practice Django REST framework and AngularTS

## APP technologies
- Backend: Python 3.10, Django 4.2, Django REST framework 3.15
- Frontend: Angular 17, Node 20
- Database: PostgreSQL 14.11
- Deployment: Docker, Docker-compose

## APP features
- User authentication
- Create ticket
- Reply ticket
- Close ticket
- Delete ticket

## APP setup
### 1. Clone project
```bash
git clone https://github.com/pre-commit/demo-repo.git
```

### 2. Run project
#### a. Run with docker-compose
```bash
docker-compose up -d
``` 
#### b. Run with local
```bash
# Create postgres database
chmod +x start.sh
./start.sh -d <dbname> -u <username> -p <password>

# Run backend
cd django-rest
pipenv install
pipenv shell
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver

# Run frontend
cd web-app
npm install
ng serve
```

You need to update some config files to make app work on your local machine:
- web-app/angular.json
- web-app/src/environments/environment.ts
- django-rest/config/local.py

## APP usage
- Open browser and access to http://localhost:4200
- Register new account
- Tick to box employee if want to create employee account
- Normal user can create, view, reply, close and delete own ticket
- Employee can view all tickets
- Employee can assign ticket to self if ticket is not assigned
- Employee can reply and close ticket which he/she assigned

## Notes
- This application need some ports to run:
    - 35432: PostgreSQL
    - 8080: Django REST framework
    - 4200: Angular

- You can run test for backend by command:
```bash
# setup database
docker-compose up postgres -d

# run test
cd django-rest
pipenv install
pipenv shell
pipenv install --dev
python3 manage.py test --parallel --testrunner django.test.runner.DiscoverRunner

# down database
docker-compose down
```
## Issue found
### 1. Error when run on windowns: /usr/bin/env: ‘python \r’: No such file or directory
- Open powershell
```base
cd django-rest
(Get-Content -Path manage.py -Raw).Replace("`r`n", "`n") | Set-Content -Path manage_unix.py -NoNewline
```
- Change manage.py to manage_unix.py in file docker-compose.yml
- Change mange.py to manage_unix.py when run related command

## Contact
Help any problem, please contact me via email: quangcuong.nguyen96@gmail.com