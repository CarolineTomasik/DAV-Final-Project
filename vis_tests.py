import matplotlib.pyplot as plt
import numpy as np
import csv
import pandas as pd

def string_to_x(X):
    #print('len x = ' + str(X.shape))
    #print(X[:5])
    XX=[]
    for i in range(0, len(X)):
        date = X[i]
        date = date.split('-')
        XX.append((12*31)*(int(date[0])-2020)+31*(int(date[1])-1)+int(date[2]))

    return XX

def timestamp_to_x(X):
    #print('len x = ' + str(X.shape))
    #print(X[:5])
    XX=[]
    for i in range(0, len(X)):
        stamp = X[i]
        XX.append((int(stamp.strftime("%Y")) - 2020 )*(12*31) + 31 * (int(stamp.strftime("%m")) - 1) + int(stamp.strftime("%d")))
    return XX


def plot_avg_tests(data_raw,a):
    dates = data_raw[1:,0]
    counts = [float(v.replace("'", '')) for v in data_raw[1:,1]]
    tot_counts = [sum(counts[i:i+3]) for i in np.arange(0,len(counts),3)]
    cla = data_raw[1:,2]
    #print(string_to_x(dates[::3]))

    gs = [tot_counts[x:(x + a)] for x in range(0, len(tot_counts), a)]
    tot_counts_avg = [sum(group) / len(group) for group in gs]
    plt.figure()
    plt.plot(string_to_x(dates[::3]), tot_counts, color='tab:green',alpha=0.2)
    plt.plot(string_to_x(dates[::3])[::a], tot_counts_avg, color='tab:green')
    plt.xlim([30, 430])
    plt.xlabel('date')
    plt.ylabel('tests')
    plt.xticks(np.arange(45, 410, 30),
               ['Feb\n 20 ', 'Mar\n 20 ', 'Apr\n 20 ', 'May\n 20 ', 'Jun\n 20 ', 'Jul\n 20 ', 'Aug\n 20 ', 'Sep\n 20 ',
                'Oct\n 20 ', 'Nov\n 20 ', 'Dec\n 20 ', 'Jan\n 21 ', 'Feb\n 21'], rotation=0)
    plt.savefig('tests_'+str(a)+'.png')

def plot_avg_tests_and_deaths(tests,deaths_df,a):
    dates = tests[1:,0]
    counts = [float(v.replace("'", '')) for v in tests[1:,1]]
    tot_counts = [sum(counts[i:i+3]) for i in np.arange(0,len(counts),3)]
    cla = tests[1:,2]
    deaths = deaths_df.to_numpy()
    gs = [deaths[x:(x + a), 1] for x in range(0, deaths.shape[0], a)]
    deaths_avg = [sum(group) / len(group) for group in gs]

    #death_rate=100 * deaths[:len(tot_counts),1]/(np.array(tot_counts)+1e-5);
    #gs3 = [death_rate[x:(x + a)] for x in range(0, death_rate.shape[0], a)]
    #death_rate_avg = [sum(group) / len(group) for group in gs3]

    gs = [tot_counts[x:(x + a)] for x in range(0, len(tot_counts), a)]
    tot_counts_avg = [sum(group) / len(group) for group in gs]
    plt.figure()
    plt.plot(string_to_x(dates[::3]), 1*np.array(tot_counts), color='tab:green',alpha=0.2)
    plt.plot(string_to_x(dates[::3])[::a], 1*np.array(tot_counts_avg), color='tab:green',label='tests')
    plt.plot(timestamp_to_x(deaths[:,0]), 10*deaths[:,1], color='tab:red',alpha=0.2)
    plt.plot(timestamp_to_x(deaths[:,0])[::a], 10*np.array(deaths_avg), color='tab:red',label='deaths x 10')
    plt.xlim([30, 430])
    plt.xlim([30, 430])
    plt.legend()
    plt.xlabel('date')
    plt.ylabel('tests')
    plt.xticks(np.arange(45, 410, 30),
               ['Feb\n 20 ', 'Mar\n 20 ', 'Apr\n 20 ', 'May\n 20 ', 'Jun\n 20 ', 'Jul\n 20 ', 'Aug\n 20 ', 'Sep\n 20 ',
                'Oct\n 20 ', 'Nov\n 20 ', 'Dec\n 20 ', 'Jan\n 21 ', 'Feb\n 21'], rotation=0)
    plt.savefig('tests_and_deaths_'+str(a)+'.png')



tests = np.genfromtxt('NPC-statistics-data-set.csv',dtype='str',delimiter=",")

deaths_df = pd.read_excel('Folkhalsomyndigheten_Covid19.xls', sheet_name='Antal avlidna per dag')
deaths_df.columns = ['date', 'deaths per day']
deaths_df.drop(deaths_df.tail(1).index,inplace = True)

plot_avg_tests(tests,5)
plot_avg_tests(tests,10)
plot_avg_tests(tests,15)
plot_avg_tests_and_deaths(tests,deaths_df,5)
plot_avg_tests_and_deaths(tests,deaths_df,10)
plot_avg_tests_and_deaths(tests,deaths_df,15)