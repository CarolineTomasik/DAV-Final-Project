import numpy as np
import matplotlib.pyplot as plt
import math

# utils
def string_to_x(X):
    XX = []
    for i in range(0, len(X)):
        date = X[i]
        date = date.split('-')
        XX.append((12 * 31) * (int(date[0]) - 2020) + 31 * (int(date[1]) - 1) + int(date[2]))
    return XX

def x_to_ticks(xmin,xmax):
    xt = np.arange(math.ceil(xmin/31) * 31, math.ceil(xmax/31) * 31, 31) - 15.5;
    labs =  ['Jan\n 20', 'Feb\n 20 ', 'Mar\n 20 ', 'Apr\n 20 ', 'May\n 20 ', 'Jun\n 20 ', 'Jul\n 20 ', 'Aug\n 20 ', 'Sep\n 20 ',
               'Oct\n 20 ', 'Nov\n 20 ', 'Dec\n 20 ', 'Jan\n 21 ', 'Feb\n 21', 'Mar\n 21', 'Apr\n 21', 'May\n 21']
    xl = labs[math.ceil(xmin/31):math.ceil(xmax/31)]
    return xt,xl


# plot comparison for a list of countries and a given index
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
    #plt.ylabel(data[0,idx])
    plt.savefig('compare_' + data[0][idx] + '.png')


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
# ...etc.

#print(columns[40:])

#countries = ['Sweden', "Germany", "Poland", "Spain", "Italy", "France"]
countries =  ["Sweden", "Denmark", "Finland", "Norway"]

for i in [10, 12, 13, 15, 40, 41]:
    try: plot_global(data, countries, i)
    except: print('No graph for ' + columns[i])