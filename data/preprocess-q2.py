# -*- coding: UTF-8 -*-
import os
import csv
import datetime
from collections import defaultdict

def csv_to_dicts(csv_name):
    with open(os.path.join("raw", "{}.csv".format(csv_name))) as csv_file:
        d_reader = csv.DictReader(csv_file)
        return list(d_reader)

age_accepted = []
age_rev = dict()
s = 0
e = 9
for a in range(100):
    if a > e:
        s = a
        e = a + 9
    age_rev[str(a)] = f"{s}-{e}"
    if not age_rev[str(a)] in age_accepted:
        age_accepted.append(age_rev[str(a)])

c = 0
age_sex_dict = {
    'male' : defaultdict(int),
    'female' : defaultdict(int)
}
death_dict = {
    'male' : defaultdict(int),
    'female' : defaultdict(int)
}
age_fix = {
    '0-10':'0-9',
    '60-60':'60-69',
    '80-80':'80-89',
    '13-19':'10-19',
    '0-6':'0-9'
}
age_set = set()
na = set(["N/A", "NA", "na"])
#for r in csv_to_dicts("COVID19_open_line_list"):
for r in csv_to_dicts("COVID19_line_list_data"):
    sex = r['gender']
    if r['age'] and sex:

        a = r['age']
        if a in na:
            continue
        if sex in na:
            continue

        a = age_fix[a] if a in age_fix else a
        a = age_rev[a] if a in age_rev else a

        if not a in age_accepted:
            continue

        #print(r['outcome'])
        #print(r['date_death_or_discharge'])

        age_sex_dict[sex.lower()][a] += 1
        if r["death"] != '0':
            death_dict[sex.lower()][a] += 1
        c += 1

with open('q2.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=["group", 'male', 'female', 'male_deaths', 'female_deaths'])
    writer.writeheader()

    s = 0
    for aa in age_accepted:
        d = {
            'group':aa,
            'male':age_sex_dict['male'][aa],
            'female':age_sex_dict['female'][aa],
            'male_deaths':death_dict['male'][aa],
            'female_deaths':death_dict['female'][aa],
        }
        s += age_sex_dict['male'][aa] + age_sex_dict['female'][aa]
        writer.writerow(d)
    print(s)