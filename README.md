# Python programmable Prometheus exporter

[![Docker Repository on Quay](https://quay.io/repository/codeaffen/p3exporter/status "Docker Repository on Quay")](https://quay.io/repository/codeaffen/p3exporter)
[![PyPI version](https://badge.fury.io/py/p3exporter.svg)](https://badge.fury.io/py/p3exporter)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/0c608f1a8a18412ba2031853b8963be7)](https://www.codacy.com/gh/codeaffen/p3exporter/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=codeaffen/p3exporter&amp;utm_campaign=Badge_Grade)
[![Documentation Status](https://readthedocs.org/projects/p3exporter/badge/?version=develop)](https://p3exporter.readthedocs.io/en/latest/?badge=latest)

p3exporter will help any DevOps to quickstart its Prometheus exporter development. It is completly written in python and provides a facility for pluggable metric collectors.
The exporter comes with real life exporters to illustrate how it works but is also intended to use as a framework for completely custom collectors.

The included collectors were only tested on linux systems. Other \*nix derivates are not supported by us but you are welcome to contribute to bring this exporter to a broader audience.

## Installation and Running

There are different ways to run the exporter on your system. Our exporter listen on tcp/5876 by default. You can change this by adding `--port` or `-p` option with the port of your choice.

### Running exporter as docker container

The simplest way will is to start it as docker container.
The container image is hosted on [quay.io](https://quay.io/repository/codeaffen/p3exporter) and [dockerhub](https://hub.docker.com/r/codeaffen/p3exporter) and the `latest` tag represent the `develop` branch of the github repository.
If you want to use a given version you can us the verson string (e.g. `v1.0.0`) as tag instead.

```text
docker run -d --net="host" --pid="host" -v "/:/host:ro,rslave" codeaffen/p3exporter:latest
```

### Installing from pypi.org

We also release all versions on [pypi](https://pypi.org/project/p3exporter/) so you can use `pip` to install the exporter and run it locally.

```text
pip install p3exporter
```

This will install the exporter and all of its dependencies. Now you can start it as every other program. You need to provide a valid configuration file either by adding `--config` or `-c` option with path to your `p3.yml` file or by defining an environment variable `P3E_CONFIG` which points to your configuration.

```text
$ curl --silent https://raw.githubusercontent.com/codeaffen/p3exporter/develop/p3.yml --output ~/tmp/p3.yml
$ p3exporter --config ~/tmp/p3.yml
INFO:root:Collector 'example' was loaded and registred successfully
INFO:root:Collector 'loadavg' was loaded and registred successfully
INFO:root:Collector 'netdev' was loaded and registred successfully
INFO:root:Start exporter, listen on 5876
```

### Install from repository

The last option to install and run p3exporter is to install it from a local clone of our [github repository](https://github.com/codeaffen/p3exporter).

```text
$ git clone https://github.com/codeaffen/p3exporter.git
Cloning into 'p3exporter'...
remote: Enumerating objects: 158, done.
remote: Counting objects: 100% (158/158), done.
remote: Compressing objects: 100% (112/112), done.
remote: Total 158 (delta 63), reused 101 (delta 28), pack-reused 0
Receiving objects: 100% (158/158), 188.37 KiB | 1.08 MiB/s, done.
Resolving deltas: 100% (63/63), done.
$ cd p3exporter
$ pip install -e .
```

From now you can run it with:

```text
$ p3exporter
INFO:root:Collector 'example' was loaded and registred successfully
INFO:root:Collector 'loadavg' was loaded and registred successfully
INFO:root:Collector 'netdev' was loaded and registred successfully
INFO:root:Start exporter, listen on 5876
```

## Building your own container image

To build your own container image you can use the dockerfile which is delivered in our github repository.
This file is also used to create our images on quay.io or dockerhub.

```text
$ docker build -t p3exporter .
Sending build context to Docker daemon  181.8kB
...
Successfully built a6bdf60489f5
Successfully tagged p3exporter:latest
```

Now you can start the container. Here you can use the command from above. You have just to use your image

```text
docker run -d --net="host" --pid="host" -v "/:/host:ro,rslave" p3exporter:latest
```

## Collectors

| Name | Description |
| ---- | ----------- |
| example | example collector that actually does nothing but show how long a function has been executed |
| loadavg | collects average load in 1, 5 and 15 minutes interval |
| netdev | collects netword device information and statistics |

### Activation and Deactivation of collectors

To activate or deactive collectors you have to configure it in `p3.yml` within the `collectors` list. All collectors listed in this list will be activated a start time of p3exporter. If there are any issues e.g. collector can't be found or has failures in code a warning will be shown and it will not be activated.

```yaml
exporter_name: "Python prammable Prometheus exporter"
collectors:
  - example
  - loadavg
  - netdev
collector_opts:
  netdev:
    log_level: DEBUG
    whitelist:
    blacklist:
      - docker0
      - lo
logging:
  - name: root
    level: INFO
  - name: foomodule.barcollector
    level: WARNING
    target: /path/to/my/collector/logfile.log
```

The `collector_opts` can optionally contain a `log_level` entry which
will configure the logging-level for that specific collector. Note that
support for this must be implemented by each individual collector.

Logging can optionally be configured for any logger. The entries must
specify the name of the logger and can optionally specify a
logging-level (default: stay at whatever the default logging-level for
that logger is) and/or can specify a file to write the log to (default:
log to stderr).

### Start-up Configuration

You can define two fundamental Parameters on program start-up. The following table summarized you options:

| Parameter | Environment variable | Default | Description |
| --------- | -------------------- | ------- | ----------- |
| --config  | P3E_CONFIG | p3.yml | Path to the used configuration file |
| --port | P3E_PORT | 5876 | TCP port on which the p3exporter listen for connections |
