# -*- coding: utf-8 -*
import os
import sys
import getopt
import json
import subprocess
TIMERANGE = "-48h"

LABELS = {
    "out_temp": ("Улица", "#2863E8"),
    "room_temp": ("Комната", "#0A4C11"),
    "kitchen_temp": ("Кухня", "#E51226"),
    "bathroom_temp": ("Ванная", "#FF21AD"),
    "radiator_temp": ("Батарея", "#909090"),
    "balcony_temp_temp": ("Балкон", "#3F0290"),
    #"pressure": ("Давление", "#909090")
}


def parse_rrd_file(input_filename, output_filename=None):
    data = []
    cmd_s = 'export LC_NUMERIC="C.UTF-8";rrdtool fetch {filename} -s{timerange} AVERAGE'
    poutput = subprocess.Popen(
        cmd_s.format(filename=input_filename, timerange=TIMERANGE),
        shell=True,
        stdout=subprocess.PIPE
    )

    for line in poutput.stdout:
        if line.strip() and ':' not in line:
            z = [x for x in line.rstrip().split(' ') if x]
            for i in z:
                data.append({'label': LABELS[i][0], "color": LABELS[i][1], 'data': []})
        elif line.strip() and ':' in line:
            d = []
            time, rrd_data = line.rstrip().split(':')
            d = [x for x in rrd_data.rstrip().split(' ') if x]
            for k, i in enumerate(d):
                data[k]['data'].append([int(time) * 1000, i])

    if not output_filename:
        fname, ext = os.path.splitext(input_filename)
        output_filename = fname + ".json"
    try:
        fd = open(output_filename, "wb")
        fd.write(json.dumps(data))
        fd.close()
    except:
        sys.stderr.write("File write error.\r\n")


def main(argv):
    input_filename = ''
    output_filename = ''
    try:
        if len(argv) == 0:
            raise getopt.GetoptError("Err")
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        sys.stderr.write("main.py -i <inputfile> -o <outputfile>\r\n")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            sys.stderr.write('main.py -i <inputfile> -o <outputfile>\r\n')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            input_filename = arg
        elif opt in ("-o", "--ofile"):
            output_filename = arg
    if input_filename:
        parse_rrd_file(input_filename, output_filename)


if __name__ == "__main__":
    main(sys.argv[1:])
