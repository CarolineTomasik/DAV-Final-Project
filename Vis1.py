#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 09:05:19 2021

@author: caroline
"""
import pandas as pd
import os
import matplotlib.pyplot as plt

#case/deaths/ICU data
#cases_df = pd.read_excel(os.getcwd() + '/Folkhalsomyndigheten_Covid19.xlsx', sheet_name='Antal per dag region')
cases_df = pd.read_excel('Folkhalsomyndigheten_Covid19.xlsx', sheet_name='Antal per dag region')
cases_df = cases_df.rename(columns ={'Statistikdatum':'date', 'Totalt_antal_fall':'cases per day'})

#icu_df = pd.read_excel(os.getcwd() + '/Folkhalsomyndigheten_Covid19.xlsx', sheet_name='Antal intensivvårdade per dag')
icu_df = pd.read_excel('Folkhalsomyndigheten_Covid19.xlsx', sheet_name='Antal intensivvårdade per dag')
icu_df.columns = ['date', 'Hospitalizations-ICU']

#deaths_df = pd.read_excel(os.getcwd() + '/Folkhalsomyndigheten_Covid19.xlsx', sheet_name='Antal avlidna per dag')
deaths_df = pd.read_excel('Folkhalsomyndigheten_Covid19.xlsx', sheet_name='Antal avlidna per dag')
deaths_df.columns = ['date', 'deaths per day']
deaths_df.drop(deaths_df.tail(1).index,inplace = True)


#vaccine data
vaccine_df = pd.read_excel(os.getcwd() + '/Folkhalsomyndigheten_Covid19_Vaccine.xlsx', sheet_name='Vaccinerade ålder')
vaccine_df = vaccine_df.rename(columns ={'Åldersgrupp':'age group', 'Antal vaccinerade':'number of vaccinated', 'Vaccinationsstatus': 'Vaccination status'})
vaccine_df.replace('Minst 1 dos', 'at least 1 dose', inplace=True)
vaccine_df.replace('Färdigvaccinerade', 'fully vaccinated', inplace=True)
vaccine_df.replace('| Sverige |', 'Sweden', inplace=True)

one_dose_df = vaccine_df.loc[(vaccine_df['Region'] == 'Sweden') & (vaccine_df['Vaccination status'] == 'at least 1 dose')]
full_dose_df = vaccine_df.loc[(vaccine_df['Region'] == 'Sweden') & (vaccine_df['Vaccination status'] == 'fully vaccinated')]

plt.bar(x='age group', height='number of vaccinated', data= one_dose_df)
plt.bar(x='age group', height='number of vaccinated', data= full_dose_df)



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

    fig, ax = plt.subplots()
    plt.plot(icu[:,0], icu[:,1], '-b', alpha=0.2)
    plt.plot(icu[::a,0], icu_avg, '-b', label = 'avg. ('+str(a)+'d) icu')
    plt.plot(deaths[:,0], deaths[:,1], '-r', alpha=0.2)
    plt.plot(deaths[::a,0], deaths_avg, '-r', label = 'avg. ('+str(a)+'d) deaths')
    plt.legend()
    plt.xlabel('date')
    plt.title('Total number of hospitalizations (icu) & deaths')
    plt.savefig('icu_and_deaths_avg_' + str(a) + '.png')


plot_avg_deaths_and_icu(icu_df, deaths_df, a=5)
plot_avg_deaths_and_icu(icu_df, deaths_df, a=10)
plot_avg_deaths_and_icu(icu_df, deaths_df, a=15)
plot_avg_cases(cases_df, a=5)
plot_avg_cases(cases_df, a=10)
plot_avg_cases(cases_df, a=15)