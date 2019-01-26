'''
Sensu Go Execution module
'''
import json

from salt.utils.path import which

__virtualname__ = 'sensu'

base_cmd = ['sensuctl', '--format', 'json']


def __virtual__():
    '''
    Check requirements for this module
    '''
    if which('sensuctl'):
        return __virtualname__
    return False, 'sensuctl binary not found'


def _sensuctl(arguments):
    cmd = base_cmd + arguments
    return json.loads(__salt__['cmd.run'](cmd))


def list_checks():
    '''
    List checks

    CLI Example:

        salt '*' sensu.list_checks
    '''
    return _sensuctl(['check', 'list'])
