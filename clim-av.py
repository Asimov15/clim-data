#!/usr/bin/python
# David Zuccaro 11/03/2017

# graph climate chart

import matplotlib
matplotlib.use('TkAgg') 
import numpy
from os import listdir
from os.path import isfile, join
import pylab
import datetime
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

degree_sign 	= unichr(176)
char_inc        = 0
temp_tots       = []
aves            = numpy.zeros(365)
mypath          = "/home/dz/ghcnd_all/"
temp            = 0.0
station         = "ASN00031037"
fn              = station + ".dly"
fullpath        = mypath + fn
month_days      = (31,28,31,30,31,30,31,31,30,31,30,31)
s_temp          = 0
s_temp          = 0

font 			= \
{
	'family' : 'normal',
	'weight' : 'bold',
	'size'   : 16
}

m     = numpy.zeros(12)
grids = numpy.zeros(12)
a = 0
b = -1
for x in range(12):
    grids[x] = a
    b += month_days[x]
    m[x] = (a+b)/2
    a += month_days[x]

def num_days(m):    
    t = 0
    for x in range(m):
        t += month_days[x]
    return t
    
month_labs = []
for i in range(1,13):
    month_labs.append(datetime.date(2008, i, 1).strftime('%B'))

for x in range(365):
    myline = [0,0,x]
    temp_tots.append(myline)

with open(fullpath, "r") as this_file:
    # look thru lines of file
    for line in this_file:
        #only look at mins
        if line[17:21] == "TMIN":           
            
            this_month = int(line[15:17]) 

            this_year = int(line[11:15]) # get year        
            
            char_inc = 0
            
            for col in range(month_days[this_month - 1]):      # scan thru days on each line  
  
                s_temp = 21 + char_inc
                e_temp = 21 + char_inc + 5             # isolate temp reading

                if e_temp < len(line):                 # check for end of line (days < 31)
                    temp = float(line[s_temp:e_temp])
                    
                    if temp < 600 and temp > -900 and temp != 0:      # ignore invalid temperature
                        
                        temp_tots[num_days(this_month - 1) + col][0] += 1
                        temp_tots[num_days(this_month - 1) + col][1] += temp
                    char_inc += 8                       # move to next temperature
                else:
                    break
i = 0

for x in temp_tots:

    if x[0] > 0:
        aves[i] = x[1] / (x[0] * 10)
    i += 1
        
# create graph
#fig, ax = pylab.subplots()

fig=plt.figure()
ax = fig.add_subplot(111)
pylab.grid(b=True, which='both', color='0.65',linestyle='')
pylab.plot(range(365), aves, 'ro')

pylab.ylabel(u'Temperature {0}C'.format(degree_sign))
pylab.xlabel('Month')
ax.xaxis.set_major_locator(ticker.FixedLocator(m))
pylab.subplots_adjust(left=0.04, bottom=0.03, right=0.99, top=0.94, wspace=0.2, hspace=0.0)
#pylab.xticks(x, month_labs, rotation='vertical')
ax.set_xticks(grids, minor=True)
ax.set_xticklabels(month_labs)

for xmin in ax.xaxis.get_minorticklocs():
    #print xmaj
    ax.axvline(x=xmin,ls=':',color='grey')

for ymaj in ax.yaxis.get_majorticklocs():
  ax.axhline(y=ymaj,ls=':',color='grey')

ax.set_xlim(0, 365)
pylab.title("Average Temperatures By Day From GHCN Data".format(fontweight='bold'))
matplotlib.rc('font', **font)

pylab.show()
