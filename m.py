#!/usr/bin/python
import numpy

print "0"

print "1"
month_days      = (31,28,31,30,31,30,31,31,30,31,30,31)
print "2"
m = numpy.zeros(12)
a = 0
b = -1
for x in range(12):
    b += month_days[x]
    m[x] = (a+b)/2
    print m
    a += month_days[x]
    
