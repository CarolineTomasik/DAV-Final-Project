import pandas as pd
import os
import matplotlib.pyplot as plt
import datetime
import numpy as np
import math
from matplotlib.collections import PatchCollection
from matplotlib.patches import Rectangle


def timestamp_to_x(X):
    XX=[]
    for i in range(0, len(X)):
        stamp = X[i]
        XX.append((int(stamp.strftime("%Y")) - 2020 )*(12*31) + 31 * (int(stamp.strftime("%m")) - 1) + int(stamp.strftime("%d")))
    return XX

def string_to_x(X):
    XX = []
    for i in range(0, len(X)):
        date = X[i]
        date = date.split('-')
        XX.append((12 * 31) * (int(date[0]) - 2020) + 31 * (int(date[1]) - 1) + int(date[2]))
    return XX

def x_to_ticks(xmin, xmax, sparse = 1):
    xt = np.arange(math.ceil(xmin/31) * 31, math.ceil(xmax/31) * 31, 31) - 15.5;
    #print(xt)
    labs =  ['Jan\n 20', 'Feb\n 20 ', 'Mar\n 20 ', 'Apr\n 20 ', 'May\n 20 ', 'Jun\n 20 ', 'Jul\n 20 ', 'Aug\n 20 ', 'Sep\n 20 ',
               'Oct\n 20 ', 'Nov\n 20 ', 'Dec\n 20 ', 'Jan\n 21 ', 'Feb\n 21', 'Mar\n 21', 'Apr\n 21', 'May\n 21']
    xl = labs[math.ceil(xmin/31):math.ceil(xmax/31)]
    return xt[::sparse],xl[::sparse]

def add_events(ax):
    ds = np.array([[2020, 11, 3], [2020, 27, 3], [2020, 7, 12], [2020, 14, 12]])#, [2021, 1, 1]])#, [2021, 11, 2]])
    ds = np.array([[2020, 11, 3], [2020, 27, 3], [2020, 7, 12], [2021, 1, 1]])#, [2021, 1, 1]])#, [2021, 11, 2]])

    events = ['500+\ngatherings\nbanned', '50+\ngatherings\nbanned', 'distant\nlearning\n16+', 'distant\nlearning\n13+',
              'schools\nreopened']#, '80+% elderly vacc.']
    ymax = ax.get_ylim()[1]
    pos = np.array([0.1,0.3,0.55,0.75,0.95])*ymax
    pos= np.array([0.2,0.45,2,2])*ymax
    for i in range(len(ds)):
        yr = ds[i, 0];
        m = ds[i, 2];
        d = ds[i, 1];
        date = (datetime.datetime(yr, m, d, 0, 0))
        ax.plot(timestamp_to_x([date]) * 10, np.linspace(0, ymax, 10), 'k', linestyle = 'dotted',  alpha=0.25)
        ax.text(timestamp_to_x([date])[0] , pos[i]  , events[i])
        #schools closed patch
        if i==2:
           ax.add_patch(Rectangle((timestamp_to_x([date])[0], 0), 23,ymax,edgecolor='g',facecolor='k',alpha=0.1))
           ax.text(timestamp_to_x([date])[0]-10,0.75*ymax,'schools\n closed ')
