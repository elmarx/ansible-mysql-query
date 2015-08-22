import unittest

from tests import utils
from tests.fixtures import Fixture

class MysqlQueryCheck(unittest.TestCase):
    def testFailForEmptyValues(self):
        args = dict(
            login_user='root',
            name='ansible-mysql-query-test',
            table='key_value_example',
        )

        result = utils.ansible_run(args)
        self.assertTrue(result['failed'])
        self.assertEqual(result['msg'], 'missing required arguments: identifiers')