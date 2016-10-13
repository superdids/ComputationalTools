from mrjob.job import MRJob
from mrjob.step import MRStep
import itertools

class MapReduce(MRJob):

    # In this function, we specify a customized order
    # of steps to be performed. This is because we will
    # need to gather the edge count information of each
    # vertex in a final reducer.
    def steps(self):
        return [
            MRStep(mapper=self.mapper_find_neighbors,
                   reducer=self.forward_neighbors),
            MRStep(mapper=self.map_two,
                   reducer=self.reduce_two),
            MRStep(reducer=self.reduce_three)
        ]

    # Finds all vertices' neighbors
    def mapper_find_neighbors(self, _, line):
        vertices = line.split()
        u, v = vertices[0], vertices[1]
        yield u, v
        yield v, u

    def forward_neighbors(self, v, neighbors):
        a = [x for x in neighbors]
        #print(v, ' <> ', a)
        yield v, a

        #for x in neighbors:
            #yield v, x

    # Now this mapper will match the expected input as the lecture
    # explained.
    def map_two(self, v, node_pair):

        neighbors = [x for x in node_pair]

        # Ensures that the two-neighboring vertices are always sorted.
        def f(a,b):
            return (a, b) if a < b else (b, a)

        return ((f(v, x), neighbors) for x in neighbors)

    # Now we need to find vertices that two neighbors has
    # in common
    def reduce_two(self, k, values):

        u, v = k[0], k[1]
        def remDup(the_list):
            b = []
            [b.append(uniq) for uniq in the_list if uniq not in b]
            return b

        lst = [x for x in values]#remDup(values)

        #lst = [x for x in values]

        #print(k, ' <> ', lst)
        c = set()
        c.add(u)
        c.add(v)
        #a = set(lst[0])
        #b = set()
        length = 0#len(a - c)

        while len(lst) > 1:
            a = set(lst[0])
            b = set(lst[len(lst)-1])
            length += len((a & b) - c)
            del lst[0]
            del lst[len(lst)-1]


        '''if len(lst) > 1:
            b = set(lst[1])

        print(k, ' > ', lst, ' ----> ', (a & b) - c)

        length = len((a & b) - c)'''
        yield None, length / 2




    def reduce_three(self, _, values):
       # print([x for x in values])
        yield 'Triangle count: ', sum(values)

        #yield 1,1
        #string = "Triangle in sequence: ", k, " ? "
        #str_b = [v for v in values] #any(v is not None for v in values)
        #yield string, str_b #v#sum(1 if v is not None else 0 for v in values)

if __name__ == '__main__':
    MapReduce.run()
