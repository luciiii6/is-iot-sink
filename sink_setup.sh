#!/bin/bash
alias sink-run='sink-setup-env && python is_iot_sink/main.py'
alias sink-setup-env='cd /home/pi/is-iot-sink && source env/bin/activate && set -o allexport; source .env; set +o allexport'
sudo touch /usr/local/bin/startup.py
sudo chmod u+x /usr/local/bin/startup.python
sudo echo "#!/bin/bash" | sudo tee -a /usr/local/bin/startup.py
sudo echo "sink-run" | sudo tee -a /usr/local/bin/startup.py
sudo cp sink.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable sink.service