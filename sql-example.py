# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 14:48:03 2019

@author: NATE
This program uses the outline given on https://www.dataquest.io/blog/sql-basics/
to test sql commands in python, and adds other general sql statments not provided,
such as determining the average trip length for ages over/under 30 in a single
command. The database concerns hubway bicycle trips in the Boston area in 2017.
"""

import sqlite3 as sql
import pandas as pd

pd.set_option("display.max_columns", 10)
db = sql.connect("hubway.db")
def run_query(query):
    return(pd.read_sql_query(query,db))
    
#THESE QUERIES ARE JUST LOOKING AT THE TRIP TABLE 
 
#calculates average trip length by registration 
avg_trip_rc = run_query("select sub_type, avg(duration) as 'Average Duration by Registration' from trips \
              group by sub_type;")

print(avg_trip_rc)
 
#Separates average trip length by gender   
avg_trip_fm = run_query("select gender, avg(duration) as 'Average Duration by Gender' from trips \
               where gender<> 'Female\n' and sub_type = 'Registered' group by gender;")


print(avg_trip_fm)

#Separates average trip length by age
young_trip = run_query("select case \
                           when (2017 -birth_date)<30 \
                               Then 'under 30' \
                           else 'over 30' end \
                           as 'Age',\
                       avg(duration) as 'Avg Trip Length' from \
                       trips group by case \
                       when (2017 -birth_date)<30 \
                       Then 'under 30' \
                       else 'over 30' end")

print(young_trip)

#THESE QUERIES LOOK AT BOTH THE STATIONS AND TRIPS TABLES

#counts trips that start and end at the same place
round_trip = run_query("select stations.station as 'Station', count(*) as 'Round Trips' \
              From trips inner join stations \
              on trips.start_station = stations.id \
              where trips.start_station = trips.end_station\
              group by stations.station order by count(*) desc limit 5 ")

print(round_trip)

#round trips for Registered vs Casual users
round_trip_rc = run_query("select sub_type as 'Reg/Casual', count(*) as 'Round Trips' \
              From stations inner join trips \
              on trips.start_station = stations.id \
              where trips.start_station = trips.end_station\
              group by sub_type")

print(round_trip_rc)


#counts how many trips cross municipalities
cross_mun = run_query("select count(trips.id) as 'Cross Mun Count' \
              from trips inner join stations as start \
              on trips.start_station = start.id \
              inner join stations as end\
              on trips.end_station = end.id\
              where start.municipality <> end.municipality")

print(cross_mun)





db.close()
