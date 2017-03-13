#!/usr/bin/python

import datetime 
import mysql.connector
import calendar
from os import listdir
from os.path import isfile, join

file_count = 0
max_files = 200
cnx = mysql.connector.connect(user='root', password='happy1', database='ghcndata')

cursor = cnx.cursor()
mypath = "/home/dz/ghcnd_all/"

add_clim = ("INSERT INTO climate "
               "(station, rec_type, measurement, rec_date) "
               "VALUES (%s, %s, %s, %s)")

cursor.execute("DELETE FROM climate")
cnx.commit()

# get list of filenames
onlyfiles = [g for g in listdir(mypath) if isfile(join(mypath, g))]

# loop thru files
for file_name in onlyfiles:
    datafile = mypath + file_name
    
    file_count += 1
    if file_count > max_files:
        # only look at specified number of files
        break 
    print datafile
    with open(datafile, "r") as this_file:
        for line in this_file:  
            station = line[:11]
            year    = line[11:15]
            month   = line[15:17]
            m_type  = line[17:21]
            
            hl = " "

            if m_type == "TMAX":
                hl = "H"
            elif m_type == "TMIN":
                hl = "L"
            
            if hl == " ":
                continue

            day = 1
            char_inc = 0
            for col in range(calendar.monthrange(int(year), int(month))[1]):                       # scan thru days on each line      
                s_temp = 21 + char_inc
                e_temp = 21 + char_inc + 5                # isolate temp reading
                if e_temp < len(line):                   # check for end of line (days < 31)
                    temp = float(line[s_temp:e_temp])                
                    char_inc += 8                        # move to next temperature

                    if temp > -1000.0 and temp < 600 and temp != 0:
                        m_date = datetime.datetime(int(year), int(month), day)
                        data_clim = (station, hl, temp / 10, m_date)    
                        cursor.execute(add_clim, data_clim)
                
                    day += 1
                else:
                    break
            
# Make sure data is committed to the database
cnx.commit()
cursor.close()
cnx.close()
