#!/usr/bin/python

import mysql.connector
from subprocess import call

mypath          = "/home/dz/ghcnd_all/"

cnx = mysql.connector.connect(user='root', password='happy1', database='ghcndata')

cursor1 = cnx.cursor(buffered=True)

get_station = ("SELECT field1 FROM station WHERE temperatures = 0;")

cursor1.execute(get_station)

for station_id in cursor1:
    #print station_id
    datafile = mypath + station_id[0] + ".dly"    
    print datafile
    call(["rm", datafile])
            
# Make sure data is committed to the database
cnx.commit()
cursor1.close()
cnx.close()
