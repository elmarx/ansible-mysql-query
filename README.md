ansible-mysql-query
===================

Ansible module to set values in a mysql table, or insert records. Useful for webapplications that store configurations in database. E.g. icingaweb2 requires the initial user to be inserted into the database. The install-wizard could do it, but with ansible you want to automate installation ;)

Requirements:

- python bindings for mysql ([python-mysqldb](https://packages.debian.org/jessie/python-mysqldb) on Debian, MySQL-python on RedHat/Fedora)

Install
-------

Install via ansible-galaxy, *ansible-galaxy install zauberpony.mysql-query*, or manually put the file `mysql_query` into your *roles_path*.

Running the examples
--------------------

Make sure you have a running mysql server (e.g.: use the *docker-compose.yml* in *tests/infrastructure*) and update the connection-parameters if necessary.
 
Run via ```ansible-playbook -i demo.yml``` (or even simpler ```./demo.yml```) and undo (to start all over) with ```ansible-playbook -i reset.yml```.