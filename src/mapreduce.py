from mrjob.job import MRJob

class MapReduce(MRJob):

    def mapper(self, _, line):
        items = dict()

        exists = lambda key: key in items
        format_string = lambda string: ''\
            .join(c for c in string if c not in '!"#%&/()=?\\1234567890+.,;:')\
            .lower()

        for word in line.split():
            word = format_string(word)
            if exists(word):
                items[word].append(1)
            else:
                items[word] = [1]

        #for key in items:
            #print('k: ', key, ', v: ', items[key])

            #yield key, items[key]

        return ((key, items[key]) for key in items)

    def reducer(self, key, values):

        yield key, sum(values)


if __name__ == '__main__':
    MapReduce.run()


