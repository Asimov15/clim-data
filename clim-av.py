#!/usr/bin/python
# David Zuccaro 11/03/2017

# graph climate chart

import matplotlib
matplotlib.use('TkAgg') 
import numpy
from os import listdir
from os.path import isfile, join
import pylab

degree_sign 	= unichr(176)
year_span       = 70
char_inc        = 0
temp_tots       = numpy.zeros(365)
start_year      = 1940
file_count      = 0
max_files       = int(2e3)
mypath          = "/home/dz/ghcnd_all/"
year_no         = 0
counter         = 0
monthly_limit   = 20
month_check     = numpy.zeros(12)
this_year       = 0
last_year       = 0
year_temp_sum   = 0
year_temp_count = 0
all_months_read = True
station         = "ASN00031037"
fn              = station + ".dly"
fullpath        = "/home/dz/ghcnd_all/" + fn
month_days      = (31,28,31,30,31,30,31,31,30,31,30,31)

font 			= \
{
	'family' : 'normal',
	'weight' : 'bold',
	'size'   : 16
}

def num_days(m):
    t = 0
    for x in range(m):
        t += month_days[x]
    return t

for x in range(350):
    temp_tots.append((0,0))

with open(datafile, "r") as this_file:
    # look thru lines of file
    for line in this_file:
        #only look at mins
        if line[17:21] == "TMIN":           
            
            this_month = int(line[15:17]) 
            this_year = int(line[11:15]) # get year        
            
            for col in range(month_days[this_month - 1]):      # scan thru days on each line      
                s_temp = 21 + char_inc
                e_temp = 21 + char_inc + 5             # isolate temp reading
                if e_temp < len(line):                 # check for end of line (days < 31)
                    temp = float(line[s_temp:e_temp])
                    if temp < 600 and temp > -900 and temp != 0:      # ignore invalid temperature
                        temp_tots[numdays(this_month - 1) + col][0] += 1
                        temp_tots[numdays(this_month - 1) + col][1] += temp
                    char_inc += 8                       # move to next temperature
                else:
                    break          

global_ave_temp = []
year_list = []
y = start_year
        
# create graph
pylab.plot(year_list, global_ave_temp, 'ro')
pylab.ylabel(u'Temperature {0}C'.format(degree_sign))
pylab.xlabel('Year')
pylab.subplots_adjust(left=0.06, bottom=0.1, right=0.97, top=0.94, wspace=0.2, hspace=0.0)
pylab.title("Average Temperatures By Year From GHCN Data - {0} Stations".format(max_files), fontweight='bold')
matplotlib.rc('font', **font)
pylab.grid(b=True, which='both', color='0.65',linestyle='-')
pylab.show()
