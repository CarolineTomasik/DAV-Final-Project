# let's try fitting
import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from utils import *

plt.rcParams.update({'font.size': 14.5})

# 1. Cumulative cases

cases_df = pd.read_excel('Folkhalsomyndigheten_Covid19.xls', sheet_name='Antal per dag region')
cases_df = cases_df.rename(columns ={'Statistikdatum':'date', 'Totalt_antal_fall':'cases per day'})

cases = cases_df.to_numpy()
tot_cases = cases[:,1:].sum(axis=1)

cumul = []
c = 0
for i in range(len(tot_cases)):
    c += tot_cases[i]
    cumul.append(c)

plt.plot(timestamp_to_x(cases[:,0]), cumul)
plt.xlim([30, 430])
plt.xlabel('date')
plt.ylabel('cumulative cases')
plt.xticks(np.arange(45, 410, 30),
           ['Feb\n 20 ', 'Mar\n 20 ', 'Apr\n 20 ', 'May\n 20 ', 'Jun\n 20 ', 'Jul\n 20 ', 'Aug\n 20 ', 'Sep\n 20 ',
            'Oct\n 20 ', 'Nov\n 20 ', 'Dec\n 20 ', 'Jan\n 21 ', 'Feb\n 21'], rotation=0)
plt.savefig('cumul.png')


# fitting an exp function of form: y = a*np.exp((t+b)/c)

fit = curve_fit(lambda t,a,b,c: a*np.exp((t+b)/c),timestamp_to_x(cases[:,0]), cumul, p0=(6,140,46))
#print(fit[0])
plt.figure(figsize=(8,6))
plt.plot(timestamp_to_x(cases[:,0]),fit[0][0] * np.exp( (np.array(timestamp_to_x(cases[:,0]))+fit[0][1])/fit[0][2] ),'--k',alpha=0.3)
plt.plot(timestamp_to_x(cases[:,0]), cumul)
#plt.plot(timestamp_to_x(cases[:,0]), 6*np.exp((np.array(timestamp_to_x(cases[:,0]))+140)/46 + 0))

plt.xlim([30, 430])
plt.xlabel('date')
plt.ylabel('cumulative cases')
plt.xticks(np.arange(45, 410, 30),
           ['Feb\n 20 ', 'Mar\n 20 ', 'Apr\n 20 ', 'May\n 20 ', 'Jun\n 20 ', 'Jul\n 20 ', 'Aug\n 20 ', 'Sep\n 20 ',
            'Oct\n 20 ', 'Nov\n 20 ', 'Dec\n 20 ', 'Jan\n 21 ', 'Feb\n 21'], rotation=0)
plt.savefig('cumul_fit1.png')

#look at the stages
#plt.figure()
#plt.plot(timestamp_to_x(cases[:,0])[:150], cumul[:150])
#plt.plot(timestamp_to_x(cases[:,0])[150:265], cumul[150:265])
#plt.plot(timestamp_to_x(cases[:,0])[265:340], cumul[265:340])
#plt.plot(timestamp_to_x(cases[:,0])[340:], cumul[340:])
#plt.savefig('cumul_tst.png')

#2. Cumulative cases divided into stages

# fitting 2 exp functions: y = a*np.exp((t+b)/c)
fit1 = curve_fit(lambda t,a,b,c: a*np.exp((t+b)/c),timestamp_to_x(cases[:150,0]), cumul[:150], p0=(6,140,46))
fit2 = curve_fit(lambda t,a,b,c: a*np.exp((t+b)/c),timestamp_to_x(cases[265:340,0]), cumul[265:340], p0=(6,140,46))

plt.figure(figsize=(8,5))
plt.ylim([0, 1.75e6])
lab = 'fit: $y =a \cdot exp(\\frac{x+b}{c}$)'
plt.plot(timestamp_to_x(cases[:,0]),fit1[0][0] * np.exp( (np.array(timestamp_to_x(cases[:,0]))+fit1[0][1])/fit1[0][2] ),'k',linestyle='dotted',alpha=1,label=lab)
plt.plot(timestamp_to_x(cases[:,0]),fit2[0][0] * np.exp( (np.array(timestamp_to_x(cases[:,0]))+fit2[0][1])/fit2[0][2] ),'k',linestyle='dotted',alpha=1)
plt.plot(timestamp_to_x(cases[:,0]), cumul)
date_min, date_max = min(timestamp_to_x(cases[:, 0])), max(timestamp_to_x(cases[:, 0]))
ticks, labels = x_to_ticks(date_min, date_max,sparse = 2)
plt.xticks(ticks, labels)
plt.legend(loc='upper left')
plt.xlim(date_min,date_max)
plt.ylim([0,1.4*1e6])
plt.yticks(np.arange(0,1.6,0.2)*1e6, [t+'K' for t in np.arange(0,1600,200).astype(str)])
#plt.xlabel('date')
plt.ylabel('Cases, cumul. (in thousands)')


plt.savefig('cumul_fit2.png')


# 3. Correlation of unemployment data with bimodal data: deaths

# unemployment data
unemp = np.genfromtxt('DP_LIVE_20042021212852502.csv',dtype='str',delimiter=",")
unemp = unemp[unemp[:,0]=='SWE'][5:,-2].astype(float)
print(unemp)
# deaths data
deaths_df = pd.read_excel('Folkhalsomyndigheten_Covid19.xls', sheet_name='Antal avlidna per dag')
deaths_df.columns = ['date', 'deaths per day']
deaths_df.drop(deaths_df.tail(1).index,inplace = True)
deaths = deaths_df.to_numpy()
# monthly average
deaths_m_avg = []
months = list(range(3,13)) + [1,2,3]
y = 2020
for m in months:
    l=[]
    for i in range(0, deaths.shape[0]):
        if int(deaths[i,0].strftime("%m"))==m and int(deaths[i,0].strftime("%Y"))==y:
            l.append(deaths[i,1])
    print(l)
    deaths_m_avg.append(np.mean(l))
    if m==12: y=2021

#normalize etc.
deaths_m_avg = np.array(deaths_m_avg)
deaths_m_avg = deaths_m_avg/max(deaths_m_avg)
deaths_m_avg = deaths_m_avg - min(deaths_m_avg)
deaths_m_avg = deaths_m_avg/max(deaths_m_avg)
unemp = np.array(unemp)
unemp = unemp/max(unemp)
unemp = unemp - min(unemp)
unemp = unemp/max(unemp)

q=np.corrcoef(deaths_m_avg[:-1],unemp)

plt.figure()
plt.plot(deaths_m_avg)
plt.plot(unemp)
plt.xticks([])
plt.xlabel('time')
plt.title('Deaths vs unemployment, corr = %.3f' % q[1,0])
plt.savefig('corr.png')

print(q)# very weak anti-correlation...