#!/bin/bash
apt-get -y update

apt-get install -y apache2 php libapache2-mod-php
service httpd start
update-rc.d apache2 enable
groupadd www
usermod -a -G www ubuntu
chown -R root:www /var/www
chmod 2775 /var/www
find /var/www -type d -exec chmod 2775 {} +
find /var/www -type f -exec chmod 0664 {} +
rm -f /var/www/html/index.html
echo "<?php header("Location: https://internet.byu.edu"); ?>" > /var/www/html/index.php

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
