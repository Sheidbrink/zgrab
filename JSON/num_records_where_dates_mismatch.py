import sqlite3
from datetime import datetime

DATABASE = "certs.db"

def main():
	conn = sqlite3.connect(DATABASE)

	cursor = conn.cursor()
	d13 = '2016-07-13 00:00:00'
	d18 = '2016-07-18 00:00:00'

	cursor.execute("SELECT ip,domain,signature,first,last FROM certs")
	record = cursor.fetchone()
	nrecs = 0
	nmism = 0
	f = open("mismatch_dates.log","w")
	while record is not None:
		nrecs += 1
		if nrecs % 100000 == 0:
			print nrecs
		first = datetime.strptime(record[-2],"%Y-%m-%d %H:%M:%S")
		last = datetime.strptime(record[-1],"%Y-%m-%d %H:%M:%S")
		if first > last:
			nmism += 1
			f.write("%s,%s,%s,%s,%s\n" % record)
		record = cursor.fetchone()
	f.close()
	print "Total records: %d" % (nrecs)
	print "Mismatched dates: %d" % (nmism)

	conn.commit()
	conn.close()

main()
