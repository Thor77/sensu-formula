{% from 'sensu/map.jinja' import sensu with context %}

{% for name, parameters in sensu.checks.iteritems() %}
sensu_check_{{ name }}:
  sensu.check_present:
    - name: {{ name }}
    - command: {{ parameters.command }}
    - subscriptions: {{ parameters.subscriptions }}
    - timeout: {{ parameters.get('timeout') }}
    - interval: {{ parameters.get('interval') }}
{% endfor %}
