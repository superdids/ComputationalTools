import time

from mrjob.job import MRJob
import json

from mrjob.step import MRStep

LAT = 'lat'
LNG = 'lng'

def location_hashing(entry):
    return entry[27], entry[28]

class MrLocations(MRJob):

    def steps(self):
        return [
            MRStep(mapper=self.passLocations),
            MRStep(mapper=self.yieldPositions)
        ]

    def passLocations(self, _, line):
        lineJSON = json.loads(line)

        lat, lng = location_hashing(lineJSON)
        if type(lat) != type(None) and type(lng) != type(None):
            yield (float(lng), float(lat)), 1

    def yieldPositions(self, key, values):
            yield key#, 1

if __name__ == '__main__':
    start = time.time()
    MrLocations.run()
    end = time.time()
    print('Execution time: ', (end-start))
