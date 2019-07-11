{% from 'sensu/map.jinja' import sensu with context %}

{% for name, parameters in sensu.checks.iteritems() %}
sensu_check_{{ name }}:
  sensu.check_present:
    - name: {{ name }}
    - command: {{ parameters.command }}
    - subscriptions: {{ parameters.subscriptions }}
    {% if 'timeout' in parameters %}
    - timeout: {{ parameters.timeout }}
    {% endif %}
    {% if 'interval' in parameters %}
    - interval: {{ parameters.interval }}
    {% endif %}
{% endfor %}
