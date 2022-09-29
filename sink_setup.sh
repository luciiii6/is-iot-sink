#!/bin/bash
sudo touch /usr/local/bin/startup.sh
sudo chmod u+x /usr/local/bin/startup.sh
sudo echo "#!/bin/bash" | sudo tee -a /usr/local/bin/startup.sh
sudo echo 'shopt -s expand_aliases' | sudo tee -a /usr/local/bin/startup.sh
sudo echo "alias sink-run='sink-setup-env && python is_iot_sink/main.py'" | sudo tee -a /usr/local/bin/startup.sh
sudo echo "alias sink-setup-env='cd /home/pi/is-iot-sink && source env/bin/activate && set -o allexport; source .env; set +o allexport'" | sudo tee -a /usr/local/bin/startup.sh
sudo echo "sink-run" | sudo tee -a /usr/local/bin/startup.sh
#copy the service file to be started by systemd
sudo cp sink.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable sink.service