'''
Sensu Go Execution module
'''
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


def list_checks():
    '''
    List checks

    CLI Example:

        salt '*' sensu.list_checks
    '''
    cmd = base_cmd + ['check', 'list']
    output = __salt__['cmd.run'](cmd).readlines()
    return output
