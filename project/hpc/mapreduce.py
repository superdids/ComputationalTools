from mrjob.job import MRJob
import json


def type_hashing(entry):
    return entry[13].lower()

class ReduceData(MRJob):
    # Generates a (k,v) pair for each occurrence of a word
    # in a text file.
    def mapper(self, _, line):
        lineJSON = json.loads(line)
        yield type_hashing(lineJSON), 1

    # The reduction step now performs the sum function on the values list,
    # and returns a single value as result.
    def reducer(self, key, values):
        yield key, sum(values)


if __name__ == '__main__':
    ReduceData.run()
