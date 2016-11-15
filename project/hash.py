import json

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

