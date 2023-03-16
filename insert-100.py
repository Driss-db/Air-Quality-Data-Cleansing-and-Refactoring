#!/usr/bin/env python
# coding: utf-8

# In[1]:


import csv
import itertools
from datetime import datetime
import sys
# initialize the sql file
sql_file = "INSERT INTO `readings` VALUES\n"
cnt = 1
with open("clean.csv","r") as file:
    for row in itertools.islice(csv.DictReader(file),100):
        # deleting location and geo_point_2d
        del row['Location']
        del row['geo_point_2d']
        
        # formatting the dates
        dt = datetime.fromisoformat(row['Date Time'][:-6])
        dt.strftime('%Y-%m-%d %H:%M:%S')
        row['Date Time'] = dt
        
        ds = datetime.fromisoformat(row['DateStart'][:-6])
        ds.strftime('%Y-%m-%d %H:%M:%S')
        row['DateStart'] = ds
        
        if row['DateEnd']:
            de = datetime.fromisoformat(row['DateEnd'][:-6])
            de.strftime('%Y-%m-%d %H:%M:%S')
            row['DateEnd'] = de

        # inserting the records
        readings = ["'"+str(val)+"'" for val in row.values()]
        sql_readings = ",".join(readings)
        sql_readings = sql_readings.replace("''","NULL")
        sql_readings = sql_readings.replace("'False'","False")
        sql_readings = sql_readings.replace("'True'","True")
        sql_file = sql_file + "(" + str(cnt) + "," + sql_readings + ")," + "\n"
        cnt += 1

# writing the the string into the sql file
sql_file=sql_file[:-2]+';'
file=open("insert-100.sql","w")
file.write(sql_file + "\n")


# In[ ]:




