# Task 5

NoSQL database is a non-relational Data Management System, it is non-tabular, and store data differently than relational tables. Moreover, it does not require fixed schema, avoids joins and is easy to scale due to its horizontal scaling. <br>
Although NoSQL databases does not require a fixed schema, it is important to model data correctly to improve performance.  Modelling and organizing the data for a given workload can result in significant performance improvements. <br>
Thus, In order to meet the specifications of the task on my hand, I will start by modelling the data, then I will implement the database on MongoDB, which is a document-based database, then finally I will import the data to the database. <br>
To model our data, we need first to establish the project requirements, and work on the specific objectives of the UK Government to protect our health. Then, we need define the structure of the data, which comes to enumerate data items and attributes, and finally state the relationship between the items. <br>
From the data we have, I opted for selecting three data items, which are readings ( attributes: 'Date Time', 'NOx', 'NO2', 'NO', 'PM10', 'NVPM10', 'VPM10','NVPM2.5', 'PM2.5', 'VPM2.5', 'CO', 'O3', 'SO2', 'Temperature', 'RH','Air Pressure', 'DateStart', 'DateEnd', 'Current', 'Instrument Type', 'Station'), stations ( attributes: 'SiteID', 'Location', 'geo_point_2d') and schema ( attributes: 'measures', 'description', 'units'). However, we have a nested relationship between readings and stations; every reading is taken from a specific station.  Therefore, this results to an embedded data model. <br>
As the task specifications required, we will be working on a specific monitor. Therefore, I chose ‘Old Market’ station to implement. <br>
In order to implement the data model explained above and import the data to MongoDB database, I wrote the following python code:




```python
import pymongo
import pandas as pd
import json
import datetime
```

Importing the cleaned data


```python
df = pd.read_csv("clean.csv")
```

    C:\Users\driss\anaconda3\lib\site-packages\IPython\core\interactiveshell.py:3165: DtypeWarning: Columns (20) have mixed types.Specify dtype option on import or set low_memory=False.
      has_raised = await self.run_ast_nodes(code_ast.body, cell_name,
    

Selecting the 'Old Market' station


```python
df = df[df['SiteID']==213]
```

Affecting the columns to the data items


```python
df_readings = df[['Date Time', 'NOx', 'NO2', 'NO', 'PM10', 'NVPM10', 'VPM10',
       'NVPM2.5', 'PM2.5', 'VPM2.5', 'CO', 'O3', 'SO2', 'Temperature', 'RH',
       'Air Pressure', 'DateStart', 'DateEnd', 'Current', 'Instrument Type']]
df_stations = df[['SiteID', 'Location', 'geo_point_2d']]
df_stations = df_stations.drop_duplicates(ignore_index=True)
```

Creating schema DataFrame


```python
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

df_schema = pd.DataFrame(measures,columns=['measures'])
df_schema['descriptions'] = descriptions
df_schema['units'] = units
```

Connecting to the MongoClient on the localhost: 27017


```python
client = pymongo.MongoClient("mongodb://localhost:27017")
```

Transforming the dataframes to dictionaries 


```python
df_readings_dict = df_readings.to_dict(orient = "records")
df_stations_dict = df_stations.to_dict(orient = "records")
for reading in df_readings_dict:
    reading["station"] = df_stations_dict[0]
df_schema_dict = df_schema.to_dict(orient = "records")
```

Creating a database named 'pollution_db3'


```python
db = client["pollution_db3"]
```

Creating the collections then inserting the documents


```python
db.readings.insert_many(df_readings_dict)
db.schema.insert_many(df_schema_dict)
```




    <pymongo.results.InsertManyResult at 0x28241877790>



An exemple of the documents in the readings collection is: <br>
{  "_id": {    "$oid": "62c513caabfc15f5dd7c2ed7"  },  "Date Time": "2010-06-27 15:00:00+00:00",  "NOx": 101,  "NO2": 36,  "NO": 43,  "PM10": 22.7,  "NVPM10": null,  "VPM10": null,  "NVPM2.5": null,  "PM2.5": null,  "VPM2.5": null,  "CO": 0.7,  "O3": null,  "SO2": null,  "Temperature": null,  "RH": null,  "Air Pressure": null,  "DateStart": null,  "DateEnd": null,  "Current": false,  "Instrument Type": "Continuous (Reference)",  "station": {    "SiteID": 213,    "Location": "Old Market",    "geo_point_2d": "51.4560189999,-2.58348949026"  }}

# Query example
when executing the following query which is supposed to return documents with moderate and high levels of NO2: <br>
db.readings.find( {NO2: {$gt: 200}} ) <br>
we get the following 3 documents which has NO2 greater than 200: 

{
  "_id": {
    "$oid": "62c50b299e348bd2995b494b"
  },
  "Date Time": "2010-12-09 09:00:00+00:00",
  "NOx": 1645,
  "NO2": 288,
  "NO": 888,
  "PM10": 59.1,
  "NVPM10": null,
  "VPM10": null,
  "CO": 2.9,
  "O3": null,
  "SO2": null,
  "Temperature": null,
  "RH": null,
  "Air Pressure": null,
  "DateStart": null,
  "DateEnd": null,
  "Current": false,
  "Instrument Type": "Continuous (Reference)",
  "station": {
    "SiteID": 213,
    "Location": "Old Market",
    "geo_point_2d": "51.4560189999,-2.58348949026"
  }
},

{
  "_id": {
    "$oid": "62c50b299e348bd2995b53f6"
  },
  "Date Time": "2010-11-26 09:00:00+00:00",
  "NOx": 1173,
  "NO2": 216,
  "NO": 626,
  "PM10": null,
  "NVPM10": null,
  "VPM10": null,
  "CO": 2.1,
  "O3": null,
  "SO2": null,
  "Temperature": null,
  "RH": null,
  "Air Pressure": null,
  "DateStart": null,
  "DateEnd": null,
  "Current": false,
  "Instrument Type": "Continuous (Reference)",
  "station": {
    "SiteID": 213,
    "Location": "Old Market",
    "geo_point_2d": "51.4560189999,-2.58348949026"
  }
},

{
  "_id": {
    "$oid": "62c50b299e348bd2995b5e90"
  },
  "Date Time": "2010-12-09 08:00:00+00:00",
  "NOx": 1234,
  "NO2": 222,
  "NO": 663,
  "PM10": 38,
  "NVPM10": null,
  "VPM10": null,
  "CO": 2.1,
  "O3": null,
  "SO2": null,
  "Temperature": null,
  "RH": null,
  "Air Pressure": null,
  "DateStart": null,
  "DateEnd": null,
  "Current": false,
  "Instrument Type": "Continuous (Reference)",
  "station": {
    "SiteID": 213,
    "Location": "Old Market",
    "geo_point_2d": "51.4560189999,-2.58348949026"
  }
})
