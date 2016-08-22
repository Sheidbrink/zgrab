import sqlite3
import argparse
import logging
from datetime import datetime,timedelta

DATABASE = "certs.db"
# logging.basicConfig(filename='stats.log',level=logging.INFO)

# def parse_args():
# 	parser = argparse.ArgumentParser(description="Processes Alexa records " \
# 		"to generate new stats")

# 	return parser.parse_args()

# def init_tables():
# 	conn = sqlite3.connect(DATABASE)

# 	cursor = conn.cursor()

# 	cursor.execute("CREATE TABLE ")

def main():
	conn = sqlite3.connect(DATABASE)
	cursor = conn.cursor()

	print "Executing..."
	cursor.execute("SELECT domain FROM certs")
	print "Executed"

	print "Fetching..."
	# records = cursor.fetchall()
	next_record = cursor.fetchone()
	print "Fetched"

	# records = 0
	c = 0
	records = []
	while next_record is not None:
		next_record = next_record[0]
		# records += 1
		c += 1
		if c % 10000 == 0:
			print c
			print next_record
		records.append(next_record)
		next_record = cursor.fetchone()

	unique = set(records)
	counts = []
	# print "Counting..."
	# c = 0
	# for record in unique:
	# 	c += 1
	# 	if c % 100 == 0:
	# 		print c
	# 	count = records.count(record)
	# 	counts.append((record,count))
	# print "Counted"

	print "Counting..."
	counts_dict = {}
	for record in records:
		if record in counts_dict:
			counts_dict[record] += 1
		else:
			counts_dict[record] = 1
	counts = []
	for record in counts_dict:
		counts.append((record,counts_dict[record]))
	print "Counted"

	print "Sorting..."
	counts = sorted(counts,key=lambda x: x[1], reverse=True)
	print "Sorted"
	print counts[0:10]

	# print "Records: %d" % (records)
	print "Records: %d" % (len(records))
	print "Unique entries: %d" % (len(unique))

	conn.commit()
	conn.close()

main()

