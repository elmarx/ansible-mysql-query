import unittest

from tests import utils
from tests.fixtures import Fixture
from tests.settings import MYSQL_CONNECTION_PARAMS

class MysqlQueryMultiCheckTest(unittest.TestCase):
    def setUp(self):
        self.f = Fixture()
        self.f.create_database()
        self.f.create_multicolumn_example()

    def tearDown(self):
        self.f.close()

    def testInsertRequired(self):
        args = dict(
            login_user=MYSQL_CONNECTION_PARAMS['user'],
            name=MYSQL_CONNECTION_PARAMS['db'],
            login_password=MYSQL_CONNECTION_PARAMS['passwd'],
            login_host=MYSQL_CONNECTION_PARAMS['host'],
            table='multicolumn_example',
            identifiers=dict(identifier1='elmar@athmer.org', identifier2='4', identifier3='testInsert'),
            values=dict(value1='8', value2='admin', value3="made up"),
        )

        result = utils.ansible_check(args)
        self.assertTrue(result['changed'], 'a required change is detected')
        self.assertRegexpMatches(result['msg'], 'insert')
        self.assertEquals(self.f.count_multicolumn_example(), 0, 'no row has been inserted in check-mode')

    def testNoChangeRequired(self):
        # insert a row that does not need to be updated
        self.f.insert_into_multicolumn_example(['elmar@athmer.org', 4, 'testNoChangeRequired'], [8, 'admin', 'made up'])

        args = dict(
            login_user=MYSQL_CONNECTION_PARAMS['user'],
            name=MYSQL_CONNECTION_PARAMS['db'],
            login_password=MYSQL_CONNECTION_PARAMS['passwd'],
            login_host=MYSQL_CONNECTION_PARAMS['host'],
            table='multicolumn_example',
            identifiers=dict(identifier1='elmar@athmer.org', identifier2='4', identifier3='testNoChangeRequired'),
            values={'value1': '8', 'value2': 'admin', 'value3': "made up"},
        )

        result = utils.ansible_check(args)
        self.assertIn('changed', result)
        self.assertFalse(result['changed'], 'no changed required is detected')
        self.assertEquals(self.f.count_multicolumn_example(), 1, 'no additional row has been inserted in check-mode')
