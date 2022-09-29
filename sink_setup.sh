#!/bin/bash
sudo cp sink.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable sink.service