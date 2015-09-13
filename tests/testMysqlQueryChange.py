import unittest
from tests import utils
from tests.fixtures import Fixture
from tests.fixtures import MYSQL_CONNECTION_PARAMS


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
        self.assertEquals(self.f.count_change_example(), 1, 'a row has been inserted')
        row = self.f.query_change_example('do_backups', 4)
        self.assertItemsEqual((8, 'fifteen'), row[3:5], 'values were inserted')
        self.assertItemsEqual((16, 42, 'thirty-two'), row[5:8], 'row has been inserted with default values')

    def testUpdateRequired(self):
        self.f.insert_into_change_example(['do_syncs', '5'], [42, 'four'], [8, 16, 'bar'])

        args = dict(
            login_user=MYSQL_CONNECTION_PARAMS['user'],
            name=MYSQL_CONNECTION_PARAMS['db'],
            login_password=MYSQL_CONNECTION_PARAMS['passwd'],
            login_host=MYSQL_CONNECTION_PARAMS['host'],
            table='change_example',
            identifiers=dict(setting_name='do_syncs', setting_group_id='5'),
            values=dict(value1='43', value2='five'),
            defaults=dict(default1=9, default2='miow', bogus='foo')
        )

        result = utils.ansible_run(args)
        self.assertIn('changed', result)
        self.assertRegexpMatches(result['msg'], 'Successfully updated')
        self.assertEquals(self.f.count_change_example(), 1, 'no additional row has been inserted')
        row = self.f.query_change_example('do_syncs', '5')
        self.assertItemsEqual((43, 'five'), row[3:5], 'values have been updated')
        self.assertItemsEqual((8, 16, 'bar'), row[5:8], 'defaults have not been changed')

    def testNoChangeRequiredInNoCheckMode(self):
        """
        this is the case if no change is required, but we're not in check mode.
        :return:
        """
        self.f.insert_into_change_example(['no change required', 3], [1, 'one'], [1, 2, 'three'])

        args = dict(
            login_user=MYSQL_CONNECTION_PARAMS['user'],
            name=MYSQL_CONNECTION_PARAMS['db'],
            login_password=MYSQL_CONNECTION_PARAMS['passwd'],
            login_host=MYSQL_CONNECTION_PARAMS['host'],
            table='change_example',
            identifiers=dict(setting_name='no change required', setting_group_id=3),
            values=dict(value1=1, value2='one')
        )

        result = utils.ansible_run(args)
        self.assertIn('changed', result)
        self.assertFalse(result['changed'])




