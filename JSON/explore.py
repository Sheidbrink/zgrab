import sqlite3
import argparse
import IPython

DATABASE = "certs.db"
conn = sqlite3.connect(DATABASE)
cursor = conn.cursor()

def parse_args():
	parser = argparse.ArgumentParser(description="explore w/ SQL")
	parser.add_argument(
		"query",
		metavar="QUERY",
		type=str,
		help="SQL query to be executed")
	return parser.parse_args()

def excsql(query):
	cursor.execute(query)

def main():
	global conn
	args = parse_args()
	excsql(args.query)
	IPython.embed()
	conn.commit()
	conn.close()

main()

