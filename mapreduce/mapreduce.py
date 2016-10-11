from mrjob.job import MRJob

class MapReduce(MRJob):

    def mapper(self, _, line):
        items = dict()

        format_string = lambda string: ''\
            .join(c for c in string if c not in '!"#%&/()=?\\1234567890+.,;:')\
            .lower()

        for word in line.split():
            yield format_string(word), 1

    def reducer(self, key, values):
        yield key, sum(values)


if __name__ == '__main__':
    MapReduce.run()


