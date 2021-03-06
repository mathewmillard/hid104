#Step 1: Import modules (some of visualizations will use custom imports later)
import requests, json, csv
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from math import pi
from timeit import default_timer as timer



#Step 2: Read Data from CSV and group into races
file = open("projectdata.csv", "r")
name_csv = csv.DictReader(file)

name_lst = [] #This list will be used later

name_race = {'pctwhite':'', 'pctblack':'', 'pctapi':'', 'pcthispanic':''}

for index, row in enumerate(name_csv):
    if index >= 500:
        break
    name_lst.append(row['name'])
    if max(row['pctwhite'], row['pctblack'], row['pctapi'], row['pctaian'], row['pct2prace'], row['pcthispanic']) == row['pctwhite']:
        name_race['pctwhite']+=row['name']
        name_race['pctwhite']+= ' '
    elif max(row['pctwhite'], row['pctblack'], row['pctapi'], row['pctaian'], row['pct2prace'], row['pcthispanic']) == row['pctblack']:
        name_race['pctblack']+=row['name']
        name_race['pctblack']+= ' '
    elif max(row['pctwhite'], row['pctblack'], row['pctapi'], row['pctaian'], row['pct2prace'], row['pcthispanic']) == row['pctapi']:
        name_race['pctapi']+=row['name']
        name_race['pctapi']+= ' '
    elif max(row['pctwhite'], row['pctblack'], row['pctapi'], row['pctaian'], row['pct2prace'], row['pcthispanic']) == row['pcthispanic']:
        name_race['pcthispanic']+=row['name']
        name_race['pcthispanic']+= ' '

file.close()

names = {k: v + 1 for v, k in enumerate(name_lst)}

name_race['pctwhite'] = name_race['pctwhite'].split()
name_race['pctblack'] = name_race['pctblack'].split()
name_race['pctapi'] = name_race['pctapi'].split()
name_race['pcthispanic'] = name_race['pcthispanic'].split()

name_counts = [len(name_race['pctwhite']), len(name_race['pctblack']), len(name_race['pctapi']), len(name_race['pcthispanic'])]

#Step 3: Define function to capture search suggetion results

#Define user agent set to Mozilla Firefox
headers = {'User-agent':'Mozilla/5.0'}

#Create a function to literate through names and capture search results
def suggestion_master(results, dictionary, search, target, target2 = None):
    for name in names.keys():
        URL="http://suggestqueries.google.com/complete/search?client=firefox&q=" + name + " " + target
        response = requests.get(URL, headers=headers)
        results.append(json.loads(response.content.decode('utf-8')))    #captures search results and appends to a list
    for result in results:  #iterates through search results for every name
        name = result[0].split()
        for suggestion in result[1]:
            if target or target2 in suggestion:
                dictionary[name[0]] += 1

#Step 4 Run the test for search result case

#Tracks how long it takes to run the functions
start = timer()

#4a
arrest_results = []
arrest_dict = {k: v*0 for v, k in enumerate(name_lst)}
suggestion_master(arrest_results, arrest_dict, "arre", "arrest")

#4b
murder_results = []
murder_dict = {k: v*0 for v, k in enumerate(name_lst)}
suggestion_master(murder_results, murder_dict, "murd", "murder")

#4c
homicide_results = []
homicide_dict = {k: v*0 for v, k in enumerate(name_lst)}
suggestion_master(homicide_results, homicide_dict, "homi", "homicide")

#4d
crime_results = []
crime_dict = {k: v*0 for v, k in enumerate(name_lst)}
suggestion_master(crime_results, crime_dict, "crim", "crime", "criminal")

#4e
prison_results = []
prison_dict = {k: v*0 for v, k in enumerate(name_lst)}
suggestion_master(prison_results, prison_dict, "pris", "prison")

#Tracks how long it takes to run the functions
end = timer()
query_time = (end - start)

#Step 5 Summarise data results

avg_data = [arrest_dict, murder_dict, homicide_dict, crime_dict, prison_dict]

#5a Calculate search data results by race/ethnicity category

pctwhite_stats = {'arrest':0, 'murder':0, 'homicide':0,'crime':0,'prison':0}

pctblack_stats = {'arrest':0, 'murder':0, 'homicide':0,'crime':0,'prison':0}

pctapi_stats = {'arrest':0, 'murder':0, 'homicide':0,'crime':0,'prison':0}

pcthispanic_stats = {'arrest':0, 'murder':0, 'homicide':0,'crime':0,'prison':0}

term_lst = ['arrest','murder','homicide','crime','prison']

#Define a function to calculate results for every race/ethnicity and for every search criterion
def stat_stuffer(race_name, pct_stats, avg_dict):
    for i in range(0, len(avg_dict)):
        for datum in avg_dict[i]:
            for name in name_race[race_name]:
                if datum == name:
                    pct_stats[term_lst[i]]+=avg_dict[i][datum]


#Run the function for every race/ethnicity
stat_stuffer('pctwhite', pctwhite_stats, avg_data)

stat_stuffer('pctblack', pctblack_stats, avg_data)

stat_stuffer('pctapi', pctapi_stats, avg_data)

stat_stuffer('pcthispanic', pcthispanic_stats, avg_data)


#5b Average all the results

#One dictionary stores just raw data which will be used later in the box plots
name_race_raw = {'pctwhite':[], 'pctblack':[], 'pctapi':[], 'pcthispanic':[]}
name_race_avg = {'pctwhite':0, 'pctblack':0, 'pctapi':0, 'pcthispanic':0}

for race_name in name_race:
    for data in avg_data:
        for datum in data:
                for name in name_race[race_name]:
                    if datum == name:
                        name_race_raw[race_name].append(data[datum])
                        name_race_avg[race_name]+=data[datum]

#Calculate average aggregate associations for every race/ethnicity
for race_avg in name_race_avg:
    name_race_avg[race_avg] = name_race_avg[race_avg] / (len(name_race[race_avg])*len(avg_data))

#Calculate average associations for every race/ethnicity by search criteria
for stat in pctwhite_stats:
    pctwhite_stats[stat] = pctwhite_stats[stat] / len(name_race['pctwhite'])

for stat in pctblack_stats:
    pctblack_stats[stat] = pctblack_stats[stat] / len(name_race['pctblack'])

for stat in pctapi_stats:
    pctapi_stats[stat] = pctapi_stats[stat] / len(name_race['pctapi'])

for stat in pcthispanic_stats:
    pcthispanic_stats[stat] = pcthispanic_stats[stat] / len(name_race['pcthispanic'])
