import sqlite3
import json
import argparse
import logging
from datetime import datetime,timedelta
import sys

DATABASE = "certs.db"
logging.basicConfig(filename='certs.log',level=logging.INFO)

def get_time_left(start,curr,prog):
	delta = curr - start
	total = timedelta(0,(100 * delta.total_seconds())/prog,0)
	time_left = total - delta
	hours,remainder = divmod(int(time_left.total_seconds()),3600)
	minutes,seconds = divmod(remainder,60)
	return "%dh%dm%ds" % (hours,minutes,seconds)

def get_time_left_v2(speed,num):
	remaining = 1000000 - num
	total_seconds = int(float(remaining) / float(speed))
	hours,remainder = divmod(total_seconds,3600)
	minutes,seconds = divmod(remainder,60)
	return "%dh%dm%ds" % (hours,minutes,seconds)

def get_speed(num,prev,curr):
	delta = curr - prev
	seconds = delta.total_seconds()
	speed = float(num)/float(seconds)
	return speed

def parse_args():
	parser = argparse.ArgumentParser(description="Adds Alexa records " \
		"to db")
	parser.add_argument(
		"input",
		metavar="INPUT",
		type=str,
		help="filename (paths will break this) for input JSON")
	parser.add_argument(
		"-i",
		"--init",
		action="store_true",
		help="flag to initialize the db")
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

def init_db():
	conn = sqlite3.connect(DATABASE)

	cursor = conn.cursor()

	cursor.execute("CREATE TABLE certs (ip VARCHAR(15) NOT NULL, domain VARCHAR(253) NOT NULL, signature TEXT NOT NULL, first DATE NOT NULL, last DATE NOT NULL, start DATE NOT NULL, end DATE NOT NULL, issuer TEXT NOT NULL, self_signed BOOLEAN NOT NULL, valid BOOLEAN NOT NULL, latitude REAL NOT NULL, longitude REAL NOT NULL, timezone TEXT NOT NULL, country TEXT NOT NULL, country_code VARCHAR(2) NOT NULL, CONSTRAINT id PRIMARY KEY (domain,ip,signature))")
	cursor.execute("CREATE TABLE errors (ip VARCHAR(15) NOT NULL, domain VARCHAR(253) NOT NULL, type TEXT NOT NULL, date DATE NOT NULL, CONSTRAINT id PRIMARY KEY (domain,date))")
	conn.commit()
	conn.close()

def clear_tables():
	conn = sqlite3.connect(DATABASE)

	cursor = conn.cursor()

	cursor.execute("DELETE FROM certs")
	cursor.execute("DELETE FROM errors")

	conn.commit()
	conn.close()

def drop_tables():
	conn = sqlite3.connect(DATABASE)

	cursor = conn.cursor()

	cursor.execute("DROP TABLE certs")
	cursor.execute("DROP TABLE errors")

	conn.commit()
	conn.close()

def process(args):
	date,ext = args.input.split(".")
	date = datetime.strptime(date,"%Y-%m-%d")
	print date 

	f = open(args.input,"r")

	conn = sqlite3.connect(DATABASE)

	cursor = conn.cursor()

	n443 = 0
	ntls = 0
	ncert = 0
	ngood = 0
	ntotal = 0
	nnew = 0
	nupdated = 0
	start_time = datetime.now()
	for line in f:
		line = line.strip()
		if line == "":
			continue
		# print "*************************\n\n"
		data = json.loads(line)
		# print data
		final_data = []
		final_data.append(data['ip'])
		final_data.append(data['domain'])
		ntotal += 1
		error = None
		if 'p443' not in data:
			error = "443"
			n443 += 1
		elif 'tls' not in data['p443']['https']:
			error = "TLS"
			ntls += 1
		elif 'certificate' not in data['p443']['https']['tls']:
			error = "Cert"
			ncert += 1
		else:
			try:
				# import IPython; IPython.embed()
				cert = data['p443']['https']['tls']['certificate']['parsed']
				ngood += 1
				final_data.append(cert['signature']['value'])
				cursor.execute("SELECT * FROM certs WHERE ip=? AND domain=? AND signature=?", tuple(final_data))
				record = cursor.fetchone()
				if record is None:
					final_data.append(str(date))
					final_data.append(str(date))
					final_data.append(str(datetime.strptime(cert['validity']['start'],"%Y-%m-%dT%H:%M:%SZ")))
					final_data.append(str(datetime.strptime(cert['validity']['end'],"%Y-%m-%dT%H:%M:%SZ")))
					if 'common_name' in cert['issuer']:
						final_data.append(str(sorted(cert['issuer']['common_name'])))
					else:
						final_data.append("N/A")
					final_data.append(cert['signature']['self_signed'])
					final_data.append(cert['signature']['valid'])
					final_data.append(data['location']['latitude'])
					final_data.append(data['location']['longitude'])
					final_data.append(data['location']['timezone'])
					final_data.append(data['location']['country'])
					final_data.append(data['location']['country_code'])
					logging.info(str(final_data))
					cursor.execute("INSERT INTO certs VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",tuple(final_data))
					nnew += 1
				else:
					old_first = datetime.strptime(record[3],"%Y-%m-%d %H:%M:%S")
					old_last = datetime.strptime(record[3],"%Y-%m-%d %H:%M:%S")
					new_first = old_first
					new_last = old_last
					if date < old_first:
						new_first = date
					elif date > old_last:
						new_last = date
					cursor.execute("UPDATE certs SET first=?,last=? WHERE ip=? AND domain=? AND signature=?",(str(new_first),str(new_last),final_data[0],final_data[1],final_data[2]))
					nupdated += 1

			except Exception as e:
				print sys.exc_info()
				import IPython; IPython.embed()
				break
		INTERVAL = 10000
		if ntotal % INTERVAL == 0:
			if ntotal == INTERVAL:
				prev = start_time
			print "n443: %s (%.2f%%)" % (str(n443),float(n443)/float(ntotal) * 100)
			print "ntls: %s (%.2f%%)" % (str(ntls),float(ntls)/float(ntotal) * 100)
			print "ncert: %s (%.2f%%)" % (str(ncert),float(ncert)/float(ntotal) * 100)
			print "ngood: %s (%.2f%%)" % (str(ngood),float(ngood)/float(ntotal) * 100)
			print "\nntotal: " + str(ntotal) 
			print "**************************"
			done = float(ntotal)/float(1000000) * 100
			now = datetime.now()
			speed = get_speed(INTERVAL,prev,now)
			print "Progress: %.2f%% (%s)" % (done,get_time_left(start_time,now,done)) 
			print "Speed: %.2f IPs/s" % (speed)
			print "Time-left (2.0): %s" % (get_time_left_v2(speed,ntotal))
			print "**************************\n\n"
			conn.commit()

			prev = now

		if error:
			logging.error("%s: %s , %s" % (error,data['ip'],data['domain']))
			try:
				cursor.execute("INSERT INTO errors VALUES (?,?,?,?)", (data['ip'],data['domain'],error,date))
			except sqlite3.IntegrityError as e:
				print "UNIQUE constraint failed: errors.domain, errors.date"
	conn.commit()
	conn.close()
	print "\nNew records: %s" % (str(nnew))
	print "Updated records: %s" % (str(nupdated))

def main():
	args = parse_args()

	if args.init:
		init_db()
	elif args.drop:
		drop_tables()
	elif args.clear:
		clear_tables()
	else:
		process(args)

main()
