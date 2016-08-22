import sqlite3
import argparse
# from datetime import datetime,timedelta

DATABASE = "certs.db"

def main():
	conn = sqlite3.connect(DATABASE)
	cursor = conn.cursor()
	cursor.execute("SELECT domain,ip FROM certs")
	print "Fetching domain/ip pairs..."
	pairs = cursor.fetchall()
	print "Done!"
	counts = []
	print "Fetching sigs..."
	c = 0
	print len(pairs)
	pairs = set(pairs)
	print len(pairs)
	for domain,ip in pairs:
		c += 1
		if c % 10000 == 0:
			print c
		# if 'google.com' not in domain:
		# 	continue
		cursor.execute("SELECT signature,first,last FROM certs WHERE domain=? AND ip=?",(domain,ip))
		sigs = cursor.fetchall()
		counts.append((domain,ip,len(sigs)))
		# if 'google.com' in domain:
		# 	import IPython; IPython.embed()
	print "Done!"
	counts = sorted(counts,key=lambda x: x[2], reverse=True)
	import IPython; IPython.embed()

main()