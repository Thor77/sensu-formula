'''
Sensu Go Execution module
'''
import json

from salt.utils.path import which

__virtualname__ = 'sensu'

base_cmd = ['sensuctl']


def __virtual__():
    '''
    Check requirements for this module
    '''
    if which('sensuctl'):
        return __virtualname__
    return False, 'sensuctl binary not found'


def _sensuctl(arguments, json_format=True):
    cmd = base_cmd + arguments
    if json_format:
        cmd.extend(['--format', 'json'])
    ret = __salt__['cmd.run_all'](cmd)
    if ret['retcode'] == 0 and json_format:
        ret['json'] = json.loads(ret['stdout'])
    return ret


# Subcommand 'check'
def list_checks():
    '''
    List checks

    CLI Example:

        salt '*' sensu.list_checks
    '''
    return _sensuctl(['check', 'list'])


def create_check(name, command, subscriptions, timeout=None, interval=None):
    '''
    Create a new check

    CLI Example:

        salt '*' sensu.create_check check-cpu 'check-cpu.sh -w 75 -c 90' linux
    '''
    if type(subscriptions) == list:
        subscriptions = ','.join(subscriptions)
    arguments = [
        'check', 'create', name, '-c', command, '-s', subscriptions
    ]
    if timeout:
        arguments.extend(['-t', timeout])
    if interval:
        arguments.extend(['-i', interval])
    r = _sensuctl(arguments, json_format=False)
    return r


def show_check(name):
    '''
    Show detailed information about a check

    CLI Example:

        salt '*' sensu.show_check check-cpu
    '''
    return _sensuctl(['check', 'info', name])


def check_present(name):
    '''
    Check if a check is present

    CLI Example:

        salt '*' sensu.check_present check-cpu
    '''
    return show_check(name)['retcode'] == 0
