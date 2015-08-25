import unittest
from tests import utils
from tests.fixtures import MYSQL_CONNECTION_PARAMS


class MysqlQueryTest(unittest.TestCase):
    """
    general robustness/configuration tests
    """
    def testFailForEmptyValues(self):
        args = dict(
            login_user='root',
            name='ansible-mysql-query-test',
            table='key_value_example',
        )

        result = utils.ansible_run(args)
        self.assertTrue(result['failed'])
        self.assertEqual(result['msg'], 'missing required arguments: identifiers')

    def testFailForTableMissing(self):
        args = dict(
            login_user=MYSQL_CONNECTION_PARAMS['user'],
            name=MYSQL_CONNECTION_PARAMS['db'],
            login_password=MYSQL_CONNECTION_PARAMS['passwd'],
            login_host=MYSQL_CONNECTION_PARAMS['host'],
            table='does_not_exist_table',
            identifiers=dict(not_relevant='bogus'),
            values=dict(not_relevant2='bogus'),
        )

        result = utils.ansible_run(args)
        self.assertTrue(result['failed'])
        self.assertEqual(result['msg'], 'No such table `does_not_exist_table`')
