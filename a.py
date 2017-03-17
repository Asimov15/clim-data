#!/usr/bin/python

from numpy import arange
import matplotlib
matplotlib.use('TkAgg') 
# import matplotlib as mpl
import matplotlib.pyplot
# import matplotlib.pyplot as plt

x1 = [1,2,3]
y1 = [4,5,6]
x2 = [1,2,3]
y2 = [5,5,5]

# initialization
fig2 = matplotlib.pyplot.figure(figsize=(8.0, 5.0)) # The size of the figure is specified as (width, height) in inches

# lines:
l1 = fig2.add_subplot(111).plot(x1,y1, label="Text $formula$", lw=2)
l2 = fig2.add_subplot(111).plot(x2,y2, label="$legend2$", lw=3)
fig2.add_subplot(111).legend((l1,l2), loc=0)

# axes:
fig2.add_subplot(111).grid(True)
fig2.add_subplot(111).set_xticks(arange(1,3,0.5))
fig2.add_subplot(111).axis(xmin=3, xmax=6) # there're also ymin, ymax
fig2.add_subplot(111).axis([0,4,3,6]) # all!
fig2.add_subplot(111).set_xlim([0,4])
fig2.add_subplot(111).set_ylim([3,6])

# labels:
fig2.add_subplot(111).set_xlabel(r"x $2^2$", fontsize=15, color = "r")
fig2.add_subplot(111).set_ylabel(r"y $2^2$")
fig2.add_subplot(111).set_title(r"title $6^4$")
fig2.add_subplot(111).text(2, 5.5, r"an equation: $E=mc^2$", fontsize=15, color = "y")
fig2.add_subplot(111).text(3, 2, unicode('f\374r', 'latin-1'))

# saving:
fig2.savefig("fig2.png")
