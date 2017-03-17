#!/usr/bin/python

import mysql.connector

mypath          = "/home/dz/ghcnd_all/"

cnx = mysql.connector.connect(user='root', password='happy1', database='ghcndata')

cursor1 = cnx.cursor(buffered=True)
cursor2 = cnx.cursor()
get_station = ("SELECT field1 FROM station WHERE temperatures = 0;")

cursor1.execute(get_station)

for station_id in cursor1:
    #print station_id
    datafile = mypath + station_id[0] + ".dly"

    maxes = 0
    mins  = 0

    with open(datafile, "r") as this_file:
        for line in this_file:  
            if line[17:21] == "TMIN":    
                mins += 1
            elif line[17:21] == "TMAX":    
                maxes += 1                 
            if maxes > 70 and mins > 70:
                command = "UPDATE station SET temperatures = 1 WHERE field1 = '" + station_id[0] + "';"                
                print command
                cursor2.execute(command)
                break
            
# Make sure data is committed to the database
cnx.commit()
cursor.close()
cnx.close()
