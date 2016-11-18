import json
import ijson

with open('testData.json') as f:
    dataJSON = ijson.items(f, 'data.item')
    dataText = open('data.txt', 'w')
    for crime in dataJSON:
        crimeText = json.dumps(crime)
        dataText.write(crimeText + '\n')

    dataText.close()
