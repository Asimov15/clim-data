#!/usr/bin/python
# David Zuccaro 11/03/2017

# graph global temperatures

import matplotlib
matplotlib.use('TkAgg') 
import numpy
from os import listdir
from os.path import isfile, join
import pylab

degree_sign 	= unichr(176)
year_span       = 70
char_inc        = 0
temp_aves       = numpy.zeros((year_span,2))
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

font 			= \
{
	'family' : 'normal',
	'weight' : 'bold',
	'size'   : 16
}

# get list of filenames
onlyfiles = [g for g in listdir(mypath) if isfile(join(mypath, g))]

# loop thru files
for file_name in onlyfiles:
    datafile = mypath + file_name

    file_count += 1
    if file_count > max_files:
        # only look at specified number of files
        break 

    with open(datafile, "r") as this_file:
        # look thru lines of file
        for line in this_file:
            #only look at mins
            day_counter = 0
            month_temp_sum = 0
            if line[17:21] == "TMIN":
                this_year = int(line[11:15]) # get year
                this_month = int(line[15:17])
                if this_year != last_year:
                    for x in range(12):
                        month_check[x] = 0

                month_check[this_month-1] = 1

                year_no = this_year - start_year 
                if year_no >= 0 and year_no < year_span:  # only look at required years
                    char_inc = 0
                    counter += 1
                    if counter % 1e4 == 0:
                        print "{0} Lines Found".format(counter)
                    for col in range(31):                       # scan thru days on each line      
                        s_temp = 21 + char_inc
                        e_temp = 21 + char_inc + 5              # isolate temp reading
                        if e_temp < len(line):                  # check for end of line (days < 31)
                            temp = float(line[s_temp:e_temp])
                            if temp < 600 and temp > -900 and temp != 0:      # ignore invalid temperature
                                day_counter     += 1
                                month_temp_sum  += temp                                
                            char_inc += 8                       # move to next temperature
                        else:
                            break
                            
                    if day_counter > monthly_limit:        #ignore months without sufficient number of days measured
                        year_temp_sum   += month_temp_sum  # add to year total
                        year_temp_count += day_counter     # add day_counter to year total
                               
                    if this_month == 12:       # check if lines for each monthhave been read
                        for x in range(11):
                            if month_check[x] == 0:
                                all_months_read = False
                                
                        if all_months_read:                  # all all months have been read then add year sums to totals          
                            temp_aves[year_no][0] += year_temp_sum 
                            temp_aves[year_no][1] += year_temp_count
                        # reste counters and flags    
                        all_months_read = True
                        year_temp_sum = 0
                        year_temp_count = 0
                         
                last_year = this_year

global_ave_temp = []
year_list = []
y = start_year

#Create arrays for ploting       
# loop thru each year         
for year_no in range(year_span):
    #ignore years for which there is no data
    if temp_aves[year_no][1] > 0:
        # calc average
        average = temp_aves[year_no][0]/(temp_aves[year_no][1]*10)
       #print year_no + start_year, temp_aves[year_no][0], temp_aves[year_no][1], average
        # append average to array
        global_ave_temp.append(average) 
        #append year to array
        year_list.append(y)
        y += 1
        
# create graph
pylab.plot(year_list, global_ave_temp, 'ro')
pylab.ylabel(u'Temperature {0}C'.format(degree_sign))
pylab.xlabel('Year')
pylab.subplots_adjust(left=0.06, bottom=0.1, right=0.97, top=0.94, wspace=0.2, hspace=0.0)
pylab.title("Average Temperatures By Year From GHCN Data - {0} Stations".format(max_files), fontweight='bold')
matplotlib.rc('font', **font)
pylab.grid(b=True, which='both', color='0.65',linestyle='-')
pylab.show()
