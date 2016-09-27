#!/bin/bash
apt-get -y install git
git clone https://github.com/Sheidbrink/zgrab.git
cd zgrab
./setup_ztools.sh
python zcerts.py -w ips.txt
