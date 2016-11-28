# X509 Certificate scanning tool
This is not actually zgrab.  Forgive the repo title.
## Setup
### zcerts.py
In order to use zcerts.py, the following tools must be installed
#### zmap
##### Debian-based Linux distros
```
sudo apt-get install zmap
```
##### RHEL/Fedora
NOTE: it is unclear whether ztee is installed as well when using yum
```
sudo yum install zmap
```
##### From source
Refer to https://zmap.io/download.html  
NOTE: I found on RHEL that unistr.h was missing when compiling from source. This can be installed via yum:
```
sudo yum install libunistring-devel
```
#### zgrab
Ensure go is installed and you have a valid $GOPATH setup (https://golang.org/doc/code.html). With go installed, just run the following:
```
go get github.com/zmap/zgrab
cd $GOPATH/src/github.com/zmap/zgrab
go build
```
#### Additional tips
Depending on your sudoer setup, you may encounter some issues when trying to run zmap as root. zmap and related tools are installed by default to /usr/local/sbin, and you may find that this path is not included on your secure_path variable in the sudoers file. You have the options if this is the case:
- edit the secure_path to include /usr/local/sbin
- copy zmap and the related binaries to a path included in secure_path
- setup zmap so that it does not require sudo privileges
Zmap can be given explicit privileges to capture network data without the need for root as below:  
  
```
setcap cap_net_raw=ep /usr/local/sbin/zmap
```

## Usage
### zcerts.py
The following command will gather certs for all hosts in the IPv4 address space listening on port 443:
```
python zcerts.py
```
However, zcerts.py allows for many options. Please consider zcerts.py's built-in help message below:
```
usage: zcerts.py [-h] [-p PORT] [-i IFACE] [-G MAC] [-r RATE] [-B BWIDTH]
                 [-b BLACKLIST] [-H HOST [HOST ...]] [--zmap-out ZMAP_OUT]
                 [--zgrab-out ZGRAB_OUT] [--zcerts-out ZCERTS_OUT]

Utilizes zmap and zgrab to enumerate HTTPS hosts and collect their certificate
chains

optional arguments:
  -h, --help            show this help message and exit
  -p PORT, --port PORT  the port to check for SSL/TLS on
  -i IFACE, --interface IFACE
                        the interface for zmap to attempt to use in its scan
  -G MAC, --gateway-mac MAC
                        the MAC of the gateway for a given iface
  -r RATE, --rate RATE  send rate in packets/sec
  -B BWIDTH, --bandwidth BWIDTH
                        send rate in bits/sec; support G, M, and K suffixes;
                        overrides --rate flag
  -b BLACKLIST, --blacklist BLACKLIST
                        filepath for blacklisted IPs/IP blocks; defaults to
                        /etc/zmap/blacklist.conf
  -H HOST [HOST ...], --hosts HOST [HOST ...]
                        the IP(s) to scan; accepts a list of IP addresses or
                        blocksin CIDR notation; defaults to the full IPv4
                        address space
  --zmap-out ZMAP_OUT   the file to output the results of the zmap scan to
  --zgrab-out ZGRAB_OUT
                        the file to output the results of the zgrab scan to
  --zcerts-out ZCERTS_OUT
                        the file to output the certs parsed from the zgrab
                        results to
```
