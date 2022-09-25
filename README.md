
# Project: Support application
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pw?label=Python%20)![PyPI](https://img.shields.io/pypi/v/django?color=919&label=Django)![GitHub Workflow Status](https://img.shields.io/github/workflow/status/SamIvanov7/hillel_05_2022_support/pre-commit-action)

Online support service for users which organizes quick and comfortable connection 
specialists of service with users issues.

## Setup the Environment
#### Install pipenv

```bash
$pip install pipenv
```

#### Install [pre-commit hooks](https://pre-commit.com/#install)
> Note: Install pre-commit tool before
```bash
pre-commit install
```
## Run application with Docker

```bash
docker build -t support_django . -f Dockerfile
docker run -p 8000:80 -v $PWD:/app/ --rm -it support_django
```
## Run application with Docker-compose
```bash
docker compose build
docker compose up -d
```
## Dump postgress DB
```bash
docker compose exec postgres pg_dump -U support support > db-backup-$(date +%d-%m-%y).sql
```
## Load postgress DB
```bash
docker compose exec -T postgres psql -U support support < db-backup-25-09-22.sql
```
You have to change db-backup-25-09-22.sql to your current DB dump file name

# Description

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


##### Other utilits

Pipfile - this file contains information for the dependencies of the project. Pipenv uses this file to define all required tools, utils, and modules for this env. Here we separate dev packages and default so that we can use this file for dev and prod.

Pipfile.lock - This file declares all dependencies (from Pipfile) of the project, their latest available versions, and the current hashes for the downloaded files.

.isort.cfg - we use this file to configure isort behavior. In my case, I exclude migrations from the checking.

.flake8 - we use this file to configure flake8 behavior.

.gitignore - here we specifie files that git shoud ignore.


## Files description:

#### hillel_05_2022_support 
 - folder which contains our site(project)


#### hillel_05_2022_support/.github/workflows/ci.yaml 
 - github action/code intelligence file for our project

#### hillel_05_2022_support/config 
 - “key”-folder of our project that includes:
	- settings.py - contains all project settings. Here we register applications, set the location of static files, database settings, and so on.
	- urls.py - sets associations of url-addresses with views. Although this file may contain all the url-settings, it is usually divided into parts, one per application
	- asgi.py - entry point for ASGI-compatible web servers serving the project (required for deployment to a public site)
	- wsgi.py - used to establish communication between a Django application and a web server. We use it like an utility
	- __init__.py - an empty file as default, so that Django and Python recognize the folder as a Python module and allow us to use its objects inside other parts of the project.

#### /hillel_05_2022_support/manage.py 
- script for managing our project, created by the django-admin command. used to build applications, work with databases, and to run or debug-run the server.

#### /hillel_05_2022_support/Pipfile 
- is the dedicated file used by the Pipenv virtual environment to manage project dependencies

#### /hillel_05_2022_support/Pipfile.lock 
- is intended to specify, based on the packages present in Pipfile, which specific version of those should be used, avoiding the risks of automatically upgrading packages that depend upon each other and breaking our project dependency tree

#### /hillel_05_2022_support/.flake8  
-  Flake8 config file

#### /hillel_05_2022_support/requirements.txt 
 - requirements of our project, which are used for correctly working workflowfile and code-intelligence

#### /hillel_05_2022_support/.gitignore
 - GitHub ignore file

#### /.pre-commit-config.yaml
 - describes installed repositories and hooks

#### /.pyproject.toml
 - config file which is used for isort & black for normal working without conflicts

#### migration/ 
- referred to here as “migration files”. These files are actually normal Python files with an agreed-upon object layout, written in a declarative style. What Django looks for when it loads a migration file (as a Python module) is a subclass of django.db.migrations.Migration called Migration. It then inspects this object for four attributes, only two of which are used most of the time:
    • dependencies, a list of migrations this one depends on. 
    • operations, a list of Operation classes that define what this migration does. 
The operations are the key; they are a set of declarative instructions which tell Django what schema changes need to be made. Django scans them and builds an in-memory representation of all of the schema changes to all apps, and uses this to generate the SQL which makes the schema changes.
That in-memory structure is also used to work out what the differences are between your models and the current state of your migrations; Django runs through all the changes, in order, on an in-memory set of models to come up with the state of your models last time you run makemigrations. It then uses these models to compare against the ones in your models.py files to work out what you have changed.

#### /models.py 
 - central element, that contains our project’s models. Django model typically refers to a table in the database, attributes of that model becomes the column of that table. In more of a real-world example, we would create a model for any entity in our application, and store its attributes with django fields which automatically handles data-types conversions for the database we would be using.

#### /apps.py 
 - Application information definition file. It creates an AppConfig class that is used to define metadata such as the name of the application.

#### /admin.py 
- The management site model declaration file, used for registration of model in our panel, which is empty by default.

#### /tests.py 
- Used to check code files.

#### /views.py 
- Define a URL response function here.
