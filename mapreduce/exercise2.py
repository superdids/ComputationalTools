from mrjob.job import MRJob
from mrjob.step import MRStep

class Exercise2(MRJob):

    # In this function, we specify a customized order
    # of steps to be performed. This is because we will
    # need to gather the edge count information of each
    # vertex in a final reducer.
    def steps(self):
        return [
            MRStep(mapper=self.mapper,
                   reducer=self.reducer_vertices_edge_count),
            MRStep(reducer=self.reducer_every_vertex_even)
        ]

    # In the mapper, we read each line and extract a pair of
    # vertices. We yield each vertex as a key and 1 as the
    # value (edge count), so that we accumulate the number of
    # edges for each vertex. This is because the same keys are
    # heading to the same reducer.
    def mapper(self, _, line):
        vertices = line.split()
        yield vertices[0], 1
        yield vertices[1], 1

    # When the values enter the first reduction step, we want
    # to send a single list to the second reduction step - as
    # we rely on a single output in this exercise. A single list
    # can be passed to another reduction function by simply
    # associating all yielded values to a single key - for instance
    # 'result'. We basically yield values True and False, which
    # indicates that a specific vertex has an even amount of edges
    # or not.
    def reducer_vertices_edge_count(self, vertex, values):
        yield 'result', (sum(values) % 2 == 0, vertex)

    # When the values enter the second reduction step, the function
    # receives only one key - and consequently only one generator.
    # By checking if every vertex has an even amount of edges,
    # we know whether there is a euler path or not in the graph. We
    # are not interested in the vertex names in this case, which is
    # why the underscore in (x,_) is used.
    def reducer_every_vertex_even(self, _, values):
        yield "Euler tour? ", all(x for (x,_) in values)


if __name__ == '__main__':
    Exercise2.run()
