#!/bin/bash
sudo cp sink.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable sink.service
alias sink-run='sink-setup-env && python is_iot_sink/main.py'
alias sink-setup-env='cd /home/pi/is-iot-sink && source env/bin/activate && set -o allexport; source .env; set +o allexport'