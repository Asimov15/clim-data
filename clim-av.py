#!/usr/bin/python
# David Zuccaro 11/03/2017

# graph climate chart


import matplotlib
matplotlib.use('TkAgg') 

import matplotlib.ticker as ticker

import pylab

import numpy as np

from os import listdir
from os.path import isfile, join

import datetime

import mysql.connector

degree_sign 	= unichr(176)
char_inc        = 0
temp_tots       = []
avesl           = np.zeros(365)
avesh           = np.zeros(365)
mypath          = "/home/dz/ghcnd_all/"
temp            = 0.0
station         = "ASN00031037"
file_name       = station + ".dly"
fullpath        = mypath + file_name
month_days      = (31,28,31,30,31,30,31,31,30,31,30,31)
start_temp      = 0
end_temp        = 0

font 			= \
{
	'family' : 'normal',
	'weight' : 'bold',
	'size'   : 16
}

month_tick_mark_loc = np.zeros(12)
grids               = np.zeros(12)


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
                    
i = 0
for x in temp_tots:
    if x[0] > 0:
        avesl[i] = x[1] / (x[0] * 10)
        avesh[i] = x[3] / (x[2] * 10)
    i += 1
        
# create graph
fig=pylab.figure()

ax = fig.add_subplot(111)

pylab.grid(b=True, which='both', color='0.65',linestyle='')

#pylab.plot(range(365), aves, 'ro')

lines=pylab.plot(range(365), np.poly1d(np.polyfit(range(365), avesl, 7))(range(365)), range(365), np.poly1d(np.polyfit(range(365), avesh, 7))(range(365)))
l1, l2 = lines
pylab.ylabel(u'Temperature {0}C'.format(degree_sign))
pylab.xlabel('Month')

ax.xaxis.set_major_locator(ticker.FixedLocator(month_tick_mark_loc))
pylab.subplots_adjust(left=0.04, bottom=0.1, right=0.99, top=0.94, wspace=0.2, hspace=0.0)

ax.set_xticks(grids, minor=True)
ax.set_xticklabels(month_labs)

pylab.setp(l1, linewidth=10, color='blue')
pylab.setp(l2, linewidth=10, color='red')

for xmin in ax.xaxis.get_minorticklocs():
    ax.axvline(x=xmin,ls=':',color='grey')

for ymaj in ax.yaxis.get_majorticklocs():
  ax.axhline(y=ymaj,ls=':',color='grey')

ax.set_xlim(0, 365)
pylab.title("Average Temperatures By Day From GHCN Data".format(fontweight='bold'))
matplotlib.rc('font', **font)

mng = pylab.get_current_fig_manager()
mng.resize(*mng.window.maxsize())

pylab.show()
