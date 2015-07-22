ansible-mysql-query
===================

Ansible module to set values in a mysql table, or insert records. Useful for webapplications that store configurations in database. E.g. icingaweb2 requires the initial user to be inserted into the database. The install-wizard could do it, but with ansible you want to automate installation ;)

Requirements:
- python bindings for mysql (python-mysqldb on Debian)

Install
-------

Install via ansible-galaxy, *ansible-galaxy install zauberpony.mysql-query*, or manually put this repository into your *roles_path*.


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

    $ ansible/hacking/test-module -m ./mysql_query -a "name=ansible-test table=key_value_example identifier_column=name identifier=a login_host=127.0.0.1 login_user=root login_password=secret value_column=value value=4"



