import sqlite3
import argparse
from datetime import datetime,timedelta
import json

DATABASE = "certs.db"


def parse_args():
	parser = argparse.ArgumentParser(description="enum the dom-ip pairs")
	parser.add_argument(
		"json",
		metavar="JSON",
		type=str,
		help="the JSON file to read from")
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
	parser.add_argument(
		"-s",
		"--seed",
		action="store_true",
		help="flag to seed db with first set of pairs")
	return parser.parse_args()

def init_tables():
	conn = sqlite3.connect(DATABASE)

	cursor = conn.cursor()

	cursor.execute("CREATE TABLE pairs (ip VARCHAR(15) NOT NULL, domain VARCHAR(253) NOT NULL, seen_everywhere BOOLEAN NOT NULL, CONSTRAINT id PRIMARY KEY (ip,domain))")

	conn.commit()
	conn.close()

def clear_tables():
	conn = sqlite3.connect(DATABASE)

	cursor = conn.cursor()

	cursor.execute("DELETE FROM pairs")

	conn.commit()
	conn.close()

def drop_tables():
	conn = sqlite3.connect(DATABASE)

	cursor = conn.cursor()

	cursor.execute("DROP TABLE pairs")

	conn.commit()
	conn.close()

def seed(args):
	print "Seeding..."
	f = open(args.json,"r")

	conn = sqlite3.connect(DATABASE)

	cursor = conn.cursor()
	print "Processing JSON..."
	c = 0
	for line in f:
		line = line.strip()
		if line == "":
			continue
		data = json.loads(line)
		ip = data['ip']
		domain = data['domain']
		c += 1
		if ('p443' in data) and ('tls' in data['p443']['https']) and ('certificate' in data['p443']['https']['tls']):
			cursor.execute("INSERT INTO pairs VALUES (?,?,?)", (ip,domain,True))
		if c % 10000 == 0:
			print c
			conn.commit()
	f.close()
	conn.commit()
	conn.close()
	print "Done!\n"

def process(args):
	f = open(args.json,"r")

	conn = sqlite3.connect(DATABASE)

	cursor = conn.cursor()
	cursor.execute("SELECT ip,domain FROM pairs WHERE seen_everywhere = 1")
	print "Fetching ip-dom pairs..."
	db_pairs = cursor.fetchall()
	print "Done!"
	json_pairs = []
	c = 0
	print "Processing JSON..."
	for line in f:
		line = line.strip()
		if line == "":
			continue
		data = json.loads(line)
		ip = data['ip']
		domain = data['domain']
		c += 1
		if ('p443' in data) and ('tls' in data['p443']['https']) and ('certificate' in data['p443']['https']['tls']):
			json_pairs.append((ip,domain))
			cursor.execute("SELECT * FROM pairs WHERE ip=? AND domain=?", (ip,domain))
			record = cursor.fetchone()
			if record is None:
				cursor.execute("INSERT INTO pairs VALUES (?,?,?)", (ip,domain,False))
		if c % 10000 == 0:
			print c
			conn.commit()
	f.close()
	conn.commit()
	json_pairs = set(json_pairs)
	print "Done!"
	print "Comparing ip-dom pairs..."
	c = 0
	miss_count = 0
	for db_pair in db_pairs:
		if db_pair not in json_pairs:
			cursor.execute("UPDATE pairs SET seen_everywhere=? WHERE ip=? and domain=?",(False,ip,domain))
			miss_count += 1
			if miss_count % 10000 == 0:
				print db_pair
		c += 1
		if c % 10000 == 0:
			print c
			conn.commit()
	conn.commit()
	conn.close()
	print "Done!\n"

	print "%d conflicts found" % (miss_count)

def main():
	args = parse_args()

	if args.init:
		init_tables()
	elif args.drop:
		drop_tables()
	elif args.clear:
		clear_tables()
	elif args.seed:
		seed(args)
	else:
		process(args)

main()

