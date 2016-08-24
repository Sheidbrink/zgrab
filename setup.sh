#!/bin/bash
apt-get -y install zmap
apt-get -y install golang
apt-get -y install git
apt-get -y install tmux
mkdir ~/GoPath
export GOPATH=~/GoPath
go get github.com/zmap/zgrab
cd ~/GoPath/src/github.com/zmap/zgrab/
go build
cd ~/
git clone https://github.com/Sheidbrink/zgrab.git
cd zgrab
python zcerts.py -w ips.txt
