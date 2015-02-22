ansible-mysql-query
===================

Ansible module to set values in a mysql table. Sometimes some web-applications require settings to be done in the database.

Requirements:
- python bindings for mysql (python-mysqldb on Debian)

Install
-------

Just put `mysql_query` into your library directory, or somewhere else in your module paths.


Development setup
-----------------

You'll need:

- mysql-client installed on your host
- docker
- docker-compose (previously known as fig)

I use a dockerized mysql-database, so I don't need to run a full RDBMs on my host:

    # run docker container:
    $ docker-compose up -d

Create a *~/.my.cnf* file to connect to the database easily:

    [client]
    host=127.0.0.1
    user=root
    password=secret

Then you can import the test-database:

    # import test-database:
    $ mysql < ansible-test-db.sql 

Finally, set-up the ansible-env:

    $ source ansible/hacking/env-setup
    $ chmod +x ansible/hacking/test-module

Run the module:

    $ ansible/hacking/test-module -m ./mysql_query



