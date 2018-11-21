#!/usr/bin/env python
# -*- coding: utf-8 -*-


DOCUMENTATION = """
---
module: mysql_query.py
author:
    - 'Elmar Athmer'
short_description: Insert/update/remove rows in a mysql table.
description:
  - This module sets values in a mysql table, or insert records. Useful for webapplications that store configurations
     in database.
options:
  table:
    required: true
    description:
      - table where to insert/update records
  identifiers:
    required: true
    description:
      - dictionary of values to identifier a row, i.e. determine if the row exists, needs to be updated etc.
  values:
    required: false
    description:
        - dictionary of values that should be 'enforced', i.e. either updated (if the row has been found by it's
          identifiers) or used during insert
  defaults:
    required: false
    description:
        - dictionary of additional values that will be used iff an insert is required.
"""

EXAMPLES = """
- name: update a row
  mysql_query.py:
    name: ansible-playbook-example
    table: simple_table
    login_host: ::1
    login_user: root
    login_password: password
    identifiers:
      identifier1: 4
      identifier2: 'eight'
    values:
      value1: 16
      value2: 'sixteen plus 1'
    defaults:
      default1: can be anything, will be ignored for update
      default2: will not change

- name: insert a row
  mysql_query.py:
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
      default2: one-hundred-2
"""

from contextlib import closing

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.database import mysql_quote_identifier

# make mysql-query backward compatible with ansible < 2.7.2 
try:
    from ansible.module_utils.mysql import mysql_connect, mysql_driver, mysql_driver_fail_msg
except ImportError:
    from ansible.module_utils.mysql import mysql_connect, mysqldb_found
    if mysqldb_found:
        import MySQLdb as mysql_driver
    else:
        mysql_driver = None
        mysql_driver_fail_msg = 'The MySQL-python module is required.'

from ansible.module_utils._text import to_native

DELETE_REQUIRED = 0
INSERT_REQUIRED = 1
UPDATE_REQUIRED = 2
NO_ACTION_REQUIRED = 3
ERR_NO_SUCH_TABLE = 4


def weak_equals(a, b):
    """
    helper function to compare two values where one might be a string
    :param a:
    :param b:
    :return:
    """
    # the simple case: a and b are of the same type, or of types that can be compared for equality (e.g.: int and float)
    if type(a) == type(b) or a == b:
        return a == b

    # try to stringify both and compare then…
    return str(a) == str(b)


def tuples_weak_equals(a, b):
    """
    tests two tuples for weak equality
    :param a:
    :param b:
    :return:
    """
    if len(a) == len(b):
        pairs = zip(a, b)
        return all([weak_equals(a, b) for a, b in pairs])

    return False


def generate_where_segment(items):
    """
    generate a part of an sql statement
    :param items: key-value items representing column/values
    :return: the part to insert after "where"
    """
    return [
        "%s=%s" % (name, value) if type(value) == int
        else "%s='%s'" % (name, value)
        for (name, value) in items
    ]


def check_row_exists(cursor, table, identifiers):
    """
    check a specified row only for existence
    :param cursor: cursor object able to execute queries
    :param table: name of the table to look into
    :param identifiers:
    :return: True if the row exists, False otherwise
    """
    query = "select exists(select 1 from {table} where {values})".format(
        table=table,
        values=" AND ".join(generate_where_segment(identifiers.items())),
    )

    try:
        res = cursor.execute(query)
    except mysql_driver.ProgrammingError as e:
        (errcode, message) = e.args
        if errcode == 1146:
            return ERR_NO_SUCH_TABLE
        else:
            raise e

    exists, = cursor.fetchone()
    return exists == 1


def change_required(state, cursor, table, identifiers, desired_values):
    """
    check if a change is required
    :param state: state, either 'present' or 'absent'
    :param cursor: cursor object able to execute queries
    :param table: name of the table to look into
    :type table: str
    :param identifiers: a list of tuples (column name, value) to use in where clause
    :type identifiers: dict
    :param desired_values: a list of tuples (column name, values) that the record should match
    :type desired_values: dict
    :return: one of DELETE_REQUIRED, INSERT_REQUIRED, UPDATE_REQUIRED or NO_ACTION_REQUIRED
    :rtype: int
    """

    # first, let's determine if we do a simple existence-check, or if we also have to compare values
    if state == "absent" or not desired_values:
        row_exists = check_row_exists(cursor, table, identifiers)

        if state == "absent" and row_exists:
            return DELETE_REQUIRED

        if state == "present" and not row_exists:
            return INSERT_REQUIRED

        # other cases:  state == "absent" and not row_exists:
        #               state == "present" and row_exists
        # both require no action
        return NO_ACTION_REQUIRED

    # ok, we have to compare values, so let's make a query selecting all the columns with desired_values
    query = "select {columns} from {table} where {values}".format(
        table=table,
        columns=", ".join(desired_values.keys()),
        values=" AND ".join(generate_where_segment(identifiers.items())),
    )

    try:
        res = cursor.execute(query)
    except mysql_driver.ProgrammingError as e:
        (errcode, message) = e.args
        if errcode == 1146:
            return ERR_NO_SUCH_TABLE
        else:
            raise e

    # if no row has been found at all, an insert is required
    if res == 0:
        return INSERT_REQUIRED

    # a row has been found, so we need to compare the returned values:

    # bring the values argument into shape to compare directly to fetchone() result
    expected_query_result = tuple(desired_values.values())
    actual_result = cursor.fetchone()

    # compare expected_query_result to actual_result with implicit casting
    if tuples_weak_equals(expected_query_result, actual_result):
        return NO_ACTION_REQUIRED

    # a record has been found but does not match the desired values
    return UPDATE_REQUIRED


