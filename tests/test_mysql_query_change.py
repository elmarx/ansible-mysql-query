from ansible.compat.tests import unittest
from ansible.compat.tests.mock import patch
from ansible.module_utils import basic

from library import mysql_query
from tests.fixtures import MYSQL_CONNECTION_PARAMS, Fixture
from tests.utils import exit_json, fail_json, set_module_args, AnsibleExitJson


class MysqlQueryChangeTest(unittest.TestCase):
    def setUp(self):
        self.module = mysql_query

        self.mock_exit_fail = patch.multiple(basic.AnsibleModule, exit_json=exit_json, fail_json=fail_json)
        self.mock_exit_fail.start()
        self.addCleanup(self.mock_exit_fail.stop)

        self.f = Fixture()
        self.f.create_database()
        self.f.create_change_example()

    def tearDown(self):
        self.f.close()

    def test_insert_required(self):
        set_module_args(
            login_user=MYSQL_CONNECTION_PARAMS['user'],
            name=MYSQL_CONNECTION_PARAMS['db'],
            login_password=MYSQL_CONNECTION_PARAMS['passwd'],
            login_host=MYSQL_CONNECTION_PARAMS['host'],
            table='change_example',
            identifiers=dict(setting_name='do_backups', setting_group_id='4', ),
            values=dict(value1=8, value2='fifteen'),
            defaults=dict(default1=16, default3='thirty-two'),
        )

        self.assertEquals(self.f.count_change_example(), 0, 'no row in table before running the module')

        with self.assertRaises(AnsibleExitJson) as e:
            self.module.main()

        result = e.exception.args[0]

        self.assertIn('changed', result)
        self.assertTrue(result['changed'], 'the database has been changed')
        self.assertEquals(self.f.count_change_example(), 1, 'a row has been inserted')
        row = self.f.query_change_example('do_backups', 4)
        self.assertItemsEqual((8, 'fifteen'), row[3:5], 'values were inserted')
        self.assertItemsEqual((16, 42, 'thirty-two'), row[5:8], 'row has been inserted with default values')

    def test_update_required(self):
        self.f.insert_into_change_example(['do_syncs', '5'], [42, 'four'], [8, 16, 'bar'])

        set_module_args(
            login_user=MYSQL_CONNECTION_PARAMS['user'],
            name=MYSQL_CONNECTION_PARAMS['db'],
            login_password=MYSQL_CONNECTION_PARAMS['passwd'],
            login_host=MYSQL_CONNECTION_PARAMS['host'],
            table='change_example',
            identifiers=dict(setting_name='do_syncs', setting_group_id='5'),
            values=dict(value1='43', value2='five'),
            defaults=dict(default1=9, default2='miow', bogus='foo')
        )

        with self.assertRaises(AnsibleExitJson) as e:
            self.module.main()

        result = e.exception.args[0]
        self.assertIn('changed', result)
        self.assertRegexpMatches(result['msg'], 'Successfully updated')
        self.assertEquals(self.f.count_change_example(), 1, 'no additional row has been inserted')
        row = self.f.query_change_example('do_syncs', '5')
        self.assertItemsEqual((43, 'five'), row[3:5], 'values have been updated')
        self.assertItemsEqual((8, 16, 'bar'), row[5:8], 'defaults have not been changed')

    def test_no_change_required_in_no_check_mode(self):
        """
        this is the case if no change is required, but we're not in check mode.
        :return:
        """
        self.f.insert_into_change_example(['no change required', 3], [1, 'one'], [1, 2, 'three'])

        set_module_args(
            login_user=MYSQL_CONNECTION_PARAMS['user'],
            name=MYSQL_CONNECTION_PARAMS['db'],
            login_password=MYSQL_CONNECTION_PARAMS['passwd'],
            login_host=MYSQL_CONNECTION_PARAMS['host'],
            table='change_example',
            identifiers=dict(setting_name='no change required', setting_group_id=3),
            values=dict(value1=1, value2='one')
        )

        with self.assertRaises(AnsibleExitJson) as e:
            self.module.main()

        result = e.exception.args[0]
        self.assertIn('changed', result)
        self.assertFalse(result['changed'])




