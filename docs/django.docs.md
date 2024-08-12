# Project Setup

Only after when you install python first time in your PC
    
    pip install pipenv

## To Create a new project with pipenv 

Create a project folder (Project Name) inside that folder Run
```bash
pipenv install django
```    

+ This will create the pip-file and pip-lock file.
+ config your IDE or use below commands 

+ Sub Commands to help you to  
    +   ```bash
        pipenv shell //(Activate pipenv)      
        pipenv --venv //(path to pipenv) 
        ```    

## To Create new pipenv in Existing Project
Simply Run this command in the Project Folder
```bash
pipenv install
```
+ This will create a new env for you project and Auto install pages
+ you can now config the path to you IDE


## To Create a Django-Project 
```bash
django-admin startproject --projectName-- .
```    

## To Create a App In You Django-Project
```bash
python manage.py startapp --appName--
python manage.py startapp --appName-- --settings=project.settings-dev
```
+ Don't forgot to register the app in the project

<br>
<br>

# Migrations commands

## To Create Migrations
```bash
python manage.py makemigrations
```
## To Apply Migrations
```bash
python manage.py migrate
```
## Rollback Migrations 
```bash
python manage.py migrate --app_name-- --migration_file_prefix--

```

# Static storage

```bash
python manage.py collectstatic
```