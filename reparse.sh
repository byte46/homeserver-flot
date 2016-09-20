#!/bin/bash
scp homeserver:/home/byte/scripts/rrd/temperature.rrd .
scp homeserver:/home/byte/scripts/rrd/misc.rrd .
scp homeserver:/home/byte/scripts/rrd/pressure.rrd .
scp homeserver:/home/byte/scripts/rrd/lightnings.rrd .
python rrd_parse.py -i temperature.rrd
python rrd_parse.py -i misc.rrd -e 1
python rrd_parse.py -i misc.rrd -o brightness.json -e 0,2
python rrd_parse.py -i lightnings.rrd
python rrd_parse.py -i pressure.rrd
