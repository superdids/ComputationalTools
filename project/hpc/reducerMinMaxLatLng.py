#!/usr/bin/env python

import sys

LAT_MAX = 'lat_max'
LNG_MAX = 'lng_max'
LAT_MIN = 'lat_min'
LNG_MIN = 'lng_min'

current_max_lat = -1000
current_max_lng = -1000
current_min_lat = 1000
current_min_lng = 1000

for line in sys.stdin:

    line = line.strip()
    key, value = line.split('\t', 1)
    value = float(value)

    if key == LAT_MAX:
        current_max_lat = current_max_lat if value < current_max_lat else value
    elif key == LNG_MAX:
        current_max_lng = current_max_lng if value < current_max_lng else value
    elif key == LAT_MIN:
        current_min_lat = current_min_lat if value > current_min_lat else value
    elif key == LNG_MIN:
        current_min_lng = current_min_lng if value > current_min_lng else value

print('%s\t%f' % (LAT_MAX, current_max_lat))
print('%s\t%f' % (LNG_MAX, current_max_lng))
print('%s\t%f' % (LAT_MIN, current_min_lat))
print('%s\t%f' % (LNG_MIN, current_min_lng))
