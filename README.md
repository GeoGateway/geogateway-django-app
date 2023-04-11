# geogateway-django-app

## Setting up the development environment

You will need Python 3.6.2 or later for this installation. 
This assumes you have the airavata-django-portal repo cloned and the development environment setup. 
Instructions are provided here: https://github.com/apache/airavata-django-portal. Complete this installation before following the instructions below. 
Assume this is done in $HOME/airavata-django-portal. 

After you have installed the Airavata Django Portal, install the GeoGateway Django App with the following steps. 

1. Open two terminal windows. 
2. In Terminal #1, clone this repo under $HOME, creating the directory $HOME/geogateway-django-app. 

2. In Terminal #1, install dependencies and build frontend code for the Geogateway Django App:
   * ```cd $HOME/geogateway-django-app/frontend```
   * ```yarn install```
3. In Terminal #2, activate the virtual environment 
   * ```cd $HOME/airavata-django-portal``` 
   * ```source venv/bin/activate``` 
4. In Terminal #2, install the Geogateway Django App in develop mode into the Django portal
   * ```cd $HOME/geogateway-django-app```
   * ```python setup.py develop```
4. In Terminal #2, run Airavata Django Portal Server
   * ```cd $HOME/airavata-django-portal```
   * ```python manage.py runserver```
6. In Terminal #1, run: ``` yarn serve ``` 
7. Point your browser to http://localhost:8000/geogateway_django_app/

## node version
nvm install lts/fermium
v14 is supported, not able to run with latest lts version v18.15 