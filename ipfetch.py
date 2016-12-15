# ipfetch.py
# 
# Given a a list of hostnames, this script will output one file of just the 
# resolved IPs and another file of the IP-host pairs. The list of IPs is given
# as in put to zmap and the list of IP-host pairs will be used to support SNI 
# in zgrab

import csv
import argparse
import socket

IPS_OUT_DEFAULT = "ips.out"
PAIRS_OUT_DEFAULT = "ip-host.csv"

# setup a robust argument parser
def parse_args():
    parser = argparse.ArgumentParser(
        prog="ipfetch.py",
        description="Takes a list of hostnames and attempts to resolve them \
        to IPs via DNS requests; outputs a file listing just the IPs as well \
        as a CSV of IP-host pairs")
    parser.add_argument(
        "host_file",
        metavar="HOST_FILE",
        type=str,
        help="the file to read in the hostnames from")
    parser.add_argument(
        "-o",
        "--ips-out",
        metavar="IPS_OUT",
        type=str,
        help="the file to output the resolved IPs to; defaults to ips.out")
    parser.add_argument(
        "-O",
        "--pairs-out",
        metavar="PAIRS_OUT",
        type=str,
        help="the file to output the IP-host pairs to; defaults to ip-host.csv")

    return parser.parse_args()    

# process th ehosts and output our two files
def process_hosts(host_filename,ips_out_filename=None,pairs_out_filename=None):
    # set the output files to the default if need be
    if ips_out_filename is None:
        ips_out_filename = IPS_OUT_DEFAULT
    if pairs_out_filename is None:
        pairs_out_filename = PAIRS_OUT_DEFAULT

    # open our three files
    with open(host_filename,"r") as host_file, open(ips_out_filename,"wb") as ips_out_file, open(pairs_out_filename,"wb") as pairs_out_file:
        # open two writers to the output files
        ips_writer = csv.writer(ips_out_file,delimiter=",")
        pairs_writer = csv.writer(pairs_out_file,delimiter=",")

        #go through the hostnames
        for line in host_file:
            hostname = line.strip()
            if hostname == "":
                continue
            # get the IP
            ip = socket.gethostbyname(hostname)
            # write to the output files
            ips_writer.writerow([ip])
            pairs_writer.writerow([ip,hostname])

# the main procedure
def main():
    args = parse_args()
    process_hosts(args.host_file,ips_out_filename=args.ips_out,pairs_out_filename=args.pairs_out)

main()