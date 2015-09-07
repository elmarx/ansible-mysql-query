import unittest
from tests import utils
from tests.fixtures import Fixture
from tests.fixtures import MYSQL_CONNECTION_PARAMS
import time


class MysqlQueryChangeTest(unittest.TestCase):
    def setUp(self):
        self.f = Fixture()
        self.f.create_database()
        self.f.create_change_example()

    def tearDown(self):
        self.f.close()

    def testInsertRequired(self):
        args = dict(
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
        result = utils.ansible_run(args)
        self.assertIn('changed', result)
        self.assertTrue(result['changed'], 'the database has been changed')
        count = self.f.count_change_example()
        self.assertEquals(self.f.count_change_example(), 1, 'a row has been inserted')

    @unittest.skip('update is not yet implemented, let\'s test insert first')
    def testUpdateRequired(self):
        self.f.insert_into_key_value_example('testUpdateRequired_myKey', 4)

        args = dict(
            login_user='root',
            name='ansible-mysql-query-test',
            table='key_value_example',
            identifiers=dict(name='testUpdateRequired_myKey'),
            values=dict(value='8'),
        )

        result = utils.ansible_run(args)
        self.assertIn('changed', result)
        self.assertTrue(result['changed'], 'a change (update) required is detected')
        self.assertRegexpMatches(result['msg'], 'update')
        self.assertEquals(self.f.count_key_value_example(), 1, 'no additional row has been inserted in check-mode')
