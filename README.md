Ansible Role: mysql_query
===================

Ansible module to set values in a mysql table, or insert records. Useful for web-applications that store configurations in database. E.g. icingaweb2 requires the initial user to be inserted into the database. The install-wizard could do it, but with ansible you want to automate installation ;)

Listed at Ansible Galaxy Page as [zauberpony.mysql-query](https://galaxy.ansible.com/list#/roles/5106)

Install
-------

Install via ansible-galaxy, `ansible-galaxy install zauberpony.mysql-query`, or manually put the file *mysql_query* into your *roles_path*.

### Requirements:

python bindings for mysql ([python-mysqldb](https://packages.debian.org/jessie/python-mysqldb) on Debian, MySQL-python on RedHat/Fedora), just like the core mysql_* modules.


Example playbook
----------------

A complete example that ensures a record is present in a given table.

```yaml
---
- hosts: all
  roles:
    - zauberpony.mysql-query
  tasks:
    - name: insert a row
      mysql_query:
        name: ansible-playbook-example
        table: simple_table
        login_host: ::1
        login_user: root
        login_password: password
        identifiers:
          identifier1: 14
          identifier2: 'eighteen'
        values:
          value1: 115
          value2: 'one-hundred-sixteen'
        defaults:
          default1: 125
          default2: one-hundred-25
```

### Running the examples from sources

Make sure you have a running mysql server (e.g.: use the *docker-compose.yml* in *tests/infrastructure*) and update the connection-parameters if necessary.
 
Run via `ansible-playbook -i demo.yml` (or even simpler `./demo.yml`) and undo (to start all over) with `ansible-playbook -i reset.yml`.