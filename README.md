# Automated SQL injection analysis
This project aims to automate the analysis of SQL injection incidents using IDS and full PCAP *(Moloch)*.

It was created as an implementation part of my bachelor thesis. The thesis can be found [here](https://is.muni.cz/th/422182/fi_b/thesis.pdf).

## Prerequisites
* Moloch
* Snort
* RethinkDB
* Python 2.7

## Installation
Installation instructions can be found in `./INSTALL.md`

## Structure

```
+-- config.json                                         Main configuration file
+-- engine.py                                           Analysis engine implementation
+-- forwarder.py                                        Alert forwarder implemenetation
+-- install/                                            Installation files
|   +-- install.sh                                      Main installation script
|   +-- sqli.supervisor.conf                            supervisor configuration
|   +-- requirements.txt                                List of Python packages
|   +-- test_subsystems.py                              Script testing proper functionality of subsystems
|   +-- uwsgi.ini                                       uWSGI configuration file
+-- INSTALL.md                                          Installation guidelines
+-- modules/                                            Analysis modules
|   +-- __init__.py                                     Module initialization
|   +-- canary.py                                       Canary detection module
|   +-- connections.py                                  Moloch connections module
|   +-- ipinfo.py                                       Attacker IP address information retrieval
|   +-- statistics.py                                   Statistics module
|   +-- utils.py                                        Helper function (e.g. extracting requests from PCAP)
|   +-- websiteinfo.py                                  Detecting website technologies using Wappalyzer
+-- README.md                                           This file
+-- scripts/                                            Various useful scripts
+-- ui/                                                 Web interface files
|   +-- static/                                         Static files (css, javascript, images)
|   +-- templates/                                      Jinja2 templates
```


## Configuration

Configuration details are provided in `./config.json`

**Celery**
* *celery.BROKER_URL* -- address for Celery broker. Default is AMQP (**RabbitMQ**)

**Forwarder (Snort)**
* *forwarder.sid-map* -- path to sid-msg.map which maps signatures IDs to textual description
* *forwarder.gid-map* -- path to gen-msg.map which maps generator IDs to textual description
* *forwarder.url* -- API endpoint for POSTing new alerts
* *forwarder.logs_dir* -- Snort logging directory
* *forwarder.logs_prefix* -- prefix of Snort log files

**Jobs**
* *job_freeze* -- time (in seconds) to postpone the analysis
* *pcap_directory* -- directory for storing PCAPs from Moloch

**Moloch**
* *moloch.viewer* -- URL for Moloch viewer
* *moloch.username* -- username for Moloch viewer
* *moloch.password* -- password for Moloch viewer

**RethinkDB**
* *rethinkdb.host* -- hostname / IP address of machine where RethinkDB is running
* *rethinkdb.port* -- port for RethinkDB instance
* *rethinkdb.db* -- name of database where results are stored

## Alert format
An alert must be delivered to API in this format:
```
alert = {
    'src_ip': '', # Source IP number
    'src_port': '', # Source port number
    'dest_ip': '', # Destination IP address
    'dest_port': '', # Destination port number
    'timestamp': '', # Timestamp of received alert
    'detection': '', # Detection mechanism
    'meta': {
        # Meta information about alert (description etc.)
    }
}
```
