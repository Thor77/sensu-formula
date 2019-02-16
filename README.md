# sensu-formula
Formula to install and setup [Sensu Go](https://github.com/sensu/sensu-go/).

# Available states

## `sensu.agent`
Install and configure Sensu Go agent.

Reads config from `sensu:agent` pillar.

## `sensu.cli`
Install Sensu Go CLI.

## `sensu.backend`
Install and configure Sensu Go backend.

Reads config from `sensu:backend` pillar.

## `sensu.checks`
Configure Sensu Go checks by calling the CLI.

```yaml
sensu:
  checks:
    check-cpu:
      command: '/usr/lib/sensu-scripts/check-cpu.sh -w 75 -c 90'
      subscriptions:
        - linux
      interval: 60
      timeout: 3
```
