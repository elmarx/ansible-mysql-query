import unittest

from tests import utils
from tests.fixtures import Fixture
from tests.settings import MYSQL_CONNECTION_PARAMS

class MysqlQueryCheckTest(unittest.TestCase):
    def setUp(self):
        self.f = Fixture()
        self.f.create_database()
        self.f.create_key_value_example()

    def tearDown(self):
        self.f.close()

    def testInsertRequired(self):
        args = dict(
            login_user=MYSQL_CONNECTION_PARAMS['user'],
            name=MYSQL_CONNECTION_PARAMS['db'],
            login_password=MYSQL_CONNECTION_PARAMS['passwd'],
            login_host=MYSQL_CONNECTION_PARAMS['host'],
            table='key_value_example',
            identifiers=dict(name='testInsertRequired_myKey'),
            values=dict(value='42'),
        )

        result = utils.ansible_check(args)
        print(result)
        self.assertTrue(result['changed'], 'a required change is detected')
        self.assertRegexpMatches(result['msg'], 'insert')
        self.assertEquals(self.f.count_key_value_example(), 0, 'no row has been inserted in check-mode')

    def testNoChangeRequired(self):
        # insert a row that does not need to be updated
        self.f.insert_into_key_value_example('testNoChangeRequired_myKey', 42)

        args = dict(
            login_user=MYSQL_CONNECTION_PARAMS['user'],
            name=MYSQL_CONNECTION_PARAMS['db'],
            login_password=MYSQL_CONNECTION_PARAMS['passwd'],
            login_host=MYSQL_CONNECTION_PARAMS['host'],
            table='key_value_example',
            identifiers=dict(name='testNoChangeRequired_myKey'),
            values=dict(value='42'),
        )

        result = utils.ansible_check(args)
        self.assertIn('changed', result)
        self.assertFalse(result['changed'], 'no changed required is detected')
        self.assertEquals(self.f.count_key_value_example(), 1, 'no additional row has been inserted in check-mode')

    def testUpdateRequired(self):
        # insert a row that does need to be updated (4 vs 8)
        self.f.insert_into_key_value_example('testUpdateRequired_myKey', 4)

        args = dict(
            login_user=MYSQL_CONNECTION_PARAMS['user'],
            name=MYSQL_CONNECTION_PARAMS['db'],
            login_password=MYSQL_CONNECTION_PARAMS['passwd'],
            login_host=MYSQL_CONNECTION_PARAMS['host'],
            table='key_value_example',
            identifiers=dict(name='testUpdateRequired_myKey'),
            values=dict(value='8'),
        )

        result = utils.ansible_check(args)
        self.assertIn('changed', result)
        self.assertTrue(result['changed'], 'a change (update) required is detected')
        self.assertRegexpMatches(result['msg'], 'update')
        self.assertEquals(self.f.count_key_value_example(), 1, 'no additional row has been inserted in check-mode')
