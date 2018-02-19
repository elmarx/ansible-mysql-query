from ansible.compat.tests import unittest
from ansible.compat.tests.mock import patch
from ansible.module_utils import basic
from library import mysql_query
from tests.fixtures import MYSQL_CONNECTION_PARAMS, Fixture
from tests.utils import set_module_args, AnsibleFailJson, exit_json, fail_json, AnsibleExitJson


class MysqlQueryMultiCheckTest(unittest.TestCase):
    def setUp(self):
        self.module = mysql_query

        self.mock_exit_fail = patch.multiple(basic.AnsibleModule, exit_json=exit_json, fail_json=fail_json)
        self.mock_exit_fail.start()
        self.addCleanup(self.mock_exit_fail.stop)

        self.f = Fixture()
        self.f.create_database()
        self.f.create_multicolumn_example()

    def tearDown(self):
        self.f.close()

    def test_insert_required(self):
        set_module_args(
            login_user=MYSQL_CONNECTION_PARAMS['user'],
            name=MYSQL_CONNECTION_PARAMS['db'],
            login_password=MYSQL_CONNECTION_PARAMS['passwd'],
            login_host=MYSQL_CONNECTION_PARAMS['host'],
            table='multicolumn_example',
            identifiers=dict(identifier1='elmar@athmer.org', identifier2='4', identifier3='testInsert'),
            values=dict(value1='8', value2='admin', value3="made up"),
            _ansible_check_mode=True,
        )

        with self.assertRaises(AnsibleExitJson) as e:
            self.module.main()

        result = e.exception.args[0]
        self.assertTrue(result['changed'], 'a required change is detected')
        self.assertRegexpMatches(result['msg'], 'insert')
        self.assertEquals(self.f.count_multicolumn_example(), 0, 'no row has been inserted in check-mode')

    def test_no_change_required(self):
        # insert a row that does not need to be updated
        self.f.insert_into_multicolumn_example(['elmar@athmer.org', 4, 'testNoChangeRequired'], [8, 'admin', 'made up'])

        set_module_args(
            login_user=MYSQL_CONNECTION_PARAMS['user'],
            name=MYSQL_CONNECTION_PARAMS['db'],
            login_password=MYSQL_CONNECTION_PARAMS['passwd'],
            login_host=MYSQL_CONNECTION_PARAMS['host'],
            table='multicolumn_example',
            identifiers=dict(identifier1='elmar@athmer.org', identifier2='4', identifier3='testNoChangeRequired'),
            values={'value1': '8', 'value2': 'admin', 'value3': "made up"},
        )

        with self.assertRaises(AnsibleExitJson) as e:
            self.module.main()

        result = e.exception.args[0]

        self.assertIn('changed', result)
        self.assertFalse(result['changed'], 'no changed required is detected')
        self.assertEquals(self.f.count_multicolumn_example(), 1, 'no additional row has been inserted in check-mode')

    def test_change_detection_for_digits_in_strings(self):
        # insert a row that does not need to be updated
        self.f.insert_into_multicolumn_example(['elmar@athmer.org', 4, '5'], [8, '15', '16'])

        set_module_args(
            login_user=MYSQL_CONNECTION_PARAMS['user'],
            name=MYSQL_CONNECTION_PARAMS['db'],
            login_password=MYSQL_CONNECTION_PARAMS['passwd'],
            login_host=MYSQL_CONNECTION_PARAMS['host'],
            table='multicolumn_example',
            identifiers=dict(identifier1='elmar@athmer.org', identifier2='4', identifier3='5'),
            values={'value1': '8', 'value2': '15', 'value3': "16"},
        )

        with self.assertRaises(AnsibleExitJson) as e:
            self.module.main()

        result = e.exception.args[0]

        self.assertIn('changed', result)
        self.assertFalse(result['changed'], 'no changed required is detected')
        self.assertEquals(self.f.count_multicolumn_example(), 1, 'no additional row has been inserted in check-mode')
