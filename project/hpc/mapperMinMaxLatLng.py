#!/usr/bin/env python

import ijson

import sys

LAT_MAX = 'lat_max'
LNG_MAX = 'lng_max'
LAT_MIN = 'lat_min'
LNG_MIN = 'lng_min'

def location_hashing(entry):
    return entry[27], entry[28]


for entry in ijson.items(sys.stdin, 'data.item'):
    lat, lng = location_hashing(entry)

    if type(lat) != type(None):
        print('%s\t%f' % (LAT_MAX, float(lat)))
        print('%s\t%f' % (LAT_MIN, float(lat)))

    if type(lng) != type(None):
        print('%s\t%f'% (LNG_MAX, float(lng)))
        print('%s\t%f'% (LNG_MIN, float(lng)))


#for line in sys.stdin:
#    line = line.strip()
#    keys = line.split()
#    for key in keys:
#        value = 1
#        print( "%s\t%d" % (key, value) )