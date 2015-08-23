import ansible.runner
from ansible.inventory import Inventory

def ansible_check(args):
    return ansible_run(args, check=True)

def ansible_run(args, check=False):
    """
    run the mysql_query module with ansible against localhost and return only the results for localhost (assuming
    localhost was contacted successfully)

    :param args:
    :return:
    """
    complex_args, module_args = [], []
    for key, value in args.items():
        (complex_args if isinstance(value, dict) else module_args).append((key, value))

    runner = ansible.runner.Runner(
        module_name='mysql_query',
        module_args=dict(module_args),
        complex_args=dict(complex_args),
        inventory=Inventory(['localhost']),
        transport='local',
        check=check
    )

    result = runner.run()
    if result['contacted'].has_key('localhost'):
        return result['contacted']['localhost']
    else:
        raise Exception('could not contact localhost at all: %s' % str(result['dark']['localhost']))
