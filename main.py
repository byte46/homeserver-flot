import json
data = []
with open('temperature.txt', 'r') as f:
    for line in f:
        if line.strip() and ':' not in line:
            z = [x for x in line.rstrip().split(' ') if x]
            for i in z:
                data.append({'label': i, 'data':[]})
        elif line.strip() and ':' in line:
            d = []
            time, rrd_data = line.rstrip().split(':')
            d=[x for x in rrd_data.rstrip().split(' ') if x]
            for k, i in enumerate(d):
                data[k]['data'].append([int(time)*1000,i])
            #print d
print json.dumps(data)
