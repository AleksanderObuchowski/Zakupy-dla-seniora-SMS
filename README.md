# zakupy-dla-seniora-backend
## App configuration
### Make config file
Application is using __config.py__ file for flack variables initialization (like database connection string). 
This file should be placed in _/src/config.py_ and should be defined as follows:   
```python
class Config:
    pass
```
### Create virtual environment
You should use venv to develop this application. To start virtual environment for this project make sure you are in root folder 
of `zakupy-dla-seniora` and use command `python3 -m venv venv`. Then use `source venv/bin/activate` to activate your virtual environment.   
### Install requirements
When you already have your virtual environment activated use `pip3 install -r requirements.txt` to install all dependencies.
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
Open this file and in `create_app` function add following lines:
```python
from zakupy_dla_seniora.your_module_name.routes import your_module_name
app.register_blueprint(your_module_name)
```
### Adding models
If your module needs to store information in database, you need to consider creating `models.py` file inside it. 
The file should have following template for MongoDB:   
```python
from zakupy_dla_seniora import mongo_db

class Your_Model_Name(mongo_db.Document):
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