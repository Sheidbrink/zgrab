#!/bin/bash

# *** IMPORTANT ***
#
# Before running this script, you MUST setup the following environment
# variables. Consider adding them to your bashrc for persistence.
#
#export PATH=$PATH:/usr/local/go/bin
#export GOPATH=$HOME/go-code
#export PATH=$PATH:$GOPATH/bin

# Additionally you may wish to configure the following env vars if you 
# wish to use a specific golang version. If these vars are not set, the
# script will default to v1.7 for 64-bit linux 
if [ -z "$GO_VERSION" ]; then GO_VERSION="1.7"; fi
if [ -z "$GO_OS" ]; then GO_OS="linux"; fi
if [ -z "$GO_ARCH" ]; then GO_ARCH="amd64"; fi

GO_DISTRO="go${GO_VERSION}.${GO_OS}-${GO_ARCH}.tar.gz"

printf ">>>SETUP>>> Installing dependencies via apt...\n\n"
sudo apt-get -y install git build-essential cmake libgmp3-dev libpcap-dev gengetopt byacc flex libjson0-dev libunistring-dev
rc=$?; if [[ $rc != 0 ]]; then
printf "\n\n>>>SETUP>>> Installing dependecies failed!\n" 
exit 
fi

printf "\n>>>SETUP>>> Cloning zmap repo...\n\n"
git clone git://github.com/zmap/zmap.git

rc=$?; if [[ $rc != 0 ]]; then
printf "\n\n>>>SETUP>>> Cloning repo failed!\n" 
exit 
fi

pushd zmap

printf "\n>>>SETUP>>> C-making the zmap executable...\n\n"
sudo cmake -DENABLE_DEVELOPMENT=OFF
rc=$?; if [[ $rc != 0 ]]; then
printf "\n\n>>>SETUP>>> Cmake failed!\n" 
exit 
fi

printf "\n>>>SETUP>>> Installing zmap...\n\n"
sudo make install
rc=$?; if [[ $rc != 0 ]]; then
printf "\n\n>>>SETUP>>> Installing zmap failed!\n" 
exit 
fi

popd

printf "\n>>>SETUP>>> Retrieving golang tarball...\n\n"
wget https://storage.googleapis.com/golang/${GO_DISTRO}
rc=$?; if [[ $rc != 0 ]]; then
printf "\n\n>>>SETUP>>> Retrieving tarball failed!\n" 
exit 
fi

printf "\n>>>SETUP>>> Unpacking golang to /usr/local...\n\n"
sudo tar -C /usr/local -xzf $GO_DISTRO
rc=$?; if [[ $rc != 0 ]]; then
printf "\n\n>>>SETUP>>> Unpacking tarball failed!\n" 
exit 
fi


printf "\n>>>SETUP>>> Create directory for golang projects...\n\n"
mkdir $HOME/go-code
rc=$?; if [[ $rc != 0 ]]; then
printf "\n\n>>>SETUP>>> Creating directory failed!\n" 
exit 
fi

printf "\n>>>SETUP>>> Retrieving zgrab...\n\n"
go get github.com/zmap/zgrab
rc=$?; if [[ $rc != 0 ]]; then
printf "\n\n>>>SETUP>>> Retrieving zgrab failed!\n" 
exit 
fi

printf "\n>>>SETUP>>> Building/installing zgrab...\n\n"
pushd $GOPATH/src/github.com/zmap/zgrab
go build
popd
rc=$?; if [[ $rc != 0 ]]; then
printf "\n\n>>>SETUP>>> Building/installing zgrab failed!\n" 
exit 
fi

printf "\n>>>SETUP>>> Setup complete!\n"

