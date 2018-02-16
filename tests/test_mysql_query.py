from ansible.compat.tests import unittest
from ansible.compat.tests.mock import patch
from ansible.module_utils import basic
from library import mysql_query
from tests.fixtures import MYSQL_CONNECTION_PARAMS, Fixture
from tests.utils import set_module_args, AnsibleFailJson, exit_json, fail_json


class MysqlQueryTest(unittest.TestCase):

    def setUp(self):
        self.module = mysql_query

        self.mock_exit_fail = patch.multiple(basic.AnsibleModule, exit_json=exit_json, fail_json=fail_json)
        self.mock_exit_fail.start()
        self.addCleanup(self.mock_exit_fail.stop)

        self.f = Fixture()
        self.f.create_database()

    def tearDown(self):
        self.f.close()

    def test_fail_for_empty_values(self):
        set_module_args(
            login_user='root',
            name='ansible-mysql-query-test',
            table='key_value_example',
        )
        with self.assertRaises(AnsibleFailJson) as e:
            self.module.main()

        result = e.exception.args[0]
        self.assertTrue(result['failed'])
        self.assertEqual(result['msg'], 'missing required arguments: identifiers')

    def test_fail_for_table_missing(self):
        set_module_args(
            login_user=MYSQL_CONNECTION_PARAMS['user'],
            name=MYSQL_CONNECTION_PARAMS['db'],
            login_password=MYSQL_CONNECTION_PARAMS['passwd'],
            login_host=MYSQL_CONNECTION_PARAMS['host'],
            table='does_not_exist_table',
            identifiers=dict(not_relevant='bogus'),
            values=dict(not_relevant2='bogus'),
        )
        with self.assertRaises(AnsibleFailJson) as e:
            self.module.main()

        result = e.exception.args[0]

        self.assertTrue(result['failed'])
        self.assertEqual(result['msg'], 'No such table `does_not_exist_table`')
