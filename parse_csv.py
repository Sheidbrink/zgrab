import argparse
import socket
import sys

OUTPUT_DEFAULT = "ips.out"

def parse_args():
	parser = argparse.ArgumentParser(description="Processes a CSV of " \
		"domains (like Alexa top 1M) into a list of IPs that can be used " \
		"zmap")
	parser.add_argument(
		"input",
		metavar="INPUT",
		type=str,
		help="filepath for input CSV")
	parser.add_argument(
		"-o",
		"--output",
		metavar="OUTPUT",
		type=str,
		help="filepath for output IPs")

	return parser.parse_args()

def transform(csv,out):
	for line in csv:
		line = line.strip()
		if line == "":
			continue
		rank,host = line.split(",")
		print host
		info = socket.getaddrinfo(host,"https")
		good_ip = False
		for record in info:
			ip = record[-1][0]
			if ":" not in ip:
				good_ip = True
				break
		if not good_ip:
			sys.stderr.write("No IPv4 record; skipping " + host + "...")
		else:
			out.write(ip + "\n")

def main():
	args = parse_args()

	csv = open(args.input,"r")

	if args.output:
		filepath = args.output
	else:
		filepath = OUTPUT_DEFAULT
	out = open(filepath,"w")

	transform(csv,out)

	csv.close()
	out.close()

main()
