import sqlite3
import argparse
from datetime import datetime,timedelta
import os
import json
import logging

DATABASE = "certs.db"
LOGFILE = 'intervals.log'
logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(levelname)-8s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename=LOGFILE,
                filemode='a')

def parse_args():
	parser = argparse.ArgumentParser(description="get min, max, avg stats on how often certs change")
	parser.add_argument(
		"-i",
		"--init",
		action="store_true",
		help="flag to initialize the tables")
	parser.add_argument(
		"-d",
		"--drop",
		action="store_true",
		help="flag to drop all tables")
	parser.add_argument(
		"-c",
		"--clear",
		action="store_true",
		help="flag to clear the db")
	dom_group = parser.add_mutually_exclusive_group()
	dom_group.add_argument(
		"--dom1",
		action="store_true",
		help="flag to use all domain-ip pairs (default)")
	dom_group.add_argument(
		"--dom2",
		action="store_true",
		help="flag to use only domain-ip pairs that appear in all scans")	
	return parser.parse_args()

def init_tables():
	conn = sqlite3.connect(DATABASE)

	cursor = conn.cursor()

	cursor.execute("CREATE TABLE intervals (ip VARCHAR(15) NOT NULL, domain VARCHAR(253) NOT NULL, seen_avg INTEGER NOT NULL, seen_min INTEGER NOT NULL, seen_max INTEGER NOT NULL, valid_avg INTEGER NOT NULL, valid_min INTEGER NOT NULL, valid_max INTEGER NOT NULL, CONSTRAINT id PRIMARY KEY (ip,domain))")

	conn.commit()
	conn.close()

def clear_tables():
	conn = sqlite3.connect(DATABASE)

	cursor = conn.cursor()

	cursor.execute("DELETE FROM intervals")

	os.remove(LOGFILE)

	conn.commit()
	conn.close()

def drop_tables():
	conn = sqlite3.connect(DATABASE)

	cursor = conn.cursor()

	cursor.execute("DROP TABLE intervals")

	os.remove(LOGFILE)

	conn.commit()
	conn.close()

def to_datetime(date_str):
	return datetime.strptime(date_str,"%Y-%m-%d %H:%M:%S")

def process(args):
	conn = sqlite3.connect(DATABASE)

	cursor = conn.cursor()
	if args.dom1:
		cursor.execute("SELECT ip,domain FROM certs")
	else:
		cursor.execute("SELECT ip,domain FROM pairs WHERE seen_everywhere=1")
	print "Fetching ip-dom pairs..."
	pairs = set(cursor.fetchall())
	print "Done!"
	print "Processing intervals..."
	c = 0
	for pair in pairs:
		c += 1
		ip,domain = pair
		cursor.execute("SELECT * FROM certs WHERE ip=? AND domain=?",(ip,domain))
		records = cursor.fetchall()
		sigs = []
		for record in records:
			sig = record[2]
			first = to_datetime(record[3])
			last = to_datetime(record[4])
			start = to_datetime(record[5])
			end = to_datetime(record[6])
			sigs.append((sig,first,last,start,end))
		sigs = sorted(sigs,key=lambda x: x[1])
		if len(sigs) > 1:
			seen_stats = []
			valid_stats = []
			for i in range (1,len(sigs)):
				prev = sigs[i-1]
				curr = sigs[i]
				if prev[1] > prev[2]:
					raise ValueError("Error: first-seen date is after last-seen!")
				elif prev[1] == curr[1]:
					raise ValueError("Edge-case: first-seen-date of two sigs are equal!")
				elif prev[2] == curr[2]:
					raise ValueError("Edge-case: last-seen-date of two sigs are equal!")
				elif prev[2] >= curr[1]:
					logging.error("seen-intervals of two sigs overlap! (%s, %s, #1: %s, #2: %s)" % (ip,domain,prev[0],curr[0]))
					continue
					# raise ValueError("Edge-case: seen-intervals of two sigs overlap!")
				elif (prev[1] < prev[3]) or (prev[2] > prev[4]):
					logging.error("seen range outside validity range! (%s, %s, %s)" % (ip,domain,prev[0]))
					continue
					# raise ValueError("Edge-case: seen range outside validity range!")
				seen_delta = curr[1] - prev[1]
				valid_delta = prev[4] - prev[3]
				seen_stats.append(seen_delta.days)
				valid_stats.append(valid_delta.days)
			if len(seen_stats) > 0:
				seen_avg = sum(seen_stats)/len(seen_stats)
				seen_min = min(seen_stats)
				seen_max = max(seen_stats)
				valid_avg = sum(valid_stats)/len(valid_stats)
				valid_min = min(valid_stats)
				valid_max = max(valid_stats)
				cursor.execute("INSERT INTO intervals VALUES (?,?,?,?,?,?,?,?)", (ip,domain,seen_avg,seen_min,seen_max,valid_avg,valid_min,valid_max))

		if c % 10000 == 0:
			print c
			conn.commit()
	print "Done!"
	conn.commit()
	conn.close()

def main():
	args = parse_args()

	if (not args.dom1) and (not args.dom2):
		args.dom1 = True

	if args.init:
		init_tables()
	elif args.drop:
		drop_tables()
	elif args.clear:
		clear_tables()
	else:
		process(args)

main()
