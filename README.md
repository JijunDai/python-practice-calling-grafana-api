# call-grafana-api


## Getting started

It's a python practice project to access Grafana through Grafana API

- install dependencies according to the dependencies.txt, or use poetry as package manager. The dependencies.txt file is generated from poetry's pyproject.toml.

## Functions

- Search alerts with given notifications

```
python call_grafana_api --help

# get all alert notifications
python call_grafana_api -n

# search a given notification
python call_grafana_api -u [UID]
```

