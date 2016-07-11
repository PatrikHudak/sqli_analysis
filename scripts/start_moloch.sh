#!/bin/bash
# Start moloch deployed on single machine installed using easybutton

TDIR=/data/moloch
ES_SOCKET="127.0.0.1:9200"

${TDIR}/bin/run_es.sh
sleep 5

until curl -sS "http://$ES_SOCKET/_cluster/health?wait_for_status=yellow&timeout=5s"
do
    echo "Waiting for ES to start..."
    sleep 1
done
echo

echo "Running viewer..."
nohup ${TDIR}/bin/run_viewer.sh &

echo "Running capture..."
nohup ${TDIR}/bin/run_capture.sh &
