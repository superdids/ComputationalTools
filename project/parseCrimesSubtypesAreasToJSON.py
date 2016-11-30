import sys
import json
import time

# START the timer
start = time.time()

data = sys.stdin.read().split('\n')

distinctCrimes = dict()

for line in data:
    if len(line) == 0:
        continue

    crimeNumbers = int(line[line.find('\t') + 1:len(line)])
    crimeDataArray = line[line.find('[') + 1:line.find(']')].split('", ')
    crime = crimeDataArray[0].replace('"', '')
    crimeSubtype = crimeDataArray[1].replace('"', '')
    crimeArea = crimeDataArray[2].replace('"', '')

    if crime not in distinctCrimes:
        distinctCrimes[crime] = dict()
    if crimeSubtype not in distinctCrimes[crime]:
        distinctCrimes[crime][crimeSubtype] = dict()
    if crimeArea not in distinctCrimes[crime][crimeSubtype]:
        distinctCrimes[crime][crimeSubtype][crimeArea] = crimeNumbers

with open('dataCrimesSubtypesAreas.json', 'w') as jsonFile:
    json.dump(distinctCrimes, jsonFile)

# END the timer
end = time.time()
print('processing time: ', end - start)
