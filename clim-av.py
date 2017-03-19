#!/usr/bin/env python
# -*- coding: utf-8 -*-

# David Zuccaro 11/03/2017
# graph climate chart

import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg') 

import matplotlib.ticker as ticker

import numpy as np

import datetime

import mysql.connector

import argparse

import matplotlib.patches as patches

import matplotlib.path    as path

degree_sign 	    = unichr(176)
char_inc            = 0
temp_tots           = []
precip_tots         = []
avesl               = np.zeros(365)
avesh               = np.zeros(365)
precip_aves         = np.zeros(12)
mypath              = "/srv/clim-data/ghcnd_temp/"
temp                = 0.0
min_col             = '#eac220'
max_col             = '#a30b0b'
rain_col            = 'blue'

month_days          = (31,28,31,30,31,30,31,31,30,31,30,31)
month_axes          = np.zeros(13)

month_axes[0] = 0
tot = 0
for i in range(12):
    tot += month_days[i]
    month_axes[i+1] = tot    

start_temp          = 0
end_temp            = 0

month_tick_mark_loc = np.zeros(12)
grids               = np.zeros(12)

parser 				= argparse.ArgumentParser()

parser.add_argument("-s",  "--station",  default="USC00464836", help="ghcn weather station code")
parser.add_argument("-f",  "--outfile",  default="test.png" , help="the output filename"      )

args = parser.parse_args()

file_name       = args.station + ".dly"
fullpath        = mypath + file_name
outfn           = args.outfile

cnx = mysql.connector.connect(user='root', password='happy1', database='ghcndata')
cursor1 = cnx.cursor(buffered=True)
cursor2 = cnx.cursor()
cmd = "SELECT station_name, latitude, longitude FROM station WHERE field1 = '" + args.station[2:] + "' AND country_code = '" + args.station[:2] + "';"

get_station = (cmd)

cursor1.execute(get_station)

station_data = []

for (record) in cursor1:
    station_data.append(record)

cmd = "SELECT name FROM country WHERE code = '" + args.station[:2] + "';"
get_country = (cmd)

cursor2.execute(get_country)

country_data = []

for (record) in cursor2:
    country_data.append(record)

cursor1.close()
cursor2.close()
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
    myline = [0.0, 0.0, 0.0, 0.0]
    temp_tots.append(myline)

for x in range(12):
    myline = [0.0, 0.0]
    precip_tots.append(myline)

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
                end_temp   = 21 + char_inc + 5             # isolate temp reading

                if end_temp < len(line):                 # check for end of line (days < 31)
                    temp = float(line[start_temp:end_temp])
                    
                    if temp < 600 and temp > -900 and temp != 0:      # ignore invalid temperature
                        
                        temp_tots[num_days(this_month - 1) + col][2] += 1
                        temp_tots[num_days(this_month - 1) + col][3] += temp
                    char_inc += 8                       # move to next temperature
                else:
                    break
                    
        #look for precipitation
        if line[17:21] == "PRCP":
            this_month = int(line[15:17]) 

            this_year = int(line[11:15]) # get year        
            
            char_inc = 0
            
            for col in range(month_days[this_month - 1]):      # scan thru days on each line  
  
                start_precip = 21 + char_inc
                end_precip   = 21 + char_inc + 5             # isolate precip reading

                if end_precip < len(line):                 # check for end of line (days < 31)
                    precip = float(line[start_precip:end_precip])
                    
                    if precip >= 0:      # ignore invalid precipitation                        
                        precip_tots[this_month - 1][0] += 1
                        precip_tots[this_month - 1][1] += float(precip) 
                        char_inc += 8                       # move to next precipitation
                else:
                    break
                    
#calculate aves
i = 0
for x in temp_tots:    
    if x[0] > 0:
        avesl[i]  = x[1] / (x[0] * 10) #mins
    if x[2] > 0:
        avesh[i]  = x[3] / (x[2] * 10) #maxes
    i += 1
    
i = 0
for x in precip_tots:
    if x[0] > 0:
        a = month_days[i] * x[1] / (x[0] * 10) #precipation        
        precip_aves[i] = a
        
    i += 1
    
# set up precipitation bar graph

left    = np.array(month_axes[:-1])      
right   = np.array(month_axes[1:])
bottom  = np.zeros(len(left))
top     = bottom + precip_aves

# create temp graph

#lines
fig2 = plt.figure(figsize=(22.0, 9.5)) # The size of the figure is specified as (width, height) in inches

# we need a (numrects x numsides x 2) numpy array for the path helper
# function to build a compound path
XY = np.array([[left, left, right, right], [bottom, top, top, bottom]]).T

# get the Path object
barpath = path.Path.make_compound_path_from_polys(XY)

# make a patch out of it
patch = patches.PathPatch(barpath, facecolor=rain_col, edgecolor='gray', alpha=0.5)
fig2.add_subplot(111).add_patch(patch) 

# n degree line of best fit
l1 = fig2.add_subplot(111).plot(range(365), np.poly1d(np.polyfit(range(365), avesh, 5))(range(365)), 
                                label="Maximums", lw=10, color=max_col)

l2 = fig2.add_subplot(111).plot(range(365), np.poly1d(np.polyfit(range(365), avesl, 5))(range(365)), 
                                label="Minimums", lw=10, color=min_col)
                                
l3 = fig2.add_subplot(111).plot(range(365), avesh, 'o', color=max_col)

l4 = fig2.add_subplot(111).plot(range(365), avesl, 'o', color=min_col)
red_patch  = patches.Patch(color=max_col,  label='Average Maximum Temperature')
yel_patch  = patches.Patch(color=min_col,  label='Average Minimum Temperature')
blue_patch = patches.Patch(color=rain_col, label='Rainfall', alpha=0.5)
plt.legend(handles=[red_patch, yel_patch, blue_patch], loc=0)

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

#position canvas
fig2.subplots_adjust(left=0.05, bottom=0.1, right=0.99, top=0.89, wspace=0.2, hspace=0.0)

#set title
matplotlib.rc('font', **font)
firstp = "Average Temperatures By Day From Station At "
md1 = (station_data[0][0]).strip()
md2 = station_data[0][1]
md3 = station_data[0][2]
md4 = country_data[0][0]
the_title = firstp + "{0}, {3}\n (Latitude = {1}, Longitude = {2})\n".format(md1, md2, md3, md4)
fig2.add_subplot(111).set_title(the_title, fontsize=22, weight='heavy')

#saving
image = "/var/www/html/clim-data/images/" + outfn

#print image
fig2.savefig(image)

fig2.show()
