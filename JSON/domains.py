import sqlite3
import argparse
from datetime import datetime,timedelta
import os
import json
import logging

DATABASE = "certs.db"
logging.basicConfig(filename='ranks.log',level=logging.INFO)

def parse_args():
	parser = argparse.ArgumentParser(description="get min, max and avg for domains re: Alexa rankings")
	parser.add_argument(
		"input",
		metavar="INPUT",
		type=str,
		help="filename for JSON")
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
	return parser.parse_args()

def init_tables():
	conn = sqlite3.connect(DATABASE)

	cursor = conn.cursor()

	cursor.execute("CREATE TABLE ranks (domain VARCHAR(253) NOT NULL, has_rank BOOLEAN NOT NULL, times_seen INTEGER NOT NULL, avg_rank REAL, min_rank INTEGER, max_rank INTEGER, CONSTRAINT id PRIMARY KEY (domain))")

	conn.commit()
	conn.close()

def clear_tables():
	conn = sqlite3.connect(DATABASE)

	cursor = conn.cursor()

	cursor.execute("DELETE FROM ranks")

	conn.commit()
	conn.close()

def drop_tables():
	conn = sqlite3.connect(DATABASE)

	cursor = conn.cursor()

	cursor.execute("DROP TABLE ranks")

	conn.commit()
	conn.close()

def to_datetime(date_str):
	return datetime.strptime(date_str,"%Y-%m-%d %H:%M:%S")

def process(args):
	conn = sqlite3.connect(DATABASE)

	cursor = conn.cursor()

	f = open(args.input,"r")
	nnew = 0
	nupdated = 0
	ntotal = 0
	for line in f:
		line = line.strip()
		if line == "":
			continue
		data = json.loads(line)
		# import IPython; IPython.embed()
		domain = data['domain']
		if 'alexa_rank' in data:
			has_rank = True
		else:
			logging.error("%s: %s has no rank" % (args.input,domain))
			has_rank = False
		if has_rank:
			rank = data['alexa_rank']
		else:
			rank = None
		cursor.execute("SELECT * FROM ranks WHERE domain=?",(domain,))
		record = cursor.fetchone()
		if record is None:
			cursor.execute("INSERT INTO ranks VALUES (?,?,?,?,?,?)",(domain,has_rank,1,rank,rank,rank))
			nnew += 1
		elif record is not None and has_rank:
			record_dom,has_old_rank,times_seen,old_avg,old_min,old_max = record
			if has_old_rank:
				new_avg = (float(rank) + float(old_avg*times_seen))/float(times_seen+1)
				if rank < old_min:
					new_min = rank
				else:
					new_min = old_min
				if rank > new_min:
					new_max = rank
				else:
					new_max = old_max
			else:
				new_avg = rank
				new_min = rank
				new_max = rank
			times_seen += 1
			cursor.execute("UPDATE ranks SET times_seen=?, avg_rank=?, min_rank=?, max_rank=? WHERE domain=?",(times_seen,new_avg,new_min,new_max,domain))
			nupdated += 1
		ntotal += 1
		if ntotal % 10000 == 0:
			print ntotal
			conn.commit()
	conn.commit()
	conn.close()
	print "\nNew records: %s" % (str(nnew))
	print "Updated records: %s" % (str(nupdated))


def main():
	args = parse_args()

	if args.init:
		init_tables()
	elif args.drop:
		drop_tables()
	elif args.clear:
		clear_tables()
	else:
		process(args)

main()