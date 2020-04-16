# -*- coding: UTF-8 -*-
import os
import csv
import datetime
from collections import defaultdict

def csv_to_dicts(csv_name):
    with open(os.path.join("raw", "{}.csv".format(csv_name))) as csv_file:
        d_reader = csv.DictReader(csv_file)
        return list(d_reader)

cc_dict = {}
for r in csv_to_dicts("country_code"):
    cc_dict[r['name']] = r['code']

march_dict = defaultdict(dict)
confirmed_recovered_death = defaultdict(dict)

for r in csv_to_dicts("DATASET-1"):
    d = datetime.datetime.strptime(r['Date'], '%Y-%m-%d')
    if d.month == 3:
        march_dict[d.day][r['Country']] = int(r['Confirmed'])
        confirmed_recovered_death[d.day][r['Country']] = ( int(r['Confirmed']) , int(r['Recovered']), int(r['Deaths']) )
    if d.month == 2:
        if d.day == 29:
            confirmed_recovered_death[0][r['Country']] = ( int(r['Confirmed']) , int(r['Recovered']), int(r['Deaths']) )

highest_increase = []
increase_list = []

q2 = []

for dd in list(march_dict.keys()):

    if dd == 0:
        continue
    
    highest_num = 0
    highest_c = None
    total_confirmed = 0
    total_recovered = 0
    total_death = 0
    for cc in march_dict[dd].keys():

        if cc == "Diamond Princess":
            continue

        if cc in march_dict[dd-1]:
            increase = march_dict[dd][cc] - march_dict[dd-1][cc]
        else:
            increase = march_dict[dd][cc]
        increase_list.append((increase, cc, dd))
        if increase > highest_num:
            highest_num = increase
            highest_c = cc
        confirmed, recovered, deaths = confirmed_recovered_death[dd][cc]
        total_confirmed += confirmed
        total_recovered += recovered
        total_death += deaths
    
    q2.append({
        'group': dd,
        'male': total_recovered,
        'female': total_confirmed,
        'female_deaths': total_death,
        'male_deaths': 0,
    })
    print(highest_c, confirmed_recovered_death[dd][highest_c])

    highest_increase.append((highest_num, highest_c, dd))

#print(march_dict)
top_20 = {}
for nn, cc, dd in reversed(sorted(increase_list)):
    if len(top_20.keys()) >= 20:
        break
    if cc in top_20:
        continue
    top_20[cc] = (nn, dd)

headers = ["country", "code", "pop"]
translate = {
    'Mainland China': 'China',
    'Hong Kong': 'Hong Kong, China',
    'Macau': 'Macau, China',
    'US': 'United States',
    'USA': 'United States',
    'UK': 'United Kingdom',
    'Russia': 'Russian Federation',
    'Iran (Islamic Republic of)': 'Iran',
    'Republic of Korea': 'South Korea',
    'Korea, South': 'South Korea',
    'Hong Kong SAR': 'Hong Kong, China',
    'Macao SAR': 'Macau, China',
    'Taipei and environs': 'Taiwan',
    'Viet Nam': 'Vietnam',
    'occupied Palestinian territory': 'Israel',
    'Republic of Moldova': 'Moldova',
    'Saint Martin': 'St. Martin',
    'Channel Islands': 'Bailiwick of Guernsey',
    'Holy See': 'Vatican City'
}
print(cc_dict)
q1 = defaultdict(dict)

for k,v in top_20.items():
    k = translate[k] if k in translate else k
    q1[cc_dict[k]]['pop'] = v[0]
    q1[cc_dict[k]]['country'] = k

with open('q1.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=headers)
    writer.writeheader()
        
    for k, v in q1.items():
        d = {
            'code':k,
            **v
        }
        writer.writerow(d)

# Male is recovered

with open('q2.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=["group", 'male', 'female', 'male_deaths', 'female_deaths'])
    writer.writeheader()

    for d in q2:
        writer.writerow(d)