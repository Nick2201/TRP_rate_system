#!/usr/bin/env python
# coding: utf-8

# # All PREPARE

# ## IMPORT Data and libraries

# In[16]:


import pandas as pd 
import numpy as np
from pathlib import Path
import openpyxl
import seaborn as sns


# In[2]:


docs_folder = Path(Path.cwd()/'docs')
data_upload = Path(docs_folder/ 'Выгрузка.xlsx')
data_plan = Path(docs_folder/ 'План.xlsx')
df_upload_raw = pd.read_excel(data_upload)


# ## PREPARE DATA 1 df_upload

# In[3]:


df_upload_raw = pd.read_excel(data_upload,date_format=['Дата'])
df_upload_raw['Время начала (5-29)'] = pd.to_datetime(df_upload_raw['Время начала (5-29)'], format="%H:%M:%S").dt.time
df_upload_raw = df_upload_raw.rename(columns={
    'Ролик ID выхода'               :'ID_release',
    'Дата'                          :'date',
    'Время начала (5-29)'           :'time_begin',
    'Блок Распространение'          :'distribution_ch',
    'Ролик Тип'                     :'promo_video',
    "Ролик Ожидаемая длительность"  :'promo_video_duration',
    'Ролик Тип позиции в блоке'     :'promo_video_position',
    "Ролик ID"                      :'promo_video_ID',
    'Телекомпания'                  :'telecomp',
    "TVR All 25-55"                 :'TVR'

})
df_upload_raw[['promo_video_duration','TVR']] = df_upload_raw[['promo_video_duration','TVR']].apply(pd.to_numeric)
df_upload_raw['month'] = df_upload_raw.date.dt.month
# df_upload_raw.distribution_ch.value_counts()



# ## PREPARE DATA 2 data_plan

# In[4]:


df_data_plan = pd.read_excel(data_plan)


# In[5]:


def mapping_df(df_input):
    b_ind = df_data_plan.columns.get_loc('Бюджет')
    trp_ind = df_data_plan.columns.get_loc('TRP')-1

    bud = ['Бюджет' for i in range(trp_ind-b_ind+1)]
    trp = ['TRP' for i in range(trp_ind-b_ind+1)]
    df_data_plan.columns = df_data_plan.iloc[0,:]
    df_data_plan.drop(0,inplace=True)
    der = df_data_plan.T

    df_data_plan.index=df_data_plan.Телеканал
    new = df_data_plan.drop(columns='Телеканал').T
    # new['type'] = bud+trp

    new_1 = new.rename(columns={0:"month"})
    new_1 = new_1.apply(pd.to_numeric)
   
    df_plan, df_result = np.split(new_1, 2)
    return df_plan.T,df_result.T


# In[6]:


# Split by Two DF: budjet and trp
df_budget,df_trp_raw= mapping_df(df_data_plan)


# In[7]:


df_trp = df_trp_raw
df_trp.rename(columns={'Телеканал':'telecomp'})

month_rus   = ['Январь'	,'Февраль',	'Март','Апрель','Май','Июнь','Июль','Август','Сентябрь','Октябрь','Ноябрь','Декабрь']
month_numb  = list(range(1,13))

df_trp = df_trp.rename(columns=dict(zip(month_rus,month_numb))).reset_index()


# In[8]:


# Группировка
df_group_upload= (
    df_upload_raw[['telecomp','TVR','month']]
    .groupby(['telecomp','month'])
    .agg(sum).reset_index()
    )
df_group_upload.head(7)


# In[9]:


# Preparing
melted_df1 = pd.melt(df_trp, id_vars='Телеканал', var_name='month', value_name='plan')


melted_df1.rename(columns={'Телеканал': 'telecomp'}, inplace=True)
melted_df1['telecomp'] = melted_df1['telecomp'].str.upper()

melted_df1 = melted_df1.query('month !="Все месяцы"')


# # Аналитика

# ## Tasks 1
#  - [x] Задача: понять, выполняется ли в каждой кампании плановый объём TRP
#     - general_rating рейтинг = 6
#  - [x] Задача: по всем кампаниям
#     - rating_each_company
#     - rating_analog
#     - [x] каналов дистрибъюции 1 == Сетевой : 3966
#       - df_upload_raw.distribution_ch.value_counts()

# In[10]:


def calculate_rating(deviation):
    if deviation > 5:
        rating = 10
    elif deviation == 0:
        rating = 8
    else:
        rating = 1 + (deviation / 5) * 7 
    return round(rating,2)


# In[62]:


