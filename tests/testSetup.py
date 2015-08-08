import unittest
import ansible.runner
from ansible.inventory import Inventory


class AnsibleTest(unittest.TestCase):
    def test_ping(self):
        runner = ansible.runner.Runner(
            module_name='ping',
            module_args='',
            forks=10,
            inventory=Inventory(['localhost']),
            transport='local'
        )
        datastructure = runner.run()
        self.assertEqual(len(datastructure['contacted']), 1)
        self.assertEqual(len(datastructure['dark']), 0)
