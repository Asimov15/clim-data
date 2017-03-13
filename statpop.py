#!/usr/bin/python
print "0"
import mysql.connector
print "1"
latitude = 0.0
cnx = mysql.connector.connect(user='root', password='happy1', database='ghcndata')
print "2"
cursor = cnx.cursor()
print "3"
datafile = "/home/dz/stations/ghcnd-stations.txt"
add_station = ("INSERT INTO station "
               "(field1, latitude, longitude, field2, station_name, field3) "
               "VALUES (%s, %s, %s, %s, %s, %s)")

with open(datafile, "r") as this_file:
    for line in this_file:  
        field1 = line[:11]
        latitude = line[12:20]
        longitude = line[21:30]
        station_name = line[41:72]
        data_station = (field1, latitude, longitude, 0, station_name, '')    
        # Insert new station
        cursor.execute(add_station, data_station)
        print latitude, longitude, station_name

print "6"
# Make sure data is committed to the database
cnx.commit()
print "7"
cursor.close()
cnx.close()