def make_compare_df(group_by_value):
    df_compare=(
        pd.merge(melted_df1,df_group_upload,on=['telecomp','month'])
        .groupby(group_by_value).agg(
            plan=('plan','sum'),
            fact=('TVR','sum')).reset_index()
        )
    df_compare[['fact','plan']] = df_compare[['fact','plan']].apply(pd.to_numeric)
    df_compare['TVR_deviation'] = (df_compare['fact'] - df_compare['plan']) / df_compare['plan'] * 100


    return df_compare

df_compare = make_compare_df(['month'])

df_compare['rating_'] = df_compare['TVR_deviation'].apply(calculate_rating)

df_compare= df_compare.rename(columns={'month':"company"})
group_by_company = df_compare[['company','rating_']]
sns.barplot(data=group_by_company,x='company',y='rating_')
group_by_company


# In[63]:


by_company= make_compare_df(group_by_value=["month",'telecomp',])[['month',"TVR_deviation",'telecomp',]]
by_company['rating_'] = by_company['TVR_deviation'].apply(calculate_rating)

by_company = by_company.rename(columns={"month":"company"})
by_company.sort_values(by='company',ascending=True)
by_company
sns.barplot(data=by_company,x='company',y='rating_',hue="telecomp")
# by_company


# In[138]:


totals = df_compare.sum(numeric_only=True)

totals['telecomp'] = 'Итого'
df_compare = pd.concat([df_compare, pd.DataFrame(totals).T], ignore_index=True)    


df_compare[['fact','plan']] = df_compare[['fact','plan']].apply(pd.to_numeric)
df_compare['TVR_deviation'] = (df_compare['fact'] - df_compare['plan']) / df_compare['plan'] * 100
df_compare

categories = [-float('inf'),-10,-5,0,5,10, float('inf')]
ratings = [0, 2, 4, 6, 8,10]

df_compare = df_compare[['telecomp','plan','fact','TVR_deviation']]

df_compare['client_rating'] = pd.cut(df_compare['TVR_deviation'], bins=categories, labels=ratings)

customer_rating = df_compare[['telecomp','client_rating']].rename(columns={'TVR_deviation':'customer_rating'})
general_rating = customer_rating.iloc[-1,:]

general_rating


# In[139]:


import matplotlib.pyplot as plt
import seaborn as sns


# ## Графики 
# 

# In[45]:


# telecomp	month	
df_compare_comp=(
    pd.merge(melted_df1,df_group_upload,on=['telecomp','month'])
    .groupby(['telecomp','month']).agg(
        plan=('plan','sum'),
        fact=('TVR','sum')).reset_index()
    )

df_compare_comp[['fact','plan']] = df_compare_comp[['fact','plan']].apply(pd.to_numeric)
df_compare_comp['TVR_deviation'] = (df_compare_comp['fact'] - df_compare_comp['plan']) / df_compare_comp['plan'] * 100
df = df_compare_comp[['telecomp','TVR_deviation','month','fact']]
df = df.rename(columns={"month":"company"})
sns.lineplot(data=df.sort_values(by='company'),x='company',y='TVR_deviation',hue='telecomp')

# telecomp	month	
df_compare_comp=(
    pd.merge(melted_df1,df_group_upload,on=['telecomp','month'])
    .groupby(['telecomp','month']).agg(
        plan=('plan','sum'),
        fact=('TVR','sum')).reset_index()
    )

df_compare_comp[['fact','plan']] = df_compare_comp[['fact','plan']].apply(pd.to_numeric)
df_compare_comp['TVR_deviation'] = (df_compare_comp['fact'] - df_compare_comp['plan']) / df_compare_comp['plan'] * 100
df = df_compare_comp[['telecomp','TVR_deviation','month','fact']]
df = df.rename(columns={"month":"company"})
sns.lineplot(data=df.sort_values(by='company'),x='company',y='TVR_deviation',hue='telecomp')


# In[141]:


df.groupby('telecomp',as_index=False).agg(audience=("fact",'sum'))

sns.barplot(
    data=df.groupby('telecomp',as_index=False)
        .agg(audience=("fact",'sum'))
        .sort_values(by="audience"),
    y="audience",
    x="telecomp",
    )


# # Рейтинг компаний друг относительно друга
# ## 1. quantile

# In[15]:


# by every month quanilte
df = df_compare
q10 = df['TVR_deviation'].quantile(0.1)
q90 = df['TVR_deviation'].quantile(0.9)

df['rating_by_distribute'] = np.where(df['TVR_deviation'] < q10, 0, np.where(df['TVR_deviation'] > q90, 10, ((df['TVR_deviation'] - q10) / (q90 - q10)) * 10))

# Rounding ratings to nearest integer
df['rating_by_distribute'] = df['rating_by_distribute'].round().astype(int)
rating_analog = df[['telecomp',"TVR_deviation","client_rating",'rating_by_distribute']]
rating_analog


# # Plotly

# In[ ]:


import plotly
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots

