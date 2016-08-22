import matplotlib.pyplot as plt
import sqlite3
import argparse

DATABASE = "certs.db"

def parse_args():
	parser = argparse.ArgumentParser(description="plots rank against interval")
	group = parser.add_mutually_exclusive_group()
	group.add_argument(
		"-a",
		"--avg",
		action="store_true",
		help="flag to use avg")
	group.add_argument(
		"-m",
		"--min",
		action="store_true",
		help="flag to use min")
	group.add_argument(
		"-M",
		"--max",
		action="store_true",
		help="flag to use max")
	return parser.parse_args()

def main():
	args = parse_args()
	field = None
	if args.avg:
		field = "seen_avg"
	elif args.min:
		field = "seen_min"
	elif args.max:
		field = "seen_max"
	else:
		raise ValueError("must specify avg, min or max flag")

	# connect to the DB
	conn = sqlite3.connect(DATABASE)
	cursor = conn.cursor()

	# fetch IP-dom pairs
	cursor.execute("SELECT ip,domain FROM pairs")
	print "Fetching ip-dom pairs..."
	pairs = cursor.fetchall()
	print "Done!"

	# initialize x,y value lists
	x = []
	y = []

	# iterate over ip-dom pairs
	print "Processing ip-dom pairs..."
	c = 0
	for ip,domain in pairs:
		c += 1
		# report progress
		if c % 100000 == 0:
			print "\t%d" % (c)

		# get rank
		cursor.execute("SELECT avg_rank FROM ranks WHERE domain=?",(domain,))
		rank = cursor.fetchone()
		if rank[0] is None:
			# print "No rank: %s,%s" % (ip,domain)
			continue
		rank = int(rank[0])
		
		# get interval
		query = "SELECT %s FROM intervals WHERE ip=? AND domain=?" % (field)
		cursor.execute(query,(ip,domain))
		interval = cursor.fetchone()
		if interval:
			interval = interval[0]
		else:
			# print "No interval: %s,%s" % (ip,domain)
			continue

		# add to x,y lists
		y.append(rank)
		x.append(interval)
		
	conn.close()
	print "Done!"

	# generate plot
	plt.scatter(x,y,edgecolors='none')
	plt.show()
main()