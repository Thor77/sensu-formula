{% from 'sensu/map.jinja' import sensu with context %}

{% if grains.os_family == 'RedHat' %}
sensu_repo:
  pkgrepo.managed:
    - name: sensu_stable
    - baseurl: https://packagecloud.io/sensu/stable/el/{{ grains['osmajorrelease'] }}/$basearch
    - gpgcheck: false
    - repo_gpgcheck: true
    - gpgkey: https://packagecloud.io/sensu/stable/gpgkey
{% endif %}

sensu_agent_pkg:
  pkg.installed:
    - name: {{ sensu.lookup.agent.pkg }}

sensu_agent_cfg:
  file.managed:
    - name: {{ sensu.lookup.agent.cfg }}
    - source: salt://sensu/files/config.yml
    - template: jinja
    - context:
        config: {{ sensu.agent }}
    - require:
      - pkg: sensu_agent_pkg

sensu_agent_service:
  service.running:
    - name: {{ sensu.lookup.agent.service }}
    - require:
      - pkg: sensu_agent_pkg
    - watch:
      - file: sensu_agent_cfg
    - enable: true
