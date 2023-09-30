#!/usr/bin/env bash

sudo chmod u+x *.py
sudo chmod u+x *.sh

sudo mkdir /opt/btremote
sudo cp btremote.py /opt/btremote/
sudo cp btremote.conf /opt/btremote/

$SHELL
