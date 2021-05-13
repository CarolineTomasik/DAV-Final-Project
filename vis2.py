import pandas as pd
import os
import matplotlib.pyplot as plt
import datetime
import numpy as np
from matplotlib.collections import PatchCollection
from matplotlib.patches import Rectangle

#cases_df = pd.read_excel(os.getcwd() + '/Folkhalsomyndigheten_Covid19.xlsx', sheet_name='Antal per dag region')
cases_df = pd.read_excel('Folkhalsomyndigheten_Covid19.xls', sheet_name='Antal per dag region')
cases_df = cases_df.rename(columns ={'Statistikdatum':'date', 'Totalt_antal_fall':'cases per day'})

#icu_df = pd.read_excel(os.getcwd() + '/Folkhalsomyndigheten_Covid19.xlsx', sheet_name='Antal intensivvårdade per dag')
icu_df = pd.read_excel('Folkhalsomyndigheten_Covid19.xls', sheet_name='Antal intensivvårdade per dag')
icu_df.columns = ['date', 'Hospitalizations-ICU']

#deaths_df = pd.read_excel(os.getcwd() + '/Folkhalsomyndigheten_Covid19.xlsx', sheet_name='Antal avlidna per dag')
deaths_df = pd.read_excel('Folkhalsomyndigheten_Covid19.xls', sheet_name='Antal avlidna per dag')
deaths_df.columns = ['date', 'deaths per day']
deaths_df.drop(deaths_df.tail(1).index,inplace = True)


def plot_avg_cases(cases_df, a=10):
    cases = cases_df.to_numpy()
    tot_cases = cases[:,1:].sum(axis=1)

    gs = [tot_cases[x:(x+a)] for x in range(0,len(tot_cases),a)]
    tot_cases_avg = [sum(group)/len(group) for group in gs]

    fig, ax = plt.subplots()
    cb='tab:blue'; cr='tab:red'
    plt.plot(cases[:,0], tot_cases, color=cb, alpha=0.2)
    plt.plot(cases[::a,0], tot_cases_avg, color=cb, label = 'avg. ('+str(a)+'d) total cases')
    plt.legend()
    plt.xlabel('date')
    plt.title('Total number of cases')
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
    cb='tab:blue'; cr='tab:red'
    plt.plot(icu[:,0], icu[:,1], color=cb, alpha=0.2)
    plt.plot(icu[::a,0], icu_avg, color=cb, label = 'avg. ('+str(a)+'d) icu')
    plt.plot(deaths[:,0], deaths[:,1], color=cr, alpha=0.2)
    plt.plot(deaths[::a,0], deaths_avg, color=cr, label = 'avg. ('+str(a)+'d) deaths')
    plt.legend()
    plt.xlabel('date')
    plt.title('Total number of hospitalizations (icu) & deaths')
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
    #print(deaths[:,0][0:5],deaths[::a,0][0:5])
    fig, ax2 = plt.subplots(figsize=(8,6))
    color = 'tab:red'
    ax2.plot(timestamp_to_x(deaths[:, 0]), death_rate, color=color, alpha=0.2)
    ax2.plot(timestamp_to_x(deaths[:, 0])[::a], death_rate_avg, color=color, label='avg. (' + str(a) + 'd) deaths')
    ax2.set_ylabel('death rate (%)', color=color)
    ax2.tick_params(axis='y', labelcolor=color)
    ax2.set_xlabel('date')
    ax2.set_ylim([0, 18])

    ax1=ax2.twinx()
    color='tab:blue'
    ax1.plot(timestamp_to_x(cases[:, 0]), tot_cases, color=color, alpha=0.2)
    ax1.plot(timestamp_to_x(cases[:, 0])[::a], tot_cases_avg, color=color, label='avg. (' + str(a) + 'd) total cases')
    ax1.set_ylabel('cases', color=color)
    ax1.tick_params(axis='y', labelcolor=color)
    #plt.legend()
    plt.title('Total number of cases & death rate')
    add_events(ax2)
    plt.xlim([30, 430])
    plt.xticks(np.arange(45,410,30), ['Feb\n 20 ', 'Mar\n 20 ', 'Apr\n 20 ', 'May\n 20 ', 'Jun\n 20 ', 'Jul\n 20 ', 'Aug\n 20 ', 'Sep\n 20 ', 'Oct\n 20 ', 'Nov\n 20 ', 'Dec\n 20 ', 'Jan\n 21 ', 'Feb\n 21' ], fontsize=26,rotation=90)
    plt.savefig('death_rate_avg_' + str(a) + '_events.png')


def add_events(ax):
        ds=np.array([[2020,11,3],[2020,27,3],[2020,7,12],[2020,14,12],[2021,1,1],[2021,11,2]])
        events=['banned 500+ gatherings','banned 50+ gatherings','distant learning 16+','distant learning 13+','schools reopened','80+% elderly vacc.']
        for i in range(6):
            yr=ds[i,0];m=ds[i,2];d=ds[i,1];
            date = (datetime.datetime(yr,m,d,0,0))
            ax.plot(timestamp_to_x([date])*10,np.linspace(0,100,10),'--k',alpha=0.3)
            ax.text(timestamp_to_x([date])[0]-15,16-i,events[i])

            ##schools closed patch
            #if i==2:
            #    ax.add_patch(Rectangle((timestamp_to_x([date])[0], 0), 23,100,edgecolor='g',facecolor='k',alpha=0.1))
            #    ax.text(timestamp_to_x([date])[0]-18,14,'schools closed')

def timestamp_to_x(X):
    XX=[]
    for i in range(0, len(X)):
        stamp = X[i]
        XX.append((int(stamp.strftime("%Y")) - 2020 )*(12*30) + 30 * (int(stamp.strftime("%m")) - 1) + int(stamp.strftime("%d")))
    return XX




#plot_avg_deaths_and_icu(icu_df, deaths_df, a=5)
#plot_avg_deaths_and_icu(icu_df, deaths_df, a=10)
#plot_avg_deaths_and_icu(icu_df, deaths_df, a=15)
#plot_avg_cases(cases_df, a=5)
#plot_avg_cases(cases_df, a=10)
#plot_avg_cases(cases_df, a=15)
plot_avg_cases_and_deaths(cases_df, deaths_df, a=5)
plot_avg_cases_and_deaths(cases_df, deaths_df, a=10)
plot_avg_cases_and_deaths(cases_df, deaths_df, a=15)