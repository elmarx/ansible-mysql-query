Ansible Role: mysql_query
===================

Ansible module to set values in a mysql table, or insert records. Useful for web-applications that store configurations in database. E.g. icingaweb2 requires the initial user to be inserted into the database. The install-wizard could do it, but with ansible you want to automate installation ;)

Listed at Ansible Galaxy Page as [zauberpony.mysql-query](https://galaxy.ansible.com/zauberpony/mysql-query/).

Install
-------

Install via ansible-galaxy, `ansible-galaxy install zauberpony.mysql-query`, or manually put the file *mysql_query* into your *roles_path*.

### Requirements:

python bindings for mysql (just like the core mysql_* modules):

- MySQLdb (Python 2.x only)
- PyMySQL (Python 2.7 and python 3.x)


Example playbook
----------------

### A complete example that ensures a record is present in a given table.

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
          id: 14
          email: 'john@example.com'
        values:
          role: "admin"
          department: 'IT'
        defaults:
          password: "secret"
          last_login: 1469264933
```

Given a table `simple_table` with columns (*id*, *email*, *role*, *department*, *password*, *last_login*), this example would:
- Look for a row *where id = 14 and email = 'john@example.com'*
  - if the row does not exist: insert a row with id=14, email='john@example.com', role="admin", department="IT", password="secret", last_login=1469264933
  - if the row does exist: check if the ***values*** (role, department) match the given values, if not: update

Thus:
- *identifieres* are being used to check for existence and to find a row
- *defaults* are being used as default values if the row is not present (i.e.: only used for insert)
- *values* are the state of the row that ansible ensures

### A complete example that ensures a record is not present in a given table.

```yaml
---
- hosts: all
  roles:
    - zauberpony.mysql-query
  tasks:
    - name: insert a row
      mysql_query:
        state: absent
        name: ansible-playbook-example
        table: simple_table
        login_host: ::1
        login_user: root
        login_password: password
        identifiers:
          id: 14
          email: 'john@example.com'
```

### Running the examples from sources

Make sure you have a running mysql server (e.g.: use the *docker-compose.yml*-file) and update the connection-parameters if necessary.

Run via `ansible-playbook -i demo.yml` (or even simpler `./demo.yml`) and undo (to start all over) with `ansible-playbook -i reset.yml`.
