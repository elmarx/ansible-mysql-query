from ansible.compat.tests import unittest
from ansible.compat.tests.mock import patch
from ansible.module_utils import basic

from library import mysql_query
from tests.fixtures import MYSQL_CONNECTION_PARAMS, Fixture
from tests.utils import exit_json, fail_json, set_module_args, AnsibleExitJson


class MysqlQueryCheckTest(unittest.TestCase):
    def setUp(self):
        self.module = mysql_query

        self.mock_exit_fail = patch.multiple(basic.AnsibleModule, exit_json=exit_json, fail_json=fail_json)
        self.mock_exit_fail.start()
        self.addCleanup(self.mock_exit_fail.stop)

        self.f = Fixture()
        self.f.create_database()
        self.f.create_key_value_example()

    def tearDown(self):
        self.f.close()

    def test_insert_required(self):
        set_module_args(
            login_user=MYSQL_CONNECTION_PARAMS['user'],
            name=MYSQL_CONNECTION_PARAMS['db'],
            login_password=MYSQL_CONNECTION_PARAMS['passwd'],
            login_host=MYSQL_CONNECTION_PARAMS['host'],
            table='key_value_example',
            identifiers=dict(name='testInsertRequired_myKey'),
            values=dict(value='42'),
            _ansible_check_mode=True,
        )

        with self.assertRaises(AnsibleExitJson) as e:
            self.module.main()

        result = e.exception.args[0]
        self.assertTrue(result['changed'], 'a required change is detected')
        self.assertRegexpMatches(result['msg'], 'insert')
        self.assertEquals(self.f.count_key_value_example(), 0, 'no row has been inserted in check-mode')

    def test_no_change_required(self):
        # insert a row that does not need to be updated
        self.f.insert_into_key_value_example('testNoChangeRequired_myKey', 42)

        set_module_args(
            login_user=MYSQL_CONNECTION_PARAMS['user'],
            name=MYSQL_CONNECTION_PARAMS['db'],
            login_password=MYSQL_CONNECTION_PARAMS['passwd'],
            login_host=MYSQL_CONNECTION_PARAMS['host'],
            table='key_value_example',
            identifiers=dict(name='testNoChangeRequired_myKey'),
            values=dict(value='42'),
        )

        with self.assertRaises(AnsibleExitJson) as e:
            self.module.main()

        result = e.exception.args[0]
        self.assertIn('changed', result)
        self.assertFalse(result['changed'], 'no changed required is detected')
        self.assertEquals(self.f.count_key_value_example(), 1, 'no additional row has been inserted in check-mode')

    def test_no_change_required_for_numeric_ids(self):
        # insert a row that does not need to be updated
        insert_id = self.f.insert_into_key_value_example('arbitrary', 42)

        set_module_args(
            login_user=MYSQL_CONNECTION_PARAMS['user'],
            name=MYSQL_CONNECTION_PARAMS['db'],
            login_password=MYSQL_CONNECTION_PARAMS['passwd'],
            login_host=MYSQL_CONNECTION_PARAMS['host'],
            table='key_value_example',
            identifiers=dict(id=insert_id),
            defaults=dict(value=23, name="default_arbitrary"),
        )

        with self.assertRaises(AnsibleExitJson) as e:
            self.module.main()

        result = e.exception.args[0]
        self.assertIn('changed', result)
        self.assertFalse(result['changed'], 'no changed required is detected')
        self.assertEquals(self.f.count_key_value_example(), 1, 'no additional row has been inserted in check-mode')

    def test_update_required(self):
        # insert a row that does need to be updated (4 vs 8)
        self.f.insert_into_key_value_example('testUpdateRequired_myKey', 4)

        set_module_args(
            login_user=MYSQL_CONNECTION_PARAMS['user'],
            name=MYSQL_CONNECTION_PARAMS['db'],
            login_password=MYSQL_CONNECTION_PARAMS['passwd'],
            login_host=MYSQL_CONNECTION_PARAMS['host'],
            table='key_value_example',
            identifiers=dict(name='testUpdateRequired_myKey'),
            values=dict(value='8'),
        )

        with self.assertRaises(AnsibleExitJson) as e:
            self.module.main()

        result = e.exception.args[0]
        self.assertIn('changed', result)
        self.assertTrue(result['changed'], 'a change (update) required is detected')
        self.assertRegexpMatches(result['msg'], 'update')
        self.assertEquals(self.f.count_key_value_example(), 1, 'no additional row has been inserted in check-mode')

    def test_delete_required(self):
        # insert a row that need to deleted.
        self.f.insert_into_key_value_example('testDeleteRequired_myKey', 6)

        set_module_args(
            login_user=MYSQL_CONNECTION_PARAMS['user'],
            name=MYSQL_CONNECTION_PARAMS['db'],
            login_password=MYSQL_CONNECTION_PARAMS['passwd'],
            login_host=MYSQL_CONNECTION_PARAMS['host'],
            table='key_value_example',
            identifiers=dict(name='testDeleteRequired_myKey'),
            state='absent',
            _ansible_check_mode=True,
        )

        with self.assertRaises(AnsibleExitJson) as e:
            self.module.main()

        result = e.exception.args[0]
        self.assertTrue(result['changed'], 'a required change is detected')
        self.assertRegexpMatches(result['msg'], 'delete')
        self.assertEquals(self.f.count_key_value_example(), 1, 'no row has been deleted in check-mode')
