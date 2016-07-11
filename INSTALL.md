# Installation guidelines

This guide assumes Ubuntu to be target Linux distribution for installation.

## Configuring NTP

    sudo apt-get -y update
    sudo apt-get install -y ntp


## Installing Snort
Snort installation:

    sudo apt-get -y update
    sudo apt-get install -y zlib1g-dev liblzma-dev openssl libssl-dev
    sudo apt-get install -y snort

Next, run:

    sudo nano /etc/snort/snort.conf
    
and update the configuration file appropriatelly. More details can be found for example [here](https://s3.amazonaws.com/snort-org-site/production/document_files/files/000/000/090/original/Snort_2.9.8.x_on_Ubuntu_12-14-15.pdf?AWSAccessKeyId=AKIAIXACIED2SPMSC7GA&Expires=1463915430&Signature=JHyRc8FW45SP%2BPWYN474Y6UTvQc%3D). When you are done with editing restart Snort with:

    sudo service snort restart

**NOTE**: For some reason configuration option (default):

    config checksum_mode: all

Might not work as inteded. When Snort will not generate alerts, you can try switching it to:
    
    config checksum_mode: none
    
## Installing PulledPork

**NOTE**: PulledPork is not required for proper functionality. Rules can be downloaded manually and copied to the `/etc/snort/rules`. To generate correct `sid-msg.map`, `scripts/gensidmsgmap.py` can be used.

PulledPork must be installed from source. [This blog](http://donmizutani.com/pages/snort/setup/4-installing-pulledpork/) describes it in great detail.

## Installing Moloch

Moloch is a complex system to install. The proper installation guidelines can be found on the [project homepage](https://github.com/aol/moloch).

Moloch can be installed in the single host architecture. *easybutton* method can be used for this.

    mkdir -p /tmp/moloch_installation
    cd /tmp/moloch_installation
    git clone https://github.com/aol/moloch
    cd moloch
    sudo ./easybutton-build.sh
    sudo ./easybutton-singlehost.sh
    
The Moloch is automatically started after installation. To start the Moloch after system restart, you can use `scripts/start_moloch.sh`

By default, Moloch viewer binds sockets on `https://0.0.0.0:8005`.

## Installating analysis engine & API
**Prerequisites**:

1) [Installing RabbitMQ server](https://www.digitalocean.com/community/tutorials/how-to-install-and-manage-rabbitmq) -- for Celery broker
2) [Installing RethinkDB](https://www.rethinkdb.com/docs/install/ubuntu/) -- for storing analysis results. Please note that RethinkDB does not install *init.d* script automatically ([Start RethinkDB at system startup
](https://rethinkdb.com/docs/start-on-startup/))
3) [Installing supervisor](http://supervisord.org/installing.html) -- for process management

**NOTE:** Celery worker, API, and analysis engine are meant to reside on the same machine. Distributing these processes across more machines is possible, however, the following installation guidelines cannot be used in that case.

After installing the prerequisites, update the `config.sh` will proper values. Don't forget to create RethinkDB database and create directory for storing PCAPs (with correct file permission). API and Celery workers are running under `sqlianalysis` user. Project directory can be placed anywhere on the filesystem. After placing the directory you need to change the path (`/path/to/code`) in the following files:

* `install/sqli.supervisor.conf`
* `install/uwsgi.ini`

Next, run:
    
    bash ./install/install.sh

Done. If the previous script did not raise any error, web interface should be accessible on `0.0.0.0:8000`.
