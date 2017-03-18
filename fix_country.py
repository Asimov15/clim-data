#!/usr/bin/python

import mysql.connector

mypath          = "/home/dz/ghcnd_all/"

cnx = mysql.connector.connect(user='root', password='happy1', database='ghcndata')

cursor1 = cnx.cursor(buffered=True)
cursor2 = cnx.cursor()
get_rec = ("SELECT id, field1 FROM station;")

cursor1.execute(get_rec)

for stat_rec in cursor1:        
    command = "UPDATE station SET country_code = '" +\
        stat_rec[1][:2]                             +\
        "', field1 = '"                             +\
        stat_rec[1][2:]                             +\
        "' WHERE id = "                             +\
        str(stat_rec[0])                            +\
        ";"                
    print command
    cursor2.execute(command)            
            
# Make sure data is committed to the database
cnx.commit()
cursor.close()
cnx.close()
