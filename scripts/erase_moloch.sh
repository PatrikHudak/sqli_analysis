#!/bin/bash

TDIR=/data/moloch
ES_SOCKET="127.0.0.1:9200"

echo "[-] Erasing ES (including login credentials)..."
${TDIR}/db/db.pl ${ES_SOCKET} init

read -p "Remove all PCAPs? [y/N] " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
  echo "[-] Removing PCAP files..."
  rm ${TDIR}/raw/*.pcap
fi

echo "[-] Adding admin"
${TDIR}/bin/node ${TDIR}/viewer/addUser.js -c ${TDIR}/etc/config.ini admin "Admin" admin -admin

echo "[OK]"
