#!/usr/bin/python
import psycopg2
hostname = 'localhost'
username = 'sean'
password = 'passwordpassword'
port = '5432'
database = 'jsdk'

qfile = open("test_querys.txt", "r")

conn = psycopg2.connect( host=hostname, user=username, password=password, dbname=database)


for query in qfile:
	cur = conn.cursor()
	cur.execute(query)	
	time.sleep(.6)
	print "sent query"

conn.close()
