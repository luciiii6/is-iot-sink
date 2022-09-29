#!/bin/bash
sudo touch /usr/local/bin/startup.sh
sudo chmod u+x /usr/local/bin/startup.sh
sudo echo "#!/bin/bash" | sudo tee -a /usr/local/bin/startup.sh
sudo echo "cd /home/pi/is-iot-sink" | sudo tee -a /usr/local/bin/startup.sh
sudo echo "source env/bin/activate" | sudo tee -a /usr/local/bin/startup.sh
sudo echo "python is_iot_sink/main.py" | sudo tee -a /usr/local/bin/startup.sh
#copy the service file to be started by systemd
sudo cp sink.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable sink.service