def execute_action(cursor, action, table, identifier, values, defaults):
    """
    when not running in check mode, this function carries out the required changes
    :param action: the actual action to execute
    :rtype: dict
    :param cursor:
    :param table:
    :param identifier:
    :param values:
    :param defaults:
    :return: a summary of the action done usable as kwargs for ansible
    """
    try:
        if action == DELETE_REQUIRED:
            return delete_record(cursor, table, identifier)
        if action == INSERT_REQUIRED:
            return insert_record(cursor, table, identifier, values, defaults)
        elif action == UPDATE_REQUIRED:
            return update_record(cursor, table, identifier, values)
        else:
            return {'failed': True, 'msg': 'Internal Error: unknown action "%s" required' % action}
    except Exception as e:
        return {'failed': True, 'msg': 'updating/inserting/deleting the record failed due to "%s".' % str(e)}


def update_record(cursor, table, identifiers, values):
    where = ' AND '.join(['{0} = %s'.format(column) for column in identifiers.keys()])
    value = ', '.join(['{0} = %s'.format(column) for column in values.keys()])

    query = "UPDATE {0} set {1} where {2} limit 1".format(table, value, where)

    cursor.execute(query, tuple(values.values() + identifiers.values()))
    return dict(changed=True, msg='Successfully updated one row')


def insert_record(cursor, table, identifiers, values, defaults):
    row_data = dict(identifiers.items() + values.items() + defaults.items())
    value_placeholder = ", ".join(["%s"] * len(row_data))

    query = "insert into {table} ({cols}) values ({value_placeholder})".format(
        table=table,
        cols=", ".join(row_data.keys()),
        value_placeholder=value_placeholder,
    )

    cursor.execute(query, tuple(row_data.values()))
    return dict(changed=True, msg='Successfully inserted a new row')


def delete_record(cursor, table, identifiers):
    where = ' AND '.join(['{0} = %s'.format(column) for column in identifiers.keys()])
    query = "DELETE FROM {0} WHERE {1}".format(table, where)
    cursor.execute(query, tuple(identifiers.values()))
    return dict(changed=True, msg='Successfully deleted one row')


def build_connection_parameter(params):
    """
    fetch mysql connection parameters consumable by mysqldb.connect from module args or ~/.my.cnf if necessary
    :param params:
    :return:
    :rtype: dict
    """
    # TODO: read ~/.my.cnf, set sane defaults etc.

    # map: (ansible_param_name, mysql.connect's name)
    param_name_map = [
        ('login_user', 'user'),
        ('login_password', 'passwd'),
        ('name', 'db'),
        ('login_host', 'host'),
        ('login_port', 'port'),
        ('login_unix_socket', 'unix_socket')
    ]

    t = [(mysql_name, params[ansible_name])
         for (ansible_name, mysql_name) in param_name_map
         if ansible_name in params and params[ansible_name]
         ]

    return dict(t)


def connect(connection, module):
    try:
        db_connection = mysql_driver.connect(**connection)
        return db_connection
    except Exception as e:
        module.fail_json(msg="Error connecting to mysql database: %s" % str(e))


def extract_column_value_maps(parameter):
    """
    extract mysql-quoted tuple-lists for parameters given as ansible params
    :param parameter:
    :return:
    """
    if parameter:
        for column, value in parameter.items():
            yield (mysql_quote_identifier(column, 'column'), value)


def failed(action):
    return action == ERR_NO_SUCH_TABLE


def main():
    module = AnsibleModule(
        argument_spec=dict(
            login_user=dict(default=None),
            login_password=dict(default=None, no_log=True),
            login_host=dict(default="localhost"),
            login_port=dict(default=3306, type='int'),
            login_unix_socket=dict(default=None),
            name=dict(required=True, aliases=['db']),
            state=dict(default="present", choices=['absent', 'present']),

            table=dict(required=True),

            identifiers=dict(required=True, type='dict'),
            values=dict(default=None, type='dict'),
            defaults=dict(default=None, type='dict'),

            #allow_insert=dict(default=False, type='bool'),
            #limit=dict(default=1, type='int'),
        ),
        supports_check_mode=True
    )

    if mysql_driver is None:
        module.fail_json(msg=mysql_driver_fail_msg)

    # mysql_quote all identifiers and get the parameters into shape
    table = mysql_quote_identifier(module.params['table'], 'table')
    identifiers = dict(extract_column_value_maps(module.params['identifiers']))
    values = dict(extract_column_value_maps(module.params['values']))
    defaults = dict(extract_column_value_maps(module.params['defaults']))

    exit_messages = {
        DELETE_REQUIRED: dict(changed=True, msg='Record needs to be deleted'),
        INSERT_REQUIRED: dict(changed=True, msg='No such record, need to insert'),
        UPDATE_REQUIRED: dict(changed=True, msg='Records needs to be updated'),
        NO_ACTION_REQUIRED: dict(changed=False),
        ERR_NO_SUCH_TABLE: dict(failed=True, msg='No such table %s' % table)
    }

    with closing(connect(build_connection_parameter(module.params), module)) as db_connection:
        # find out what needs to be done (independently of check-mode)
        required_action = change_required(module.params['state'], db_connection.cursor(), table, identifiers, values)

        # if we're in check mode, there's no action required, or we already failed: directly set the exit_message
        if module.check_mode or required_action == NO_ACTION_REQUIRED or failed(required_action):
            exit_message = exit_messages[required_action]
        else:
            # otherwise, execute the required action to get the exit message
            exit_message = execute_action(db_connection.cursor(), required_action, table, identifiers, values, defaults)
            db_connection.commit()

    if 'failed' in exit_message and exit_message.get('failed'):
        module.fail_json(**exit_message)
    else:
        module.exit_json(**exit_message)


if __name__ == '__main__':
    main()
