{% from 'sensu/map.jinja' import sensu with context %}

sensu_backend_pkg:
  pkg.installed:
    - name: {{ sensu.lookup.backend.pkg }}

sensu_backend_cfg:
  file.managed:
    - name: {{ sensu.lookup.backend.cfg }}
    - source: salt://sensu/files/config.yml
    - template: jinja
    - context:
        config: {{ sensu.backend }}
    - require:
      - pkg: sensu_backend_pkg

sensu_backend_service:
  service.running:
    - name: {{ sensu.lookup.backend.service }}
    - require:
      - pkg: sensu_backend_pkg
    - watch:
      - file: sensu_backend_cfg
    - enable: true
