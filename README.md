ansible-mysql-query
===================

Ansible module to set values in a mysql table, or insert records. Useful for webapplications that store configurations in database. E.g. icingaweb2 requires the initial user to be inserted into the database. The install-wizard could do it, but with ansible you want to automate installation ;)

Requirements:
- python bindings for mysql (python-mysqldb on Debian, MySQL-python on RedHat/Fedora)

Install
-------

Install via ansible-galaxy, *ansible-galaxy install zauberpony.mysql-query*, or manually put the file `mysql_query` into your *roles_path*.
