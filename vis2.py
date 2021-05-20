import pandas as pd
import os
import matplotlib.pyplot as plt
import datetime
import numpy as np
import math
from utils import timestamp_to_x, string_to_x, x_to_ticks, add_events
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

plt.rcParams.update({'font.size': 22})

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

def plot_avg_deaths_and_icu(icu_df, deaths_df, a=10):
    icu = icu_df.to_numpy()
    deaths = deaths_df.to_numpy()
    gs = [icu[x:(x + a),1] for x in range(0, icu.shape[0], a)]
    gs2 = [deaths[x:(x + a),1] for x in range(0, deaths.shape[0], a)]
    icu_avg = [sum(group) / len(group) for group in gs]
    deaths_avg = [sum(group) / len(group) for group in gs2]
    #print(deaths.shape, icu.shape)
    fig, ax = plt.subplots()
    cb='tab:blue'; cr='tab:orange'
    plt.plot(timestamp_to_x(icu[:,0]), icu[:,1], color=cb, alpha=0.2)
    plt.plot(timestamp_to_x(icu[::a,0]), icu_avg, color=cb, label ='ICU hospitalizations, ' +str(a)+'-days average')
    plt.plot(timestamp_to_x(deaths[:,0]), deaths[:,1], color=cr, alpha=0.2)
    plt.plot(timestamp_to_x(deaths[::a,0]), deaths_avg, color=cr, label = 'deaths, ' + str(a)+'-days average')
    date_min, date_max = min(timestamp_to_x(deaths[:, 0])), max(timestamp_to_x(deaths[:, 0]))
    ticks, labels = x_to_ticks(date_min, date_max,sparse = 2)
    plt.xticks(ticks, labels)
    plt.legend(loc='upper left')
    plt.xlim(date_min,date_max)
    #add_events(plt.gca())
    plt.ylabel('Deaths and ICU hospitalizations')
    #plt.xlabel('date')
    #plt.title('Total number of hospitalizations (icu) & deaths')
    plt.savefig('icu_and_deaths_avg_' + str(a) + '.png')

def plot_avg_cases_and_deaths(cases_df, deaths_df, a=10):

    cases = cases_df.to_numpy()
    tot_cases = cases[:, 1:].sum(axis=1)
    gs = [tot_cases[x:(x + a)] for x in range(0, len(tot_cases), a)]
    tot_cases_avg = [sum(group) / len(group) for group in gs]

    deaths = deaths_df.to_numpy()
    gs2 = [deaths[x:(x + a),1] for x in range(0, deaths.shape[0], a)]
    deaths_avg = [sum(group) / len(group) for group in gs2]

    death_rate=100 * deaths[:,1]/tot_cases[(tot_cases.shape[0] - deaths[:,1].shape[0]-1):-1];

    gs3 = [death_rate[x:(x + a)] for x in range(0, death_rate.shape[0], a)]
    death_rate_avg = [sum(group) / len(group) for group in gs3]
    fig, ax2 = plt.subplots()#figsize=(8,6))
    color = 'tab:orange'
    ax2.plot(timestamp_to_x(deaths[:, 0]), death_rate, color=color, alpha=0.2)
    l2 = ax2.plot(timestamp_to_x(deaths[:, 0])[::a], death_rate_avg, color=color, label= 'death rate, ' + str(a) + '-days average')
    ax2.set_ylabel('Death rate (%)', color=color)
    ax2.tick_params(axis='y', labelcolor=color)
    #ax2.set_xlabel('date')
    ax2.set_ylim([0, 18])

    ax1=ax2.twinx()
    color='tab:blue'
    ax1.plot(timestamp_to_x(cases[:, 0]), tot_cases, color=color, alpha=0.2)
    l1 = ax1.plot(timestamp_to_x(cases[:, 0])[::a], tot_cases_avg, color=color, label= 'cases, ' + str(a) + '-days average')
    ax1.set_ylabel('Cases (in thousands)', color=color)
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.set_yticks(np.arange(0, 30000, 5000))
    ax1.set_yticklabels([t + 'K' for t in np.arange(0, 30, 5).astype(str)])

    #plt.title('Total number of cases & death rate')
    #add_events(ax2)
    lns = l1 + l2
    labs = [l.get_label() for l in lns]
    ax1.legend(lns, labs, loc=0)
    plt.xlim([30, 430])
    date_min, date_max = min(timestamp_to_x(cases[:, 0])), max(timestamp_to_x(cases[:, 0]))
    ticks, labels = x_to_ticks(date_min, date_max)
    plt.xticks(ticks, labels)

    #axins = inset_axes(ax1, width=1.2, height=1.2)
    #plot_deaths_by_age(axins)
    plt.savefig('death_rate_avg_' + str(a) + '_inset.png')

def plot_deaths_by_age():
    gs = ['<60', '60-70', '70-80', '80-90', '90-100']
    data = [7+4+20+34+85+288,787,2832,5567,3638]
    plt.figure()
    cols=[[0.3,0,1],[0.25,0,.8],[0.2,0,.6],[0.15,0,.45],[0.1,0,.3],[0.0,0,.05]]
    _,_, p = plt.pie(data, labels = gs, autopct='%1.1f%%',colors=cols,pctdistance=0.7)
    plt.setp(p,color='w')
    plt.savefig('pie.png')

#plot_avg_cases(cases_df, a=14)
plot_deaths_by_age()
#plot_avg_deaths_and_icu(icu_df, deaths_df, a=7)
#plot_avg_cases_and_deaths(cases_df, deaths_df, a=5)
#plot_avg_cases_and_deaths(cases_df, deaths_df, a=10)
#plot_avg_cases_and_deaths(cases_df, deaths_df, a=14)