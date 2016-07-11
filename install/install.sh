#!/bin/bash
# Installs analysis engine & API

if ! [ -x "$(command -v virtualenv)" ]; then
	echo "virtualenv is not installed"
	exit 1
fi

if ! [ -x "$(command -v supervisorctl)" ]; then
	echo "supervisor is not installed"
	exit 1
fi

if [ ! -d "venv" ]; then
	echo "[+] Creating virtualenv..."
	virtualenv venv
fi

sudo adduser sqlianalysis

echo "[+] Installing packages..."
venv/bin/pip install -r ./install/requirements.txt

echo "[+] Running supervisor..."
sudo cp ./install/sqli.supervisor.conf /etc/supervisor/conf.d
sudo supervisorctl reread
sudo supervisorctl update

echo "[+] Testing subsystems..."
venv/bin/python ./install/test_subsystems.py

# TODO start uwsgi
echo "[+] OK"
