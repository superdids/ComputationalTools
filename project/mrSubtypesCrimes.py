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


def subtype_hashing(entry):
    return entry[14].lower()


def area_hashing(entry):
    try:
        return entry[15].lower()
    except:
        None


class ReduceData(MRJob):
    # Generates a (k,v) pair for each occurrence of a word
    # in a text file.
    def mapper(self, _, line):
        lineJSON = json.loads(line)
        crimeType = type_hashing(lineJSON)
        crimeSubtype = subtype_hashing(lineJSON)
        crimeArea = area_hashing(lineJSON)

        if crimeType and crimeSubtype and crimeArea:
            if crimeType in valid_crime_types:
                yield (crimeType, crimeSubtype, crimeArea), 1

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
    # print('processing time: ', end - start)
