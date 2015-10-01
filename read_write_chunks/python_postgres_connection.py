#to stream large results

#!/usr/bin/python
import psycopg2
import sys
import time
 
def main():
	#Define our connection string
	conn_string = "host='localhost' dbname='uwdb' user='postgres' password=''"
 
	# print the connection string we will use to connect
	print "Connecting to database\n	->%s" % (conn_string)
 
	# get a connection, if a connect cannot be made an exception will be raised here
	conn = psycopg2.connect(conn_string)
 
	# conn.cursor will return a cursor object, you can use this cursor to perform queries
	cursor = conn.cursor()
	print "Connected!\n"

	cursor.execute("SELECT * FROM \"public:adhoc10GB1GB:lineitem\"")

 	#is this blocking?
 	start = time.time()
 	records = cursor.fetchall()
 	end = time.time()

 	print "finished"
 	print "time", end-start

if __name__ == "__main__":
	main()