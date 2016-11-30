import sys

dataCSV = open('dataCrimesByYear.csv', 'w')
data = sys.stdin.read().split('\n')

distinctYears = list()
distinctCrimes = list()
crimesWithNumbers = dict()
yearsLine = ''

count = -1
lastYear = 2001
for line in data:
    if len(line) == 0:
        continue

    year = line[line.find(',') + 2:line.find(']')]
    if year not in distinctYears:
        distinctYears.append(year)
        yearsLine += ',' + year

    crimeNumbers = line[line.find('\t') + 1:len(line)]

    crime = line.split('"')[1::2][0]
    if crime not in distinctCrimes:
        distinctCrimes.append(crime)
        count += 1
        lastYear = 2001
        difference = int(year) - lastYear
        if difference > 0:
            commas = ',' * difference
            crimesWithNumbers[count] = crime + commas + crimeNumbers
        else:
            crimesWithNumbers[count] = crime + ',' + crimeNumbers
        lastYear = int(year)
    else:
        commas = ',' * (int(year) - lastYear)
        crimesWithNumbers[count] += commas + crimeNumbers
        lastYear = int(year)

dataCSV.write(yearsLine + '\n')
for c in crimesWithNumbers:
    dataCSV.write(crimesWithNumbers[c] + '\n')
