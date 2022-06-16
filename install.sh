# sudo chmod ugo+x install.sh
# ./install.sh

systemctl stop btremote.service
mkdir /opt/btremote
cp btremote.py /opt/btremote/
cp btremote.conf /opt/btremote/
cp btremote.service /lib/systemd/system/
sudo chmod u+x /opt/btremote/btremote.py
sudo systemctl enable btremote.service
sudo systemctl daemon-reload
sudo systemctl start btremote.service
sudo systemctl status btremote.service
