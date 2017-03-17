#!/usr/bin/env python
# -*- coding: utf-8 -*-

# David Zuccaro 11/03/2017
# graph climate chart

import matplotlib
#matplotlib.use('TkAgg') 
#import os
import matplotlib.ticker as ticker

import pylab

import numpy as np

#from os import listdir
#from os.path import isfile, join

import datetime

import mysql.connector

import argparse

#os.system("touch /home/dz/test1")

degree_sign 	= unichr(176)
char_inc        = 0
temp_tots       = []
avesl           = np.zeros(365)
avesh           = np.zeros(365)
mypath          = "/home/dz/ghcnd_all/"
temp            = 0.0

month_days      = (31,28,31,30,31,30,31,31,30,31,30,31)
start_temp      = 0
end_temp        = 0


month_tick_mark_loc = np.zeros(12)
grids               = np.zeros(12)

parser 					= argparse.ArgumentParser()
parser.add_argument("-s",  "--station",  default="ASN00031037", help="ghcn weather station code")
parser.add_argument("-f",  "--outfile",  default="test.png",    help="the output filename")

args = parser.parse_args()

station         = args.station
file_name       = station + ".dly"
fullpath        = mypath + file_name
outfn           = args.outfile

cnx = mysql.connector.connect(user='root', password='happy1', database='ghcndata')
cursor = cnx.cursor()
get_station = ("SELECT station_name FROM station WHERE field1 = '" + station + "';")

cursor.execute(get_station)

station_names = []

for (station_name) in cursor:
    station_names.append(station_name)

#print station_names

cursor.close()
cnx.close()

def num_days(month_no):    
    # get progressive number of days by month
    tot_days = 0
    for i in range(month_no):
        tot_days += month_days[i]
    return tot_days

#set up location of month tick markers
start_month_day = 0
end_month_day = -1
for x in range(12):
    grids[x] = start_month_day
    end_month_day += month_days[x]
    month_tick_mark_loc[x] = (start_month_day+end_month_day)/2
    start_month_day += month_days[x]
    
#create month labels
month_labs = []
for i in range(1,13):
    month_labs.append(datetime.date(2008, i, 1).strftime('%B'))

# set up main data array to calc aves
for x in range(365):
    myline = [0,0,0,0]
    temp_tots.append(myline)

#loop through each line of file
with open(fullpath, "r") as this_file:
    
    for line in this_file:
        #look for mins
        if line[17:21] == "TMIN":           
            
            this_month = int(line[15:17])  # get month

            this_year = int(line[11:15]) # get year        
            
            char_inc = 0 #initialise char pointer
            
            for col in range(month_days[this_month - 1]):      # scan thru days on each line  
  
                start_temp = 21 + char_inc
                end_temp   = 21 + char_inc + 5             # isolate temp reading (5 chars long)

                if end_temp < len(line):                 # check for end of line (days < 31)
                    temp = float(line[start_temp:end_temp])
                    
                    if temp < 600 and temp > -900 and temp != 0:      # ignore invalid temperature
                        
                        temp_tots[num_days(this_month - 1) + col][0] += 1
                        temp_tots[num_days(this_month - 1) + col][1] += temp
                    char_inc += 8                       # move to next temperature
                else:
                    break
                    
        #look for maxes
        if line[17:21] == "TMAX":
            this_month = int(line[15:17]) 

            this_year = int(line[11:15]) # get year        
            
            char_inc = 0
            
            for col in range(month_days[this_month - 1]):      # scan thru days on each line  
  
                start_temp = 21 + char_inc
                end_temp = 21 + char_inc + 5             # isolate temp reading

                if end_temp < len(line):                 # check for end of line (days < 31)
                    temp = float(line[start_temp:end_temp])
                    
                    if temp < 600 and temp > -900 and temp != 0:      # ignore invalid temperature
                        
                        temp_tots[num_days(this_month - 1) + col][2] += 1
                        temp_tots[num_days(this_month - 1) + col][3] += temp
                    char_inc += 8                       # move to next temperature
                else:
                    break
                    
#calculate aves
i = 0
for x in temp_tots:
    if x[0] > 0:
        avesl[i] = x[1] / (x[0] * 10) #mins
        avesh[i] = x[3] / (x[2] * 10) #maxes
    i += 1
        
# create graph

#lines
fig2 = matplotlib.pyplot.figure(figsize=(22.0, 10.0)) # The size of the figure is specified as (width, height) in inches

# 7 degree line of best fit
l1 = fig2.add_subplot(111).plot(range(365), np.poly1d(np.polyfit(range(365), avesh, 7))(range(365)), 
                                label="Maximums", lw=10, color='red')

l2 = fig2.add_subplot(111).plot(range(365), np.poly1d(np.polyfit(range(365), avesl, 7))(range(365)), 
                                label="Minimums", lw=10, color='blue')
                                
l3 = fig2.add_subplot(111).plot(range(365), avesh, 'ro')

l4 = fig2.add_subplot(111).plot(range(365), avesl, 'bo')

fig2.add_subplot(111).legend(("Maximums", "Minimums"), loc=0)

#axes
fig2.add_subplot(111).set_xticks(grids, minor=True)
fig2.add_subplot(111).xaxis.set_major_locator(ticker.FixedLocator(month_tick_mark_loc))

for xmin in fig2.add_subplot(111).xaxis.get_minorticklocs():
    fig2.add_subplot(111).axvline(x=xmin,ls=':',color='grey')
    
for ymaj in fig2.add_subplot(111).yaxis.get_majorticklocs():
    fig2.add_subplot(111).axhline(y=ymaj,ls=':',color='grey')

fig2.add_subplot(111).set_xlim(0, 365)

#grid
fig2.add_subplot(111).grid(b=True, which='both', color='0.65',linestyle='')

#labels
font = {
            'family' : 'normal',
            'weight' : 'bold',
            'size'   : 12
        }
fig2.add_subplot(111).set_ylabel(u'Temperature {0}C\n'.format(degree_sign), fontsize=22, weight='heavy', va='baseline')
fig2.add_subplot(111).set_xlabel('\nMonth', fontsize=22, weight='heavy', ha='center')
fig2.add_subplot(111).set_xticklabels(month_labs)

#figure
matplotlib.rc('font', **font)
fig2.subplots_adjust(left=0.05, bottom=0.1, right=0.99, top=0.92, wspace=0.2, hspace=0.0)
fig2.add_subplot(111).set_title("Average Temperatures By Day From Station At {0}\n".format(station_names[0][0]), fontsize=22, weight='heavy')

#saving

image = "/var/www/html/clim-data/images/" + outfn

#print image
fig2.savefig(image)

print 0

#os.system("touch /home/dz/test2")
#os.system("beep -f 555 -l 460")

#mng = pylab.get_current_fig_manager()
#mng.resize(*mng.window.maxsize())

#pylab.show()
#print outfn

#pylab.savefig('/var/www/html/clim-data/test.png')
