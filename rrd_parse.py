# -*- coding: utf-8 -*
import os
import sys
import getopt
import json
import subprocess

DEBUG_PORT = 8000

RRDTOOL = "/usr/bin/rrdtool"
TIMERANGE = "-48h"

LABELS = {
    "out_temp": ("Улица", "#2863E8"),
    "room_temp": ("Комната", "#0A4C11"),
    "kitchen_temp": ("Кухня", "#E51226"),
    "bathroom_temp": ("Ванная", "#FF21AD"),
    "radiator_temp": ("Батарея", "#909090"),
    "balcony_temp": ("Балкон", "#3F0290"),
    "pressure": ("Давление", "#2020FF"),
    "room_brightness": ("Освещённость в комнате", "#FF6F4E"),
    "room_humidity": ("Влажность в комнате", "#2020FF"),
    "out_humidity": ("Влажность на улице", "#FF2020"),
    "l_current": ("Разряды молний", "#FF2020")
}


def parse_rrd_file(input_filename, output_filename=None, exclude=None):
    data = []
    cmd_s = 'LC_NUMERIC="C" {rrdtool} fetch {filename} -s{timerange} AVERAGE'
    poutput = subprocess.Popen(
        cmd_s.format(
            rrdtool=RRDTOOL,
            filename=input_filename,
            timerange=TIMERANGE
        ),
        shell=True,
        stdout=subprocess.PIPE
    )

    for line in poutput.stdout:
        if line.strip() and ':' not in line:
            z = [x for x in line.rstrip().split(' ') if x]
            for i in z:
                data.append(
                    {
                        'label': LABELS.get(i, (i,))[0],
                        "color": LABELS.get(i, (0, "#909090"))[1],
                        'data': []
                    }
                )
        elif line.strip() and ':' in line:
            d = []
            time, rrd_data = line.rstrip().split(':')
            d = [x for x in rrd_data.rstrip().split(' ') if x]
            for k, i in enumerate(d):
                data[k]['data'].append([int(time) * 1000, i])

    pdata = []
    for k, v in enumerate(data):
        if k not in exclude:
            pdata.append(v)
    data = pdata
    del(pdata)
    if not output_filename:
        fname, ext = os.path.splitext(input_filename)
        output_filename = fname + ".json"
    try:
        fd = open(output_filename, "wb")
        fd.write(json.dumps(data))
        fd.close()
    except:
        sys.stderr.write("File write error.\r\n")

def application(environ, start_response):
    start_response("200 OK", [("Content-Type", "text/html")])
    return("Server is running OK.")

def main(argv):
    input_filename = ''
    output_filename = ''
    exclude = []
    help_str = """
rrd_parse.py -i <inputfile> -o <outputfile> -e <exclude list>\r\n
Example:
\trrd_parse.py -i data.rrd -o data.json -e 1,2\r\n"""
    try:
        if len(argv) == 0:
            raise getopt.GetoptError("Err")
        opts, args = getopt.getopt(argv, "hi:o:e:d", ["ifile=", "ofile=", "exclude="])
    except getopt.GetoptError:
        sys.stderr.write(help_str)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            sys.stderr.write(help_str)
            sys.exit()
        elif opt in ("-i", "--ifile"):
            input_filename = arg
        elif opt in ("-o", "--ofile"):
            output_filename = arg
        elif opt in ("-e", "--exclude"):
            exclude = arg
        elif opt == "-d":
            sys.stderr.write(
                "Daemon mode enabled. Port: {port}\r\n".format(
                    port=DEBUG_PORT
                )
            )
            from wsgiref.simple_server import make_server
            httpd = make_server('', DEBUG_PORT, application)
            httpd.serve_forever()
    if exclude:
        exclude = [int(x) for x in exclude.split(',')]
    if input_filename:
        parse_rrd_file(input_filename, output_filename, exclude)


if __name__ == "__main__":
    main(sys.argv[1:])
