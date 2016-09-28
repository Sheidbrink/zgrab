#!/bin/bash
apt-get -y install git
git clone https://github.com/Sheidbrink/zgrab.git
export PATH=$PATH:/usr/local/go/bin
export GOPATH=$HOME/go-code
export PATH=$PATH:$GOPATH/bin
cd zgrab
./setup_ztools.sh
python zcerts.py -w ips.txt
