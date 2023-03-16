#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys
import pandas as pd
import mysql.connector as mariadb
import datetime
# import data
df=pd.read_csv('clean.csv')


# In[2]:


# filling NaN values with NULL

df = df.fillna("NULL")


# In[3]:


begin_time = datetime.datetime.now()
try:
    # set the user and passoword
    # connect to mariaDB platform
    conn = mariadb.connect(
        user="root",
        password="sql123456",
        host="127.0.0.1",     
        port=3306,            
    )
    # make and get the cursor
    cur = conn.cursor()
    
    cur.execute("DROP SCHEMA IF EXISTS pollution_db2")
    cur.execute("CREATE SCHEMA IF NOT EXISTS `pollution_db2` DEFAULT CHARACTER SET utf8")
    cur.execute("USE `pollution_db2`")

    # Creating tables
    stations_sql=cur.execute('''
        CREATE TABLE IF NOT EXISTS `pollution_db2`.`stations` (
            `idstations` INT NOT NULL,
            `location` VARCHAR(48) NULL DEFAULT NULL,
            `geo_point_2d` VARCHAR(32) NULL DEFAULT NULL,
            PRIMARY KEY (`idstations`))
        ENGINE = InnoDB
        DEFAULT CHARACTER SET = utf8mb3;
         ''')
         
    schema_sql=cur.execute ('''
        CREATE TABLE IF NOT EXISTS `pollution_db2`.`schema` (
          `measure` VARCHAR(32) NOT NULL,
          `description` LONGTEXT NULL DEFAULT NULL,
          `unit` VARCHAR(24) NULL DEFAULT NULL,
          PRIMARY KEY (`measure`))
        ENGINE = InnoDB
        DEFAULT CHARACTER SET = utf8mb3;
         ''')
 
    readings_sql=cur.execute('''
        CREATE TABLE IF NOT EXISTS `pollution_db2`.`readings` (
          `idreadings` INT NOT NULL AUTO_INCREMENT,
          `datetime` DATETIME NULL DEFAULT NULL,
          `nox` FLOAT NULL DEFAULT NULL,
          `no2` FLOAT NULL DEFAULT NULL,
          `no` FLOAT NULL DEFAULT NULL,
          `pm10` FLOAT NULL DEFAULT NULL,
          `nvpm10` FLOAT NULL DEFAULT NULL,
          `vpm10` FLOAT NULL DEFAULT NULL,
          `nvpm2.5` FLOAT NULL DEFAULT NULL,
          `pm2.5` FLOAT NULL DEFAULT NULL,
          `vpm2.5` FLOAT NULL DEFAULT NULL,
          `co` FLOAT NULL DEFAULT NULL,
          `o3` FLOAT NULL DEFAULT NULL,
          `so2` FLOAT NULL DEFAULT NULL,
          `temperature` DOUBLE NULL DEFAULT NULL,
          `rh` INT NULL DEFAULT NULL,
          `airpressure` INT NULL DEFAULT NULL,
          `datestart` DATETIME NULL DEFAULT NULL,
          `dateend` DATETIME NULL DEFAULT NULL,
          `current` TEXT NULL DEFAULT NULL,
          `instrumenttype` VARCHAR(32) NULL DEFAULT NULL,
          `stationid` INT NOT NULL,
          PRIMARY KEY (`idreadings`),
          INDEX `stationid_idx` (`stationid` ASC) VISIBLE,
          CONSTRAINT `stationid`
            FOREIGN KEY (`stationid`)
            REFERENCES `pollution_db2`.`stations` (`idstations`)
            ON DELETE NO ACTION
            ON UPDATE NO ACTION)
        ENGINE = InnoDB
        DEFAULT CHARACTER SET = utf8mb3;
        ''')   
    
    
    # Creating the inserts to the schema table
    measures = ["Date Time", "NOx", "NO2", "NO", "SiteID", "PM10", 
            "NVPM10", "VPM10", "NVPM2.5","PM2.5", "VPM2.5", "CO", 
            "O3", "S02", "Temperature", "RH", "Air Pressure", 
            "Location", "geo_point_2d", "DateStart", "DateEnd",
            "Current", "Instrument Type"]
           
            
    descriptions = ["Date and time of measurement", "Concentration of oxides of nitrogen",
             "Concentration of nitrogen dioxide","Concentration of nitric oxide",
             "Site ID for the station","Concentration of particulate matter <10 micron diameter",
             "Concentration of non - volatile particulate matter <10 micron diameter","Concentration of volatile particulate matter <10 micron diameter",
             "Concentration of non volatile particulate matter <2.5 micron diameter","Concentration of particulate matter <2.5 micron diameter",
             "Concentration of volatile particulate matter <2.5 micron diameter","Concentration of carbon monoxide",
             "Concentration of ozone","Concentration of sulphur dioxide",
             "Air temperature","Relative Humidity","Air Pressure","Text description of location",
             "Latitude and longitude","The date monitoring started",
             "The date monitoring ended","Is the monitor currently operating","Classification of the instrument"]

     
    units = ["datetime", "ug/m3", "ug/m3","ug/m3","integer","ug/m3",
         "ug/m3","ug/m3","ug/m3","ug/m3","ug/m3", "mg/m3", "ug/m3",
         "ug/m3", "°C", "%", "mbar", "text","geo point",
         "datetime", "datetime", "text", "text"]
         
    
    # Insert quotes
    insert_schema_sql="""INSERT IGNORE INTO `schema` values (%s, %s, %s)"""
    insert_stations_sql="""INSERT IGNORE INTO `stations` values (%s,%s,%s)"""
    insert_readings_sql="""INSERT IGNORE INTO `readings` (`datetime`, `nox`, `no2`, `no`, `pm10`, 
   `nvpm10`, `vpm10`, `nvpm2.5`,`pm2.5`, `vpm2.5`, `co`, 
   `o3`, `so2`, `temperature`, `rh`, `airpressure`, `datestart`, 
   `dateend`, `current`, `instrumenttype`, `stationid`) 
   values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
   
    schema_vals = []
    station_records = []
    reading_records = []
    
    # Inserting the values
    for measure, description, unit in zip(measures, descriptions, units):
        schema_vals.append((measure, description, unit))

    for i,row in df.iterrows(): 
        station_records.append((row['SiteID'], row['Location'], row['geo_point_2d']))
        reading_records.append((row['Date Time'],row['NOx'],row['NO2'],row['NO'],row['PM10'],row['NVPM10'],
            row['VPM10'],row['NVPM2.5'],row['PM2.5'],row['VPM2.5'],row['CO'],row['O3'],
            row['SO2'],row['Temperature'],row['RH'],row['Air Pressure'],row['DateStart'],
            row['DateEnd'],row['Current'],row['Instrument Type'],row['SiteID']))
        
    cur.executemany(insert_schema_sql, schema_vals)
    cur.executemany(insert_stations_sql, station_records)
    cur.executemany(insert_readings_sql, reading_records)

    conn.commit()  
    conn.close()
except BaseException as err:
    print(f"An error occured: {err}")
    sys.exit(1)


# In[ ]:




