import unittest
import ansible.runner
from ansible.inventory import Inventory
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
            identifier_column='name',
            identifier='myKey',
            value_column='value',
            value='myValue',
        )

        runner = ansible.runner.Runner(
            module_name='mysql_query',
            module_args=args,
            inventory=Inventory(['localhost']),
            transport='local',
            check=True
        )

        result = runner.run()
        self.assertTrue(result['contacted']['localhost']['changed'], 'a required change is detected')

        cur = self.f.cursor()
        cur.execute('select COUNT(*) from `key_value_example`')
        self.assertEquals(cur.fetchone()[0], 0, 'no row has been inserted in checkmode')
