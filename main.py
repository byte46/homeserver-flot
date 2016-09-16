# -*- coding: utf-8 -*
import json
import subprocess
FILENAME = "temperature.rrd"
TIMERANGE = "-48h"

data = []
labels = {
        "out_temp":("Улица", "#2863E8"),
        "room_temp": ("Комната", "#0A4C11"),
        "kitchen_temp": ("Кухня", "#E51226"),
        "bathroom_temp": ("Ванная", "#FF21AD"),
        "radiator_temp": ("Батарея", "#FF0000"),
        "balcony_temp_temp": ("Балкон", "#3F0290")
        }

poutput = subprocess.Popen('export LC_NUMERIC="C.UTF-8";rrdtool fetch temperature.rrd -s-48h AVERAGE', shell=True, stdout=subprocess.PIPE)
for line in poutput.stdout:
    if line.strip() and ':' not in line:
        z = [x for x in line.rstrip().split(' ') if x]
        for i in z:
            data.append({'label': labels[i][0], "color": labels[i][1], 'data':[]})
    elif line.strip() and ':' in line:
        d = []
        time, rrd_data = line.rstrip().split(':')
        d=[x for x in rrd_data.rstrip().split(' ') if x]
        for k, i in enumerate(d):
            data[k]['data'].append([int(time)*1000,i])
        #print d
print json.dumps(data)
