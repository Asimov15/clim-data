#!/usr/bin/python
# David Zuccaro 11/03/2017

import numpy
from os import listdir
from os.path import isfile, join

year            = 100
month           = 12
day             = 31
inc             = 0
a               = numpy.zeros((year,month,day))
flag            = False
thisyear        = ""
monthcount      = 0

mypath = "/home/dz/data4/"

onlyfiles = [g for g in listdir(mypath) if isfile(join(mypath, g))]

for i in onlyfiles:
    datafile = mypath + i
    print datafile

    for x in range(year):
        for y in range(month):
            for z in range(day):
                a[x][y][z] = -9999

    with open(datafile, "r") as f:
        for line in f:
            if line[17:21] == "TMAX":
                if not flag:
                    startyear = float(line[11:15])
                    flag = True            
                inc = 0
                for col in range(31):
                    x = float(line[11:15]) - startyear
                    y = float(line[15:16])                
                    temp1 = 21 + inc
                    temp2 = 21 + inc + 5
                    if temp2 < len(line):
                        temp3 = line[temp1:temp2]
                        a[x][y][col] = float(temp3)
                        inc = inc + 8
                        #print line[0:21]
                        #print line[21 + inc:21 + inc + 5]

    yearave = []

    for x in range(year):
        count = 0
        tot = 0
        ave = 0
        for y in range(month):
            for z in range(day):
                if a[x][y][z] != -9999:      
                    count = count + 1
                    tot = tot + a[x][y][z]
                    ave = tot / count
        if count < 50:
            ave = -9999.0    
        yearave.append(ave)
            
        print ave / 10.0
    



            
