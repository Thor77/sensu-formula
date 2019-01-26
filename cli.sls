{% from 'sensu/map.jinja' import sensu with context %}

sensu_cli_pkg:
  pkg.installed:
    - name: {{ sensu.lookup.cli.pkg }}
