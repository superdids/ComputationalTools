from mrjob.job import MRJob

class Exercise1(MRJob):

    # Generates a (k,v) pair for each occurence of a word
    # in a text file.
    def mapper(self, _, line):

        # Formats a string by omitting certain characters, then
        # lower-cases the resulting string.
        format_string = lambda string: '' \
            .join(c for c in string if c not in '!"#%&/()=?\\1234567890+.,;:') \
            .lower()

        # Now we yield each occurrence of a word (along with 1 to describe
        # 'one occurrence of this word'). This will be automatically grouped
        # by the group step in the MapReduce paradigm.
        for word in line.split():
            yield format_string(word), 1

    # The reduction step now performs some function on the values list,
    # and returns a single value as result.
    def reducer(self, key, values):
        # In our case, we are interested in the sum of occurences of
        # a word.
        yield key, sum(values)


if __name__ == '__main__':
    Exercise1.run()


