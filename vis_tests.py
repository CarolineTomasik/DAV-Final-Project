import matplotlib.pyplot as plt
import numpy as np
import csv
import pandas as pd
from utils import timestamp_to_x, string_to_x, x_to_ticks


def plot_avg_tests(data_raw,a):

    dates = data_raw[1:,0]
    counts = [float(v.replace("'", '')) for v in data_raw[1:,1]]
    tot_counts = [sum(counts[i:i+3]) for i in np.arange(0,len(counts),3)]
    cla = data_raw[1:,2]

    gs = [tot_counts[x:(x + a)] for x in range(0, len(tot_counts), a)]
    tot_counts_avg = [sum(group) / len(group) for group in gs]
    plt.figure()
    plt.plot(string_to_x(dates[::3]), tot_counts, color='tab:green',alpha=0.2)
    plt.plot(string_to_x(dates[::3])[::a], tot_counts_avg, color='tab:green')
    date_min, date_max = min(string_to_x(dates[::3])), max(string_to_x(dates[::3]))
    ticks, labels = x_to_ticks(date_min, date_max)
    plt.xticks(ticks, labels)
    plt.xlabel('date')
    plt.ylabel('tests')
    plt.savefig('tests_'+str(a)+'.png')

def plot_avg_tests_and_deaths(tests,deaths_df,a=10):
    dates = tests[1:,0]
    counts = [float(v.replace("'", '')) for v in tests[1:,1]]
    tot_counts = [sum(counts[i:i+3]) for i in np.arange(0,len(counts),3)]
    cla = tests[1:,2]
    deaths = deaths_df.to_numpy()
    gs = [deaths[x:(x + a), 1] for x in range(0, deaths.shape[0], a)]
    deaths_avg = [sum(group) / len(group) for group in gs]

    gs = [tot_counts[x:(x + a)] for x in range(0, len(tot_counts), a)]
    tot_counts_avg = [sum(group) / len(group) for group in gs]
    plt.figure()
    plt.plot(string_to_x(dates[::3]), 1*np.array(tot_counts), color='tab:green',alpha=0.2)
    plt.plot(string_to_x(dates[::3])[::a], 1*np.array(tot_counts_avg), color='tab:green',label='tests')
    plt.plot(timestamp_to_x(deaths[:,0]), 10*deaths[:,1], color='tab:red',alpha=0.2)
    plt.plot(timestamp_to_x(deaths[:,0])[::a], 10*np.array(deaths_avg), color='tab:red',label='deaths x 10')
    plt.legend()
    plt.xlabel('date')
    plt.ylabel('tests')
    date_min, date_max = min(timestamp_to_x(deaths[:, 0])), max(timestamp_to_x(deaths[:, 0]))
    ticks, labels = x_to_ticks(date_min, date_max)
    plt.xticks(ticks, labels)
    plt.savefig('tests_and_deaths_'+str(a)+'.png')

def plot_avg_tests_and_cases(tests,cases_df,a=10):
    dates = tests[1:,0]
    counts = [float(v.replace("'", '')) for v in tests[1:,1]]
    tot_counts = [sum(counts[i:i+3]) for i in np.arange(0,len(counts),3)]
    cla = tests[1:,2]
    cases = cases_df.to_numpy()
    gs = [cases[x:(x + a), 1] for x in range(0, cases.shape[0], a)]
    cases_avg = [sum(group) / len(group) for group in gs]

    gs = [tot_counts[x:(x + a)] for x in range(0, len(tot_counts), a)]
    tot_counts_avg = [sum(group) / len(group) for group in gs]
    plt.figure()
    plt.plot(string_to_x(dates[::3]), 1*np.array(tot_counts), color='tab:green',alpha=0.2)
    plt.plot(string_to_x(dates[::3])[::a], 1*np.array(tot_counts_avg), color='tab:green',label='tests')
    plt.plot(timestamp_to_x(cases[:,0]), cases[:,1], color='tab:red',alpha=0.2)
    plt.plot(timestamp_to_x(cases[:,0])[::a], np.array(cases_avg), color='tab:red',label='cases')
    plt.legend()
    plt.xlabel('date')
    plt.ylabel('tests')
    date_min, date_max = min(timestamp_to_x(cases[:, 0])), max(timestamp_to_x(cases[:, 0]))
    ticks, labels = x_to_ticks(date_min, date_max)
    plt.xticks(ticks, labels)
    plt.savefig('tests_and_cases_'+str(a)+'.png')

tests = np.genfromtxt('NPC-statistics-data-set.csv',dtype='str',delimiter=",")

deaths_df = pd.read_excel('Folkhalsomyndigheten_Covid19.xls', sheet_name='Antal avlidna per dag')
deaths_df.columns = ['date', 'deaths per day']
deaths_df.drop(deaths_df.tail(1).index,inplace = True)

cases_df = pd.read_excel('Folkhalsomyndigheten_Covid19.xls', sheet_name='Antal per dag region')
cases_df = cases_df.rename(columns ={'Statistikdatum':'date', 'Totalt_antal_fall':'cases per day'})

plot_avg_tests(tests,5)
plot_avg_tests(tests,10)
plot_avg_tests(tests,15)
plot_avg_tests_and_deaths(tests,deaths_df)
plot_avg_tests_and_cases(tests,cases_df)