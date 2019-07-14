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
        if __opts__['test']:
            ret['result'] = None
            ret['comment'] = 'Check {} would be updated.'.format(name)
            return ret
        # compare current check with target
        current_state = __salt__['sensu.show_check'](name)['json']
        target_state = {
            'command': command,
            'subscriptions': subscriptions,
            'timeout': timeout,
            'interval': interval
        }
        for attribute, target_value in target_state.items():
            current_value = current_state[attribute]
            if target_value and current_value != target_value:
                r = __salt__['sensu.update_check_attribute'](
                    name, attribute, target_value
                )
                if r['retcode'] == 0:
                    ret['changes'][attribute] = {
                        'old': current_value,
                        'new': target_value
                    }
                else:
                    ret['result'] = False
                    ret['comment'] = r['stderr'] or r['stdout']
                    return ret
        ret['result'] = True
        if ret['changes']:
            ret['comment'] = 'Check {} was successfully updated.'.format(name)
        else:
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


def asset_present(name, url, sha512, filters=[]):
    '''
    Ensure an asset is present

    name
        Name of the asset

    url
        URL location of the asset

    sha512
        Checksum of the asset

    filters
        Queries used by an entity to determine if it should include the asset
    '''
    ret = {}
    present = __salt__['sensu.asset_present'](name)
    if present:
        ret['result'] = True
        ret['commment'] = 'Asset {} is already present.'.format(name)
        return ret
    if __opts__['test']:
        ret['result'] = None
        ret['comment'] = 'Asset {} would be created.'.format(name)
        return ret
    change_ret = __salt__['sensu.create_asset'](name, url, sha512, filters)
    if change_ret['retcode'] == 0:
        ret['result'] = True
        comment = 'Asset {} was created.'.format(name)
        ret['comment'] = comment
        ret['changes']['new'] = comment
    else:
        ret['result'] = False
        ret['comment'] = change_ret['stdout']
    return ret
