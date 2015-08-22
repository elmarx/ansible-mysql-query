import unittest

from tests import utils
from tests.fixtures import Fixture

class MysqlQueryTest(unittest.TestCase):
    def setUp(self):
        self.f = Fixture()
        self.f.create_database()
        self.f.create_key_value_example()

    def tearDown(self):
        self.f.close()

    def testCheckInsertRequired(self):
        args = dict(
            login_user='root',
            name='ansible-mysql-query-test',
            table='key_value_example',
            identifiers='name=testCheckInsertRequired_myKey',
            values='value=42',
        )

        result = utils.ansible_run(args)
        self.assertTrue(result['changed'], 'a required change is detected')
        self.assertRegexpMatches(result['msg'], 'insert')
        self.assertEquals(self.f.count_key_value_example(), 0, 'no row has been inserted in check-mode')

    def testFailForEmptyValues(self):
        args = dict(
            login_user='root',
            name='ansible-mysql-query-test',
            table='key_value_example',
        )

        result = utils.ansible_run(args)
        self.assertTrue(result['failed'])
        self.assertEqual(result['msg'], 'missing required arguments: identifiers')

    def testCheckNoChangeRequired(self):
        # insert a row that does not need to be updated
        self.f.insert_into_key_value_example('testCheckNoChangeRequired_myKey', 42)

        args = dict(
            login_user='root',
            name='ansible-mysql-query-test',
            table='key_value_example',
            identifiers='name=testCheckNoChangeRequired_myKey',
            values='value=42',
        )

        result = utils.ansible_run(args)
        self.assertIn('changed', result)
        self.assertFalse(result['changed'], 'no changed required is detected')
        self.assertEquals(self.f.count_key_value_example(), 1, 'no additional row has been inserted in check-mode')

    def testCheckUpdateRequired(self):
        # insert a row that does not need to be updated
        self.f.insert_into_key_value_example('testCheckUpdateRequired_myKey', 4)

        args = dict(
            login_user='root',
            name='ansible-mysql-query-test',
            table='key_value_example',
            identifiers='name=testCheckUpdateRequired_myKey',
            values='value=8',
        )

        result = utils.ansible_run(args)
        self.assertIn('changed', result)
        self.assertTrue(result['changed'], 'a change (update) required is detected')
        self.assertRegexpMatches(result['msg'], 'update')
        self.assertEquals(self.f.count_key_value_example(), 1, 'no additional row has been inserted in check-mode')