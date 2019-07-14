'''
Sensu Go Execution module
'''
import json

from salt.utils.path import which

__virtualname__ = 'sensu'

base_cmd = ['sensuctl']
base_manifest = {
    'api_version': 'core/v2',
    'metadata': {
        'namespace': 'default'
    }
}


def __virtual__():
    '''
    Check requirements for this module
    '''
    if which('sensuctl'):
        return __virtualname__
    return False, 'sensuctl binary not found'


def _sensuctl(arguments, json_format=True, stdin=None):
    cmd = base_cmd + arguments
    if json_format:
        cmd.extend(['--format', 'json'])
    ret = __salt__['cmd.run_all'](cmd, stdin=stdin)
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


def update_check_attribute(name, attribute, value):
    '''
    Update an attribute of a check

    CLI Example:

        salt '*' sensu.update_check_attribute command /bin/new-command
    '''
    return _sensuctl(
        ['check', 'set-{}'.format(attribute), name, value],
        json_format=False
    )


# Subcommand 'asset'
def list_assets():
    '''
    List assets

    CLI Example:

        salt '*' sensu.list_assets
    '''
    return _sensuctl(['asset', 'list'])


def create_asset(name, url, sha512, filters=[]):
    '''
    Create a new asset

    CLI Example:

        salt '*' sensu.create_asset sensu-pagerduty-handler https://... e93ec..
    '''
    manifest = base_manifest
    manifest['type'] = 'Asset'
    manifest['metadata']['name'] = name
    manifest['spec'] = {
        'url': url,
        'sha512': sha512,
        'filters': filters
    }
    return _sensuctl(['create'], json_format=False, stdin=json.dumps(manifest))


def show_asset(name):
    '''
    Show detailed information about an asset

    CLI Example:

        salt '*' sensu.show_asset sensu-pagerduty-handler
    '''
    return _sensuctl(['asset', 'info', name])


def asset_present(name):
    '''
    Check if an asset is present

    CLI Example:

        salt '*' sensu.asset_present sensu-pagerduty-handler
    '''
    return show_asset(name)['retcode'] == 0


def update_asset(name):
    '''
    Update an asset

    CLI Example:

        salt '*' sensu.update_asset sensu-pagerduty-handler
    '''
    return _sensuctl(['asset', 'update', name])
