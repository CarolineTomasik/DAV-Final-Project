import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np

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

#age_df = pd.read_excel('Folkhalsomyndigheten_Covid19.xls', sheet_name='Totalt antal per åldersgrupp')
#age_df = age_df.rename(columns ={'Åldersgrupp':'age group', 'Totalt_antal_fall':'cases per day','Totalt_antal_avlidna':'deaths per day'})

def plot_avg_cases(cases_df, a=10):
    cases = cases_df.to_numpy()
    tot_cases = cases[:,1:].sum(axis=1)

    gs = [tot_cases[x:(x+a)] for x in range(0,len(tot_cases),a)]
    tot_cases_avg = [sum(group)/len(group) for group in gs]

    fig, ax = plt.subplots()
    plt.plot(cases[:,0], tot_cases, '-b', alpha=0.2)
    plt.plot(cases[::a,0], tot_cases_avg, '-b', label = 'avg. ('+str(a)+'d) total cases')
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
    unempl=[8.2,9,9.8,8.9,8.8,8.3,7.8,7.7,8.2,9.3,9.7,10]
    unempl_dates=['2020-04-01','2020-05-01','2020-06-01','2020-07-01','2020-08-01','2020-09-01','2020-10-01','2020-11-01','2020-12-01','2021-01-01','2021-02-01','2021-03-01',]
    fig, ax = plt.subplots()
    plt.plot(icu[:,0], icu[:,1], '-b', alpha=0.2)
    plt.plot(icu[::a,0], icu_avg, '-b', label = 'avg. ('+str(a)+'d) icu')
    plt.plot(deaths[:,0], deaths[:,1], '-r', alpha=0.2)
    plt.plot(deaths[::a,0], deaths_avg, '-r', label = 'avg. ('+str(a)+'d) deaths')
    plt.scatter(unempl_dates,10*np.array(unempl), 10, 'k',label='unemployment rate x 10')
    plt.legend()
    plt.xlabel('date')
    plt.title('Total number of hospitalizations (icu) & deaths')
    plt.savefig('icu_and_deaths_avg_unempl_' + str(a) + '.png')


plot_avg_deaths_and_icu(icu_df, deaths_df, a=5)
plot_avg_deaths_and_icu(icu_df, deaths_df, a=10)
plot_avg_deaths_and_icu(icu_df, deaths_df, a=15)
plot_avg_cases(cases_df, a=5)
plot_avg_cases(cases_df, a=10)
plot_avg_cases(cases_df, a=15)