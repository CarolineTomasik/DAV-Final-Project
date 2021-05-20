import numpy as np
import matplotlib.pyplot as plt
import math
from utils import timestamp_to_x, string_to_x, x_to_ticks

# plot line comparison for a list of countries and a given index
def plot_global(data,countries,idx):
    plt.figure()
    print('Plotting ' + str(data[0,idx] + ' for:'))
    d = dict.fromkeys(countries)
    scale = 1
    for i in countries:
        print(i)
        d[i] = data[data[:,2]==i][:,[0,3,idx]]
        d[i][[not bool(x) for x in d[i][:, -1]], -1] = np.char.replace(d[i][[not bool(x) for x in d[i][:, -1]], -1], '', 'NaN')
        plt.plot(string_to_x(d[i][:, 1]), abs(d[i][:, 2].astype(float)) / scale, label=i, alpha = 0.8)

    plt.legend()
    plt.title(data[0][idx])
    date_min = min([min(string_to_x(d[i][:,1])) for i in countries])
    date_max = max([max(string_to_x(d[i][:,1])) for i in countries])
    ticks,labels = x_to_ticks(date_min,date_max)
    plt.xticks(ticks,labels)
    plt.savefig('compare_' + data[0][idx] + '.png')

# plot bar comparison for a list of countries and 2 given indices
def plot_global_bar(data,countries,idx):
    fig, axs = plt.subplots(2)#, figsize=(10,5))
    print('Plotting ' + str(data[0,idx[0]] )+ ', ' + str(data[0,idx[1]]) + ' for:')
    d = dict.fromkeys(countries)
    scale = 1000
    cnt = 0
    def spec(country):
        lab = ''
        if country in ['Denmark', 'Norway', 'Finland']:
            color = 'lightsteelblue'
            if country == 'Norway':
                lab = 'Scandinavia'
        elif country == 'Sweden':
            color = 'tab:blue'
            lab = 'Sweden'
        else:
            color = 'wheat'

        return color, lab
    hs0 = []; hs1 = []
    for i in countries:
        d[i] = data[data[:,2]==i][:,[0,3,idx[0],idx[1]]]
        d[i][[not bool(x) for x in d[i][:, -1]], -1] = np.char.replace(d[i][[not bool(x) for x in d[i][:, -1]], -1], '', 'NaN')
        d[i][[not bool(x) for x in d[i][:, -2]], -2] = np.char.replace(d[i][[not bool(x) for x in d[i][:, -2]], -2], '', 'NaN')

        hs1.append(abs(d[i][-1, -1].astype(float)) )
        hs0.append(abs(d[i][-1, -2].astype(float)) )
    # sort countries
    xt =[]; xl = []
    for i in np.argsort(hs0):
        cnt += 1
        axs[0].bar(cnt, hs0[i] / scale, width = 0.8, color = spec(countries[i])[0],label=spec(countries[i])[1])
        xt.append(cnt); xl.append(d[countries[i]][0,0])
    yt = np.arange(0, 120,20)
    axs[0].set_xticks(xt); axs[0].set_yticks(yt);
    axs[0].set_xticklabels(xl); axs[0].set_yticklabels([t + 'K' for t in yt.astype(str)]);
    xt = []; xl = []
    for i in np.argsort(hs1):
        cnt += 1
        axs[1].bar(cnt, hs1[i] / scale, width=0.8, color = spec(countries[i])[0],label=spec(countries[i])[1])
        xt.append(cnt); xl.append(d[countries[i]][0, 0])
    yt = np.arange(0,4)
    axs[1].set_xticks(xt); axs[1].set_yticks(yt);
    axs[1].set_xticklabels(xl); axs[1].set_yticklabels([t+'K' for t in yt.astype(str)]);

    axs[0].set_ylabel('Cases per million, cumul.')
    axs[1].set_ylabel('Deaths per million, cumul. \n')
    axs[0].legend()
    plt.savefig('bar_compare_' + data[0][idx[0]] + '.png')

data = np.genfromtxt('owid-covid-data.csv',dtype='str',delimiter=",")
columns = data[0,:]

# total_cases' 4
# new_cases' 5
# new_cases_smoothed' 6
# total_deaths' 7
# new_deaths' 8
# new_deaths_smoothed' 9
# total_cases_per_million' 10
# new_cases_per_million' 11
# new_cases_smoothed_per_million' 12
# total_deaths_per_million 13
# new_deaths_smoothed_per_million 15
# people_vaccinated_per_hundred 40
# people_fully_vaccinated_per_hundred 41
# populaiton density 45
# ...etc.

print(columns)

#countries = ["Sweden", "Germany", "Poland", "Spain", "Italy", "France"]
countries =  ["Sweden","Poland","Finland", "Denmark", "Norway", "Germany", "Spain", "Italy", "France", "Hungary"]

for i in [[10,13]]:
    plot_global_bar(data, countries, i)
    #print('No graph for ' + columns[i[0]]+', '+columns[i[1]])