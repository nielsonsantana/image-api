Image Api in Pyramid
=========

This project was built based on template [pyramid-cookiecutter-alchemy][https://github.com/Pylons/pyramid-cookiecutter-alchemy].

Não gostei do modo como as rotas são declaradas.

Pontos que não gostei no pyramid:
Não encontrei uma forma simples de gerar a url sem baseado no nome da rota.


Instalação do docker-compose

https://docs.docker.com/compose/install/



Getting Started
---------------

- Change directory into your newly created project.

    cd image_api

- Create a Python virtual environment.

    python3 -m venv env

- Upgrade packaging tools.

    env/bin/pip install --upgrade pip setuptools

- Install the project in editable mode with its testing requirements.

    env/bin/pip install -e ".[testing]"

- Configure the database.

    env/bin/initialize_image_api_db development.ini

- Run your project's tests.

    env/bin/pytest

- Run your project.

    env/bin/pserve development.ini
