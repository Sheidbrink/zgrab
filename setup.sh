#!/bin/bash
apt-get -y install zmap
apt-get -y install golang
apt-get -y install git
mkdir ~/GoPath
export GOPATH=~/GoPath
go get github.com/zmap/zgrab
cd ~/GoPath/src/github.com/zmap/zgrab/
go build
