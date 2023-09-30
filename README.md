# Bluetooth remote for LMS SqueezeBox player
## Basic features
* Play\Pause
* Prev\Next
* Volume -\+
* Sync
## Technologies
Project is created with:
* Python
* JSON
* Logitech Media Server API

## Launch
to run:
```
python3 btremote.py 
```

## Setup
settings file _btremote.conf_

key codes for "RemoterATV3 Consumer Control"
```
{
"volstep": "3",
"btdevice": "/dev/input/event0",
"player": "JBL white",
"server": "http://192.168.1.52:9000/jsonrpc.js",
"volup": "115",
"voldn": "114",
"pause": "353",
"prev": "105",
"next": "106", 
"mute": "113",
"home": "172",
"exit": "158",
"google": "217"
}
```

run `lsinput` and copy your bt device `/dev/input/event0` to settings file
```
root@orangepizero:~# lsinput
/dev/input/event0
bustype : BUS_BLUETOOTH
vendor  : 0x7545
product : 0x165
version : 257
name    : "RemoterATV3 Consumer Control"
phys    : "00:1a:7d:da:71:13"
uniq    : "54:03:84:e2:39:1f"
bits ev : (null) (null) (null) (null) (null)
```


## Install to OrangePi
### copy to pi
```
sh ssh_copy.sh
```
```
sshpass -p "12345" scp * root@192.168.1.65:/root/
```
### copy to /opt/
```
install_to_opt.sh
```
```
sudo mkdir /opt/btremote
sudo cp btremote.py /opt/btremote/
sudo cp btremote.conf /opt/btremote/
```
### install service
```
sh install_service.sh
```
```
sudo systemctl stop btremote.service
sudo cp btremote.service /lib/systemd/system/
sudo systemctl enable btremote.service
sudo systemctl daemon-reload
sudo systemctl start btremote.service

```
btremote.service
```
[Unit]
Description=Bluetooth Remote
After=multi-user.target
[Service]
Type=simple
WorkingDirectory=/opt/btremote
Restart=always
ExecStart=/usr/bin/python3 /opt/btremote/btremote.py
[Install]
WantedBy=multi-user.target
```

### must be installed before use
```
sudo apt-get install bluetooth
sudo apt install tlp
sudo apt install input-utils
sudo apt-get install python3
sudo apt install python3-pip
sudo apt install python3-dev
sudo pip3 install evdev
sudo pip3 install requests
bluetoothctl
lsinput
```