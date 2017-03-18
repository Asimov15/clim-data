#!/usr/bin/python

import mysql.connector

latitude = 0.0
cnx = mysql.connector.connect(user='root', password='happy1', database='ghcndata')

cursor = cnx.cursor()

datafile = "/srv/clim-data/ghcnd-countries.txt"
add_country = ("INSERT INTO country "
               "(code, name) "
               "VALUES (%s, %s)")

with open(datafile, "r") as this_file:
    for line in this_file:  
        code = line[:2]
        country = line[3:-2]        
        data_country = (code, country)    
        # Insert new station
        cursor.execute(add_country, data_country)
        print code, country

# Make sure data is committed to the database
cnx.commit()

cursor.close()
cnx.close()
