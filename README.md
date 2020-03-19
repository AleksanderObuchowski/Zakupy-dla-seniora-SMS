# zakupy-dla-seniora-backend

## App configuration

### Install mysql
To install mysql follow instructions of this site:
[How to install mysql on ubuntu](https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-18-04)
Then you need to create database and user for the app. If you are not in the mysql shell use `sudo mysql` to enter mysql command line.
Next run    `CREATE DATABASE zakupy_dla_seniora_db`   And then you need to create new user by running   
`CREATE USER 'artifai'@'localhost' IDENTIFIED WITH mysql_native_password BY 'your_password';`   
with your password.
Finally, grant your user privileges to run queries on created database:   
`GRANT ALL PRIVILEGES ON zakupy_dla_seniora_db.* TO 'artifai'@'localhost';`

### Make config file
Application is using __config.py__ file for flack variables initialization (like database connection string). 
This file should be placed in `/src/zakupy_dla_seniora/config.py` and should be defined as follows:

```python
from secrets import token_hex

mysql_user_name = 'artifai'
mysql_user_password = ''  # put your mysql artifai user password
mysql_server = 'localhost'
mysql_database = 'zakupy_dla_seniora_db'

twilio_sid = 'AC5afa0c6a9be65fade4dc61ae23169dc7'  # put your twilio sid
twilio_auth_token = '3ab51dd71c656bec8f0dabeccede044d'  # put your twilio auth_token

class Config:
    SECRET_KEY = token_hex(16)#  '' # put your secret key
    SQLALCHEMY_DATABASE_URI = f'mysql://{mysql_user_name}:{mysql_user_password}@{mysql_server}/{mysql_database}'
```

### Generate your secret key
To generate your secret key run python shell with `python3` command and then `import secrets`.   
Then type `secrets.token_hex(16)` and hit enter. Now copy your secret key and paste it into `config.py`file as `SECRET_KEY`.

### Create virtual environment
You should use venv to develop this application. To start virtual environment for this project make sure you are in root folder
of `zakupy-dla-seniora` and use command `python3 -m venv venv`. Then use `source venv/bin/activate` to activate your virtual environment.

### Install requirements
When you already have your virtual environment activated use `pip3 install -r requirements.txt` to install all dependencies.

### For Mac OS
You should paste it in terminal for exporting dynamic library to avoid error (*..darwin..*) : 'export DYLD_LIBRARY_PATH=/usr/local/mysql/lib/:$DYLD_LIBRARY_PATH'

### Run app
Now to run the app navigate to `/src/` and use command `python3 run.py`

## App development

### Add new module
To create new module, create new folder in path `/src/zakupy_dla_seniora/`. Folder name is your module name. Now initialize
your new module by creating `__init__.py` file inside it.

### Adding routes
To define routes for your module create new file inside it named `routes.py`. The file template, containing all necessary code goes as:   
```python
from flask import Blueprint

your_module_name = Blueprint('your_module_name', __name__)

@your_module_name.route('/')
def function_name():
    return "<h1>Hello</h1>"
```
Now you need to register your routes blueprint in `/src/zakupy_dla_seniora/__init__.py` file.
Open this file and in `register_blueprints` function add following lines:
```python
from zakupy_dla_seniora.your_module_name.routes import your_module_name
app.register_blueprint(your_module_name)
```

### Adding resources
```python
from flask_restful import Resource

class YourResourceName(Resource):
    def http_method(self):  # probably post() or get()
        return {'success': True, 'other_data': data}
```
Now you need to register your resource in `src/zakupy_dla_seniora/__init__.py` file.
Open this file and in `register_api_resources` function add following lines:
```python
from zakupy_dla_seniora.your_module_name.resources import YourResourceName
api.add_resource(YourResourceName, '/path/to/your/resource')
```

### Adding models
If your module needs to store information in database, you need to consider creating `models.py` file inside it.
```python
from zakupy_dla_seniora import mysql_db

class Your_Model_Name(mysql_db.Model):
    # Your fields definitions
```

### Adding more functions
If you need to define more functions for your module, you can create `functions.py` file containing your functions definitions.
The file should look like:
```python
# imports section

def function_name_1():
    # stuff

def function_name_2():
    # stuff
```

## Features

### Users

##### Model Fields

|id|name|first_name|last_name|password_hash|create_date|phone|verification_code|verified|points|
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
|int|varchar|varchar|varchar|varchar|datetime|varchar|int|bool|int|


##### Endpoints
- POST: `/register`
    - params:

        |name|first_name|last_name|password|phone|
        |:---:|:---:|:---:|:---:|:---:|
        |string|string|string|string|string|string|

    - answer:

        |success|message|
        |:---:|:---:
        |boolean|string|

### SMS Code Verification

##### Endpoints
- POST: `/send_code`
    - params: phone (string)
    - answer:

        |success|code|number|
        |:---:|:---:|:---:|
        |boolean|int|string|

- POST: `/check_code`
    - params: phone (string), code (int)
    - answer:

        |success|message|
        |:---:|:---:
        |boolean|string|


