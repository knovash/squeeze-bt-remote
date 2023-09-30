#!/usr/bin/env bash
# sudo chmod +x *.sh

sudo systemctl stop btremote.service
sudo cp btremote.service /lib/systemd/system/
sudo systemctl enable btremote.service
sudo systemctl daemon-reload
sudo systemctl start btremote.service

$SHELL

