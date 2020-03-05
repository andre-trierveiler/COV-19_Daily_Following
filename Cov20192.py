# -*- coding: utf-8 -*-
"""
Created on Sat Feb 29 14:16:37 2020

@author: andre
# github data https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_daily_reports

"""

import pandas as pd
import glob as gl
from datetime import datetime as dt
from datetime import timedelta
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

dt_inicial = '2020-01-22'
dt_final = (dt.today()+timedelta(days=-1)).strftime('%Y-%m-%d')

datas = pd.DataFrame(pd.date_range(dt_inicial, dt_final).tolist(), columns =['Data'])
diretorio = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/'
datas['Arquivo'] = diretorio + pd.to_datetime(datas['Data']).dt.strftime('%m-%d-%Y').astype(str) + '.csv' 

df_cov = pd.DataFrame()

for f in datas.index:
    df = pd.read_csv(datas.Arquivo[f])
    df['Date'] = datas.Data[f]
    df_cov =  pd.concat([df_cov, df], ignore_index = True)

df_cov2 = pd.concat([pd.read_csv(f) for f in datas.Arquivo], ignore_index = True)
df_sars = pd.read_csv('https://raw.githubusercontent.com/andre-trierveiler/COV-19_Daily_Following/master/data/SARS_data_old.csv')

df_cov['Province/State'] = df_cov['Province/State'].fillna('Others')
df_cov2['Province/State'] = df_cov2['Province/State'].fillna('Others')



df_cov['Cases'] = df_cov['Confirmed'].fillna(0) - df_cov['Deaths'].fillna(0) -  df_cov['Recovered'].fillna(0)
df_sars['Cases'] = df_sars['Cumulative number of case(s)'].fillna(0) - df_sars['Number of deaths'].fillna(0) -  df_sars['Number recovered'].fillna(0)

Pais = 'Brazil'
Pais_sars = 'Brazil'
 
df = df_cov[df_cov['Country/Region'] == Pais]
df = df.groupby(['Country/Region','Date']).sum().reset_index()

df['Recover Rate'] = df['Recovered'].fillna(0)/df['Confirmed']
df['Death Rate'] = df['Deaths'].fillna(0)/df['Confirmed']

df_b = df_sars[df_sars['Country'] == Pais_sars]
df_b = df_b.groupby(['Country','Date']).sum().reset_index()


df_b['Recover Rate'] = df_b['Number recovered'].fillna(0)/df_b['Cumulative number of case(s)']
df_b['Death Rate'] = df_b['Number of deaths'].fillna(0)/df_b['Cumulative number of case(s)']

sns.set(style="darkgrid", palette="Set2")

fig, ax = plt.subplots()
ax.stackplot(df.index,[ df['Recovered'], df['Deaths'],  df['Cases']], labels=['Recovered','Death','Diagnosed'], alpha=0.4 )
ax.legend(loc='upper right')
plt.title('COV-19 -'+ Pais)
plt.show()

fig, bx = plt.subplots()
bx.stackplot(df_b.index,[df_b['Number recovered'], df_b['Number of deaths'], df_b['Cases']], labels=['Recovered','Death','Diagnosed'], alpha=0.4 )
bx.legend(loc='upper right')
plt.title('SARS - ' + Pais_sars)
plt.show()
 
fig, cx = plt.subplots()
cx.set_title('COV-19 Death Rates - ' + Pais)
cx.set_ylabel('Rate (%)')
cx.plot(df.index, df['Death Rate']*100, marker='o', markerfacecolor = 'white',markersize=4,linestyle='-')
#cx.plot(df.index, df['Recover Rate']*100, marker='o', markerfacecolor = 'white',markersize=4,linestyle='-')
cx.legend(loc='upper right')
plt.show()


fig, dx = plt.subplots()
dx.set_title('SARS Death Rates - ' + Pais_sars)
dx.set_ylabel('Rate (%)')
dx.plot(df_b.index, df_b['Death Rate']*100, marker='o', markerfacecolor = 'white',markersize=4,linestyle='-')
#dx.plot(df_b.index, df_b['Recover Rate']*100, marker='o', markerfacecolor = 'white',markersize=4,linestyle='-')
dx.legend(loc='upper right')
plt.show()
    
