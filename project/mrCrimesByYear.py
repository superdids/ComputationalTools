import datetime
import time
from mrjob.job import MRJob
import json

valid_crime_types = {
    'robbery',
    'stalking',
    'prostitution',
    'narcotics',
    'motor vehicle theft',
    'kidnapping',
    'theft',
    'assault',
    'battery'
}


def type_hashing(entry):
    return entry[13].lower()


def year_hashing(entry):
    date_object = datetime.datetime.strptime(entry[10], '%Y-%m-%dT%H:%M:%S')
    year = date_object.year
    return year


class ReduceData(MRJob):
    # Generates a (k,v) pair for each occurrence of a word
    # in a text file.
    def mapper(self, _, line):
        lineJSON = json.loads(line)
        crimeType = type_hashing(lineJSON)
        crimeYear = year_hashing(lineJSON)

        if crimeType in valid_crime_types:
            yield (crimeType, crimeYear), 1

    # The reduction step now performs the sum function on the values list,
    # and returns a single value as result.
    def reducer(self, key, values):
        yield key, sum(values)


if __name__ == '__main__':
    # START the timer
    start = time.time()

    ReduceData.run()

    # END the timer
    end = time.time()
    print('processing time: ', end - start)
