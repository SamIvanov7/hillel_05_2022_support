
# Project: Support application

Online support service for users which organizes quick and comfortable connection 
specialists of service with users issues.

## Setup the Environment
#### Install pipenv

```
$pip instal pipenv
```

## Description 

#### Authentication
- Have the panel of administration with database of users. Can sign up, sign in/out. 
Also in app can assign to role of user. 

#### Core
- Tickets - can work with tickets of users requests. App have a database of a tickets.
- Comments - can work with comments of users. App have a database of comments to the tickets.
- Exchange Rate - app can doing request for updating of currency rate and make to respose in json format. 
App can save information in history file and make output respose in json format from request.

#### Shared
- contains the necessary models that each module of our project refers to. But module "shared" will never refers to any of our project's modules


## Files description:

1. #### hillel_05_2022_support 
 - folder which contains our site(project)


2. #### hillel_05_2022_support/.github/workflows/ci.yaml 
 - github action/code intelligence file for our project

3. #### hillel_05_2022_support/config 
 - “key”-folder of our project that includes:
	- settings.py - contains all project settings. Here we register applications, set the location of static files, database settings, and so on.
	- urls.py - sets associations of url-addresses with views. Although this file may contain all the url-settings, it is usually divided into parts, one per application
	- asgi.py - entry point for ASGI-compatible web servers serving the project (required for deployment to a public site)
	- wsgi.py - used to establish communication between a Django application and a web server. We use it like an utility
	- __init__.py - an empty file as default, so that Django and Python recognize the folder as a Python module and allow us to use its objects inside other parts of the project.

4. #### /hillel_05_2022_support/manage.py 
- script for managing our project, created by the django-admin command. used to build applications, work with databases, and to run or debug-run the server.

5. #### /hillel_05_2022_support/Pipfile 
- is the dedicated file used by the Pipenv virtual environment to manage project dependencies

6. #### /hillel_05_2022_support/Pipfile.lock 
- is intended to specify, based on the packages present in Pipfile, which specific version of those should be used, avoiding the risks of automatically upgrading packages that depend upon each other and breaking our project dependency tree

7. #### /hillel_05_2022_support/.flake8  
-  Flake8 config file

8. #### /hillel_05_2022_support/requirements.txt 
 - requirements of our project, which are used for correctly working workflowfile and code-intelligence

9. #### /hillel_05_2022_support/.gitignore
 - GitHub ignore file

10. #### migration/ 
- referred to here as “migration files”. These files are actually normal Python files with an agreed-upon object layout, written in a declarative style. What Django looks for when it loads a migration file (as a Python module) is a subclass of django.db.migrations.Migration called Migration. It then inspects this object for four attributes, only two of which are used most of the time:
    • dependencies, a list of migrations this one depends on. 
    • operations, a list of Operation classes that define what this migration does. 
The operations are the key; they are a set of declarative instructions which tell Django what schema changes need to be made. Django scans them and builds an in-memory representation of all of the schema changes to all apps, and uses this to generate the SQL which makes the schema changes.
That in-memory structure is also used to work out what the differences are between your models and the current state of your migrations; Django runs through all the changes, in order, on an in-memory set of models to come up with the state of your models last time you run makemigrations. It then uses these models to compare against the ones in your models.py files to work out what you have changed.

11. #### /models.py 
 - central element, that contains our project’s models. Django model typically refers to a table in the database, attributes of that model becomes the column of that table. In more of a real-world example, we would create a model for any entity in our application, and store its attributes with django fields which automatically handles data-types conversions for the database we would be using.

12. #### /apps.py 
 - Application information definition file. It creates an AppConfig class that is used to define metadata such as the name of the application.

13. #### /admin.py 
- The management site model declaration file, used for registration of model in our panel, which is empty by default.

14. #### /tests.py 
- Used to check code files.

15. #### /views.py 
- Define a URL response function here.
