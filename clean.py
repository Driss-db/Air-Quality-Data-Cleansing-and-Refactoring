#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
# import data

df = pd.read_csv('crop.csv')


# In[2]:


# drop missing values in SiteID column
df=df.dropna(subset=['SiteID'])


# In[3]:


# creating a dictionary between siteID and location

Station_dict={'188' : 'AURN Bristol Centre',
'203' : 'Brislington Depot',
'206' : 'Rupert Street',
'209' : 'IKEA M32',
'213' : 'Old Market',
'215' : 'Parson Street School',
'228' : 'Temple Meads Station',
'270' : 'Wells Road',
'271' : 'Trailer Portway P&R',
'375' : 'Newfoundland Road Police Station',
'395' : "Shiner's Garage",
'452' : 'AURN St Pauls',
'447' : 'Bath Road',
'459' : 'Cheltenham Road \ Station Road',
'463' : 'Fishponds Road',
'481' : 'CREATE Centre Roof',
'500' : 'Temple Way',
'501' : 'Colston Avenue'}


# In[4]:


# defining a function that returns the mismatched lines

def mismatched_lines(data):
    mismatched_lines=[]
    for i in range (0,len(data)):
        if str(data.SiteID[i]) not in Station_dict.keys():
            mismatched_lines.append(i)
        elif Station_dict[str(data.SiteID[i])] != data.Location[i]:
            mismatched_lines.append(i)
            #print("The line number is %s and the SiteID is %s and the Location is %s",(i,data.SiteID[i],data.Location[i]))
    return mismatched_lines


# In[5]:


# printing the mismatche rows

mismatch = mismatched_lines(df)
for ind in mismatch:
    print("The line number is %s and the SiteID is %s and the Location is %s" % (ind,df.SiteID[ind],df.Location[ind]))


# In[6]:


# drop the mismached rows

df.drop(index=mismatch, inplace = True)


# In[7]:


# exporting the csv file

df.to_csv("clean.csv",index=False, encoding="utf-8")

