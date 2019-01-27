'''
Sensu Go State module
'''


def check_present(name, command, subscriptions, timeout=None, interval=None):
    '''
    Ensure a Sensu check is present

    name
        Name of the check

    command
        The command the check should run

    subscriptions
        Comma-separated list of topics check requests will be sent to

    timeout
        Timeout in seconds at which the check has to run

    interval
        Interval in seconds at which the check is run
    '''
    ret = {
        'name': name,
        'result': False,
        'changes': {},
        'comment': ''
    }
    present = __salt__['sensu.check_present'](name)
    if present:
        ret['result'] = True
        ret['commment'] = 'Check {} is already present.'.format(name)
        return ret
    if __opts__['test']:
        ret['result'] = None
        ret['comment'] = 'Check {} would be created.'.format(name)
        return ret
    change_ret = __salt__['sensu.create_check'](
        name, command, subscriptions, timeout, interval
    )
    if change_ret['retcode'] == 0:
        ret['result'] = True
        ret['comment'] = 'Check {} was created.'.format(name)
        ret['changes']['new'] = 'Check {} was created.'.format(name)
    else:
        ret['result'] = False
        ret['comment'] = change_ret['stdout']
    return ret
