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

    @unittest.skip("not yet implemented after refactoring")
    def testCheckInsertRequired(self):
        args = dict(
            login_user='root',
            name='ansible-mysql-query-test',
            table='key_value_example',
            identifier_column='name',
            identifier='myKey',
            value_column='value',
            value='myValue',
        )

        result = utils.ansible_run(args)
        self.assertTrue(result['contacted']['localhost']['changed'], 'a required change is detected')
        self.assertEquals(self.f.count_key_value_example(), 0, 'no row has been inserted in check-mode')

    def testCheckNoChangeRequired(self):
        # insert a row that does not need to be updated
        self.f.insert_into_key_value_example('myKey', 42)

        args = dict(
            login_user='root',
            name='ansible-mysql-query-test',
            table='key_value_example',
            values='name=myKey value=42',
        )

        result = utils.ansible_run(args)
        self.assertFalse(result['contacted']['localhost']['changed'], 'no changed required is detected')
        self.assertEquals(self.f.count_key_value_example(), 1, 'no additional row has been inserted in check-mode')
