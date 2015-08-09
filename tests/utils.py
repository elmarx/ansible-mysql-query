import ansible.runner
from ansible.inventory import Inventory

def ansible_run(args):
    """
    run the mysql_query module with ansible against localhost

    :param args:
    :return:
    """
    runner = ansible.runner.Runner(
        module_name='mysql_query',
        module_args=args,
        inventory=Inventory(['localhost']),
        transport='local',
        check=True
    )

    return runner.run()