# -*- coding: UTF-8 -*-
import os
import csv
import datetime
from collections import defaultdict

def csv_to_dicts(csv_name):
    with open(os.path.join("raw", "{}.csv".format(csv_name))) as csv_file:
        d_reader = csv.DictReader(csv_file)
        return list(d_reader)

continent_dict = {}
for r in csv_to_dicts("continent"):
    continent_dict[r['country']] = r['continent']

health_dict = defaultdict(int)
for r in csv_to_dicts('health'):
    health_dict[r['Country Name']] = r['2016']

goveff_dict = defaultdict(int)
for r in csv_to_dicts('goveff'):
    goveff_dict[r['Country/Territory']] = r['2018Estimate']

country_stat = defaultdict(lambda: defaultdict(int))
translate = {
    'Mainland China': 'China',
    'Hong Kong': 'Hong Kong, China',
    'Macau': 'Macau, China',
    'US': 'United States',
    'UK': 'United Kingdom',
    'Others': 'Cruise',
    'Iran (Islamic Republic of)': 'Iran',
    'Republic of Korea': 'South Korea',
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
translate_health = {
    'South Korea' : "Korea, Dem. People’s Rep.",
    'Iran' : 'Iran, Islamic Rep.',
    'Cruise' : None,
    'Hong Kong, China' : 'Hong Kong SAR, China',
    'Egypt' : 'Egypt, Arab Rep.',
    'Taiwan' : None,
    'Macau, China' : 'Macao SAR, China',
    'Slovakia' : None,
    'French Guiana' : None,
    'Martinique' : None,
    'St. Martin' : 'St. Martin (French part)',
    'Brunei' : 'Brunei Darussalam',
    'Bailiwick of Guernsey' : 'Channel Islands',
    'Vatican City' : None,
    'Saint Barthelemy' : None,
}
translate_gov = {
    'Iran': 'Iran, Islamic Rep.',
    'South Korea': 'Korea, Rep.',
    'Cruise': None,
    'Hong Kong, China': 'Hong Kong SAR, China',
    'Egypt': 'Egypt, Arab Rep.',
    'Taiwan': 'Taiwan, China',
    'Macau, China': 'Macao SAR, China',
    'North Macedonia': 'Macedonia, FYR',
    'Slovakia': 'Slovenia',
    'Faroe Islands': None,
    'St. Martin': None,
    'Brunei': 'Brunei Darussalam',
    'Bailiwick of Guernsey': 'Jersey, Channel Islands',
    'Gibraltar': None,
    'Vatican City': None,
    'Saint Barthelemy': None
}
first_update_nonzero = dict()
last_observation_date = set()
for r in csv_to_dicts("covid_19_data"):

    last_update = None
    try:
        last_update = datetime.datetime.strptime(r['Last Update'], '%m/%d/%Y %H:%M')
    except ValueError as v:
        try:
            last_update = datetime.datetime.strptime(r['Last Update'], '%m/%d/%y %H:%M')
        except ValueError as v:
            last_update = datetime.datetime.strptime(r['Last Update'], '%Y-%m-%dT%H:%M:%S')
    
    last_observation_date.add(last_update)

    c = r['Country/Region'].strip()
    c = translate[c] if c in translate else c

    #c_health = translate_health[c] if c in translate_health else c
    #if not c_health in health_dict:
    #    continue

    c_gov = translate_gov[c] if c in translate_gov else c
    if not c_gov in goveff_dict:
        print(c)
        continue

    confirmed = float(r['Confirmed'])
    deaths = float(r['Deaths'])
    recovered = float(r['Recovered'])

    if not c in first_update_nonzero:
        first_update_nonzero[c] = (confirmed, last_update)
    else:
        l_count, l_update = first_update_nonzero[c]
        if l_count == 0:
            if l_update > last_update:
                first_update_nonzero[c] = (confirmed, last_update)

    if "03/10/2020" != r['ObservationDate'].strip():
        continue

    country_stat[c]['confirmed'] += confirmed
    country_stat[c]['deaths'] += deaths
    country_stat[c]['recovered'] += recovered
    country_stat[c]['continent'] = continent_dict[c]
    country_stat[c]['country'] = c
    #country_stat[c]['health'] = health_dict[c_health]
    country_stat[c]['goveff'] = goveff_dict[c_gov]

print_countries = set()

last_updated = max(last_observation_date)
for k,v in first_update_nonzero.items():
    delta = last_updated - v[1]
    if delta.days > 14:
        print_countries.add(k)
'''
    if (recovered + deaths) > 10:
        death_rate = deaths / (recovered + deaths)
        print(c, death_rate)
'''

headers = []
q1 = []
for r in country_stat.values():
    c = r['country']
    confirmed = float(r['confirmed'])
    deaths = float(r['deaths'])
    recovered = float(r['recovered'])

    if (recovered + deaths) > 1 and c in print_countries:
        death_rate = deaths / (recovered + deaths)
        #print(c, death_rate)
        d = {
            'country':c + ', Day '+str((last_updated-first_update_nonzero[c][1]).days), 
            'continent':r['continent'],
            'mortality_rate':death_rate,
            'n_infected':r['confirmed'],
            'gov_eff':r['goveff']
        }
        #print(r['confirmed'])
        headers = d.keys()
        q1.append(d)

with open('q1.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=headers)
    writer.writeheader()

    for ea in q1:
        writer.writerow(ea)

