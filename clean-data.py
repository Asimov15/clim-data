#!/usr/bin/python

import datetime 
import mysql.connector
import calendar
from os         import listdir
from os.path    import isfile, join
from datetime   import date
#from __future__ import print_function 

mypath = "/home/dz/ghcnd_all/"
max_files   = 1e7
print_every = 2
file_count  = 0

# get list of filenames
onlyfiles = [g for g in listdir(mypath) if isfile(join(mypath, g))]

# loop thru files
for file_name in onlyfiles:
             
    datafile = mypath + file_name
    file_count += 1
    
    if (file_count % print_every == 0):
        print file_count
        
    if file_count > max_files:
        # only look at specified number of files
        break 

    with open(datafile, "r") as ghcn_file:
        with open('/home/dz/new_files/' + file_name[:11] + '.dly', 'a') as new_file:
        
            for line in ghcn_file:
                m_type  = line[17:21]
                if m_type == "TMAX" or m_type == "TMIN" or m_type == "PRCP":
                    new_file.write(line)
                
        new_file.close()
        
    ghcn_file.close()
        
