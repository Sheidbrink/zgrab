import sqlite3

DATABASE = "certs.db"

def main():
	conn = sqlite3.connect(DATABASE)

	cursor = conn.cursor()
	d13 = '2016-07-13 00:00:00'
	d18 = '2016-07-18 00:00:00'

	# cursor.execute("UPDATE certs SET first=? WHERE first=?",())
	# cursor.execute("UPDATE certs SET last=? WHERE last=?",())
	# cursor.execute("SELECT domain from certs WHERE first=?",("2016-07-13 00:00:00"))
	cursor.execute("SELECT domain,ip,signature,first,last FROM certs WHERE first=? OR first=? OR last=? OR last=?",(d13,d18,d13,d18))
	records = cursor.fetchall()
	print "Number of poisoned entries: %s" % (str(len(records)))
	f = open("poison.log","w")
	other_dates = []
	nfirst = 0
	nlast = 0
	nlast_13 = 0
	for domain,ip,sig,first,last in records:
		if last == d13:
			nlast_13 += 1
		if (first != d13) and (first != d18):
			other_dates.append(first)
			nfirst += 1
		elif (last != d13) and (last != d18):
			other_dates.append(last)
			nlast += 1
		f.write("%s,%s,%s\n" % (domain,ip,sig))
	f.close()
	other_dates = set(other_dates)
	for date in other_dates:
		print date
	print "nFirst: %s" % (str(nfirst))
	print "nLast: %s" % (str(nlast))
	print "nLast_13: %s" % (str(nlast_13))
	print "Total: %s" % (str(len(other_dates)))
	# print len(records)
	conn.commit()
	conn.close()

main()
