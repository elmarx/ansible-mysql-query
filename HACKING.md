[![Build Status](https://travis-ci.org/zauberpony/ansible-mysql-query.svg?branch=master)](https://travis-ci.org/zauberpony/ansible-mysql-query)

# Hacking mysql_query module/role

This module is TDD, the setup is inspired by ansible
[module-unit-tests](http://docs.ansible.com/ansible/latest/dev_guide/developing_modules_general.html#unit-testing)
(although the tests here are no strict unit-tests, as they interact with a database).


## development setup

### pipenv

For python-development it's common to use [pipenv](https://pipenv.readthedocs.io/en/latest/).

Combined with [direnv](https://direnv.net/) you just need to cd into this directory.

### database

I recommend to use [docker-compose](https://docs.docker.com/compose/) for the development infrastructure, but any
MySQL/MariaDB-Server should do (e.g.: installed via your local package-manager, run via docker directly).

Start the mariadb container with *docker-compose*:

    $ docker-compose up -d

Then tests are executable via:

    $ pytest tests/

or use your favorite IDE (e.g. PyCharm) to execute your tests.

If you don't use the docker-compose file, you might need to pass the db-connection settings via env, see `settings.py`
for available options, e.g:

    $ MYSQL_PASSWORD=secret pytest tests/
