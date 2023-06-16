# Personify Service

[![Coverage Status](https://coveralls.io/repos/github/gnknithin/Personify-Service/badge.svg?branch=main)](https://coveralls.io/github/gnknithin/Personify-Service?branch=main)

## Introduction

This repo presents a proof of concept of a highly scalable Personal Server. The application was developed keeping a personal utility of an user domain in mind, but the principles used can easily applied to design software solutions for any domain. One of the primary challenges for a user application domain is the ability to expand as per requirement, giving the ability to explore more on top of exisitng. To do so, we have to architect the application that would support the scale. After understanding serveral different system architectures, a Domain-Driven Design was considered to meet the requirement. This approach holds Framework-Agnositic Design, PostgreSQL, MonogoDB and Test Driven Development.


## Development Environment

At the bare minimum you'll need the following for your development environment:

1. [Python](http://www.python.org/)
2. [PostgreSQL](https://www.postgresql.org/)
3. [MongoDB](https://www.mongodb.com/)

It is strongly recommended to also install and use the following tools:

1. [virtualenv](https://python-guide.readthedocs.org/en/latest/dev/virtualenvs/#virtualenv)


### Local Setup

The following assumes you have all of the recommended tools listed above installed.

#### Clone the project:

    $ git clone https://github.com/gnknithin/Personify-Service.git
    $ cd Personify-Service

#### Create and initialize virtualenv for the project:

    $ python3 -m venv .venv
    $ source .venv/bin/activate
    $ pip3 install -r requirements.txt

## Running the entire application stack

If you have docker-compose installed and docker running; it is really simple to spin up the entire application stack.

Make sure you are in the root directory of the repository where the docker-compose file is.

### Expected Environment Variables 
All the environment variables for the application need to be specified in the docker compose file,
this allows to seperate environment configurations concerns from our applicaiton code meaning it can easily spun up for local, development and production environments with different db credentials, ports etc.

### Create an .env as following

```
POSTGRES_HOST=localhost
POSTGRES_USER=personifydev
POSTGRES_PASSWORD=testenv@123
POSTGRES_DATABASE=personify
APPLY_MIGRATIONS=1
ALEMBIC_CONFIG=src/infra/data/migrations/alembic.ini
MONGODB_HOST=localhost
MONGODB_USERNAME=personifydev
MONGODB_PASSWORD=testenv@123
MONGODB_DATABASE=personify
```

#### Up Required Infrastrucutre:
```
docker-compose -f ./docker-compose.dev.yml up -d --force-recreate --renew-anon-volumes
```

#### To Run Server:
```
python3 src/server.py -p 8888 -c ./configs/development.yaml -d
```

#### To Stop Run Server:
```
press Cntrl + c
```

#### To Stop
```
docker-compose -f ./docker-compose.dev.yml down --remove-orphans
```

## Tests  and Code Coverage
Installing Dependencies and checking
```
pip3 install pytest pytest-asyncio pytest-cov pytest-dotenv
```
### Unit Tests and Code Coverage
```
pytest -vv --cov --cov-report=term-missing ./tests/unit
```
### Integration Tests and Code Coverage
```
pytest -vv --cov --cov-report=term-missing ./tests/integration
```
### End2End Tests and Code Coverage
```
pytest -vv --cov --cov-report=term-missing ./tests/e2e
```
### Code Coverage
```
pytest -vv --cov --cov-report=term-missing
```
## Linting
Installing Dependencies and checking
```
pip3 install ruff
ruff check .
```

## Type Checking
Installing Dependencies and checking
```
pip3 install mypy
mypy .
```


## Working Features

Once you run the entire application stack using docker compose, you should be able access the public routes below:

Feature | Type | Route | Access
------------ | ------------- | ------------- | -------------
Health Check | GET | http://localhost:8888/health | Public
Add a new user | POST | http://localhost:8888/api/v1/signup | Public
Authenticate a user | POST | http://localhost:8888/api/v1/signup | Public
Get all contacts | GET | http://localhost:8888/api/v1/contact | Protected
Add a new contact| POST | http://localhost:8888/api/v1/contact | Protected
Get a specific contact | GET | http://localhost:8888/api/v1/contact/{contact_id} | Protected
Update a specific contact | PUT | http://localhost:8888/api/v1/contact/{contact_id} | Protected
Delete a specific contact | DELETE | http://localhost:8888/api/v1/contact/{contact_id} | Protected

# Highlights
 - [x] Documentation - Swagger
 - [x] Code Coverage
 - [x] Markdown Diagrams
 - [x] Ruff Linting
 - [x] MyPy Typing
 - [x] Testing
    - [x] Unit Testing
    - [x] Integration Testing
    - [x] End2End Testing
    - [x] Postman
 - [x] Deployment Solution and Documentation
 - [x] Final: Production READY

## Project Links
- Issues: https://github.com/gnknithin/Personify-Service/issues

## License
GNU General Public License v3.0. See the bundled [LICENSE](https://github.com/gnknithin/Personify-Service/blob/main/LICENSE) file for more details.
