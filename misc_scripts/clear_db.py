import sqlite3

DATABASE = "certs.db"

def main():
	conn = sqlite3.connect(DATABASE)

	cursor = conn.cursor()

	cursor.execute("DELETE FROM certs")
	cursor.execute("DELETE FROM errors")

	conn.commit()
	conn.close()

main()