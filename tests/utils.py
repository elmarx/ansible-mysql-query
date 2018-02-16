import json

from ansible.module_utils import basic
from ansible.module_utils._text import to_bytes


def set_module_args(**kwargs):
    args = json.dumps({'ANSIBLE_MODULE_ARGS': kwargs})
    basic._ANSIBLE_ARGS = to_bytes(args)


class AnsibleExitJson(Exception):
    pass


class AnsibleFailJson(Exception):
    pass


def exit_json(*args, **kwargs):
    if 'changed' not in kwargs:
        kwargs['changed'] = False
    raise AnsibleExitJson(kwargs)


def fail_json(*args, **kwargs):
    kwargs['failed'] = True
    raise AnsibleFailJson(kwargs)
