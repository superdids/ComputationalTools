import json

with open('testData.json') as f:
    dataJSON = json.load(f)
    dataText = open('data.txt', 'w')
    for crime in dataJSON['data']:
        crimeText = json.dumps(crime)
        dataText.write(crimeText + '\n')

    dataText.close()
