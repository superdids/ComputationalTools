import json

import datetime

fields = dict()
with open('jsun.json') as f:
    data = json.load(f)

for i, field in enumerate(data['meta']['view']['columns']):
    fields[field['name'].lower()] = i

crimes = dict()
for crime in data['data']:
    crimeType = crime[fields['primary type']].lower()
    if crimeType not in crimes:
        crimes[crimeType] = []
        crimes[crimeType].append(crime)
    else:
        crimes[crimeType].append(crime)

def featureHashingYear(dateString):
    date_object = datetime.datetime.strptime(dateString, '%Y-%m-%dT%H:%M:%S')
    year = date_object.year
    result = year - 2001
    return result

for i,_ in enumerate(data['data']):
    idx = featureHashingYear(data['data'][i][10])
    data['data'][i].append(str(idx))

for x in data['data']:
    print(x)

