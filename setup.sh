#!/bin/bash
apt-get -y update
apt-get -y install git python
cd ~/
git clone https://github.com/Sheidbrink/zgrab.git
export PATH=$PATH:/usr/local/go/bin
export GOPATH=$HOME/go-code
export PATH=$PATH:$GOPATH/bin
cd zgrab
chmod +x ./setup_ztools.sh
./setup_ztools.sh
python zcerts.py -w ips.txt
