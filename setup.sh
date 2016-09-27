#!/bin/bash
apt-get -y update
apt-get -y install git python
cd ~/
git clone https://github.com/Sheidbrink/zgrab.git
cd zgrab
chmod +x ./setup_ztools.sh
./setup_ztools.sh
python zcerts.py -w ips.txt
