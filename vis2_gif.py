import pandas as pd
import os
import matplotlib.pyplot as plt
import datetime
import numpy as np
import math
from utils import timestamp_to_x, string_to_x, x_to_ticks, add_events
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import matplotlib.animation as animation

#plt.rcParams.update({'font.size': 22})

cases_df = pd.read_excel('Folkhalsomyndigheten_Covid19.xls', sheet_name='Antal per dag region')
cases_df = cases_df.rename(columns ={'Statistikdatum':'date', 'Totalt_antal_fall':'cases per day'})


icu_df = pd.read_excel('Folkhalsomyndigheten_Covid19.xls', sheet_name='Antal intensivvårdade per dag')
icu_df.columns = ['date', 'Hospitalizations-ICU']

deaths_df = pd.read_excel('Folkhalsomyndigheten_Covid19.xls', sheet_name='Antal avlidna per dag')
deaths_df.columns = ['date', 'deaths per day']
deaths_df.drop(deaths_df.tail(1).index,inplace = True)


def plot_avg_cases(cases_df, a=10):
    cases = cases_df.to_numpy()
    tot_cases = cases[:,1:].sum(axis=1)

    gs = [tot_cases[x:(x+a)] for x in range(0,len(tot_cases),a)]
    tot_cases_avg = [sum(group)/len(group) for group in gs]

    fig, ax = plt.subplots(figsize=(6,4.5))
    cb='tab:blue'; cr='tab:red'
    plt.plot(timestamp_to_x(cases[:,0]), tot_cases, color=cb, alpha=0.15)
    plt.plot(timestamp_to_x(cases[::a,0]), tot_cases_avg, color=cb, label = str(a)+'-days average')
    date_min, date_max = min(timestamp_to_x(cases[:, 0])), max(timestamp_to_x(cases[:, 0]))
    ticks, labels = x_to_ticks(date_min, date_max, sparse = 2)
    add_events(plt.gca())
    plt.xticks(ticks, labels)
    plt.yticks(np.arange(0,30000,5000),[t+'K' for t in np.arange(0,30,5).astype(str)])
    plt.legend(loc = 'upper left')
    plt.ylim([0,24000])
    plt.xlim([date_min,date_max])
    plt.xlabel('date')
    plt.ylabel('Cases (in thousands)')
    #plt.title('Total number of cases')
    plt.savefig('cases_avg_' + str(a) + '.png')





def update_plot(num, tot_cases, tot_cases_avg, xvec):
    plt.cla()
    #plt.plot(xvec[:num], tot_cases[:num],color='tab:blue',alpha=0.25)
    plt.plot(xvec[:num], tot_cases_avg[:num],color='tab:blue', label='weekly average')
    date_min, date_max = min(timestamp_to_x(cases[:, 0])), max(timestamp_to_x(cases[:, 0]))
    ticks, labels = x_to_ticks(date_min, date_max, sparse = 2)
    plt.ylabel('Cases (in thousands)')
    plt.xticks(ticks, labels)
    plt.legend(loc='upper left')
    plt.yticks(np.arange(0,30000,5000),[t+'K' for t in np.arange(0,30,5).astype(str)])
    plt.ylim([0,17000])
    plt.xlim([date_min,date_max])

fig, ax = plt.subplots()
cases = cases_df.to_numpy()
a=7
l = cases[::a,:].shape[0]
tot_cases = cases[:, 1:].sum(axis=1)

gs = [tot_cases[x:(x + a)] for x in range(0, len(tot_cases), a)]
tot_cases_avg = [sum(group) / len(group) for group in gs]
xvec = timestamp_to_x(cases[:, 0])[::a]

animation = animation.FuncAnimation(fig, update_plot, l, fargs=(tot_cases, tot_cases_avg, xvec, ) )
animation.save('avg_cases.gif', writer='imagemagick', fps=10)

