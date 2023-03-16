#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


# importing data
df = pd.read_csv("bristol-air-quality-data.csv", delimiter=";")
print(len(df))


# In[3]:


# formating Date time column

datetime_format = '%Y-%m-%dT%H:%M:%S%z'
start_date = pd.to_datetime('2010-01-01T00:00:00+00:00',format=datetime_format)
df['Date Time'] = pd.to_datetime(df['Date Time'], format=datetime_format)

# delete any records before 00:00 1 Jan 2010 
df=df.loc[df['Date Time'] >= start_date]
print(len(df))


# In[4]:


# exporting the csv file
df.to_csv('crop.csv',index=False, encoding="utf-8")

