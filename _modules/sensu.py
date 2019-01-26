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
    r = _sensuctl(arguments)
    return r
