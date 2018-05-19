Image Api in Pyramid
=========

[![Build Status](https://travis-ci.org/nielsonsantana/image-api.svg?branch=master)](https://travis-ci.org/nielsonsantana/image-api)

This project was built based on template [pyramid-cookiecutter-alchemy](https://github.com/Pylons/pyramid-cookiecutter-alchemy).

## Project Structure
This tree show some notes about the code structure of the project.
    
    .
    ├── CHANGES.txt
    ├── compose
    │   └── start.sh            # Script to start the server in development mode
    ├── development.ini
    ├── docker-compose.yml
    ├── docker-entrypoint.sh
    ├── Dockerfile
    ├── documentation-api.yml
    ├── image_api
    │   ├── api_v1              # Main application where the REST API was implemented
    │   │   ├── __init__.py
    │   │   ├── models.py       # Image model
    │   │   ├── routes.py       # Api routes
    │   │   ├── tests           # Tests for views, model, utils and functional
    │   │   ├── utils.py        # Helper functions
    │   │   └── views.py
    │   ├── core
    │   │   ├── __init__.py
    │   │   ├── models
    │   │   ├── routes.py
    │   │   └── views.py
    │   ├── __init__.py         # Initialize the Project 
    │   ├── routes.py           # Setup routes
    │   ├── scripts             # Script to initialize db
    │   ├── static
    │   └── templates
    ├── LICENSE
    ├── media                   # Directore to store of images
    ├── production.ini
    ├── pytest.ini
    ├── README.md
    ├── requirements
    │   ├── base.txt
    │   └── test.txt
    ├── requirements.txt
    └── setup.py

## Getting Started
To start using the project In order to use and develop the project is need install

### Using docker-compose
Fallow the install instructions at https://docs.docker.com/compose/install/

After install docker-compose, use this command to start:

    docker-compose up
    
### Using docker
Build the docker project with the command:
    
    docker build -t image-api .

Start the image-api with the command:
    
    docker run image-api /app/compose/start.sh
    
#### Tests using docker
    docker run --rm image-api bash -c "pip install -r requirements/tests.txt && pytest"

## API
API docs at https://app.swaggerhub.com/apis/nsantana/Image-api-pyramid/1.0.0

## Automated Build and Test
Access at https://travis-ci.org/nielsonsantana/image-api

## Docker Image Repository
Access at https://hub.docker.com/r/nsantana/image-api-pyramid/