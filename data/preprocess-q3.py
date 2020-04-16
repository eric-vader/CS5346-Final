# -*- coding: UTF-8 -*-
import os
import csv
import datetime
from collections import defaultdict
from collections import Counter

def csv_to_dicts(csv_name):
    with open(os.path.join("raw", "{}.csv".format(csv_name))) as csv_file:
        d_reader = csv.DictReader(csv_file)
        return list(d_reader)

symptoms = []
for r in csv_to_dicts("COVID19_open_line_list"):
    sym = r["symptoms"].strip().lower()
    if sym:
        if ',' in sym:
            sym_l = [ 'fever' if 'fever' in s else s.strip() for s in sym.split(',') ]
            
        elif ';' in sym:
            sym_l = [ 'fever' if 'fever' in s else s.strip() for s in sym.split(';') ]
        elif 'fever' in sym:
            sym_l = ['fever']
        else:
            sym_l = [ sym ]
        symptoms.extend(sym_l)   
count_sym = Counter(symptoms)

common_syn = count_sym.most_common(25)
print(common_syn)

with open('q3.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=["word", 'size'])
    writer.writeheader()

    for w, c in common_syn:
        d = {
            'word':w,
            'size':c
        }
        writer.writerow(d)
