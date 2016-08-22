import sqlite3
from datetime import datetime

DATABASE = "certs.db"

def main():
	conn = sqlite3.connect(DATABASE)

	cursor = conn.cursor()
	d13 = '2016-07-13 00:00:00'
	d18 = '2016-07-18 00:00:00'

	cursor.execute("SELECT * FROM certs WHERE first=%s" % d13)
	nf13 = len(cursor.fetchall())
	cursor.execute("SELECT * FROM certs WHERE first=%s" % d18)
	nf18 = len(cursor.fetchall())

	print "Num with 7/13 as first: %d" % nf13
	print "Num with 7/18 as first: %d" % nf18

	conn.commit()
	conn.close()

main()
