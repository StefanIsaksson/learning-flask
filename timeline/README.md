# Flask
Examples of trying out the micro web framework to build a simple web page.

## Setting up a new virtualenv with Flask

### Install virtualenv (if not already installed)

`pip install virtualenv`

`pip install virtualenvwrapper-win`

### Creating new virtualenv for learning-flask project

`mkvirtualenv learning-flask`

`cd learning-flask`

`setprojectdir .`

`pip install Flask`

Project uses flask-sqlalchemy for persistence, to install package write:

`pip install flask flask-sqlalchemy`

### Enter and Exit the project environment

`deactivate` leaves the project environment

`workon learning-flask` switches to project environment

### Create database
Run `create_db.py` to create database tables

## Start web app

`python app.py`

OR

`set FLASK_APP=app.py`
`flask run`