{% from 'sensu/map.jinja' import sensu with context %}

{% for name, attributes in sensu.checks.items() %}
{% set statefile = salt['temp.file'](prefix='state-') %}
sensu_check_cfg_{{ name }}:
  file.managed:
    - name: {{ statefile }}
    - contents: {{ attributes|json }}

sensu_check_{{ name }}:
  cmd.run:
    - name: 'sensuctl check create --file {{ statefile }}'
{% endfor %}
