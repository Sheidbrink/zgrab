import sqlite3

DATABASE = "certs.db"

def main():
	conn = sqlite3.connect(DATABASE)

	cursor = conn.cursor()
	d13 = '2016-07-13 00:00:00'
	d18 = '2016-07-18 00:00:00'
	total_records = 0

	cursor.execute("SELECT * FROM certs WHERE first=? AND last=?", (d13,d13))
	records = cursor.fetchall()
	print "%d records deleted" % (len(records))
	total_records += len(records)
	cursor.execute("DELETE FROM certs WHERE first=? AND last=?", (d13,d13))
	
	cursor.execute("SELECT * FROM certs WHERE first=? AND last=?", (d13,d18))
	records = cursor.fetchall()
	print "%d records deleted" % (len(records))
	total_records += len(records)
	cursor.execute("DELETE FROM certs WHERE first=? AND last=?", (d13,d18))
	
	cursor.execute("SELECT * FROM certs WHERE first=? AND last=?", (d18,d18))
	records = cursor.fetchall()
	print "%d records deleted" % (len(records))
	total_records += len(records)
	cursor.execute("DELETE FROM certs WHERE first=? AND last=?", (d18,d18))
	
	cursor.execute("SELECT * FROM certs WHERE first=? AND last=?", (d18,d13))
	records = cursor.fetchall()
	print "%d records deleted" % (len(records))
	total_records += len(records)
	cursor.execute("DELETE FROM certs WHERE first=? AND last=?", (d18,d13))

	print "%d total records deleted" % (total_records)

	conn.commit()
	conn.close()

main()
