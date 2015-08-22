import ansible.runner
from ansible.inventory import Inventory

def ansible_run(args):
    """
    run the mysql_query module with ansible against localhost and return only the results for localhost (assuming
    localhost was contacted successfully)

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

    result = runner.run()
    if result['contacted'].has_key('localhost'):
        return result['contacted']['localhost']
    else:
        raise Exception('could not contact localhost at all')
