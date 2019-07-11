{% from 'sensu/map.jinja' import sensu with context %}

{% for name, parameters in sensu.assets.iteritems() %}
sensu_asset_{{ name }}:
  sensu.asset_present:
    - name: {{ name }}
    - url: {{ parameters.url }}
    - sha512: {{ parameters.sha512 }}
{% endfor %}
