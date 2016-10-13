from mrjob.job import MRJob
from mrjob.step import MRStep

class MapReduce(MRJob):

    # In this function, we specify a customized order
    # of steps to be performed. This is because we will
    # need to gather the edge count information of each
    # vertex in a final reducer.
    def steps(self):
        return [
            MRStep(mapper=self.mapper_find_neighbors,
                   reducer=self.reduce_length_two_paths),
            MRStep(mapper=self.map_two,
                   reducer=self.reduce_two)
        ]

    '''
    We avoid cycles by 'directing' the vertices' neighborhood.
    '''
    def mapper_find_neighbors(self, _, line):
        vertices = line.split()
        u, v = vertices[1], vertices[0]
        #print(u, ' ', v)
        yield u, v

    def reduce_length_two_paths(self, v, neighbors):
        for u in neighbors:
            for w in neighbors:
                if u is not w and u is not v and w is not v:
                    print(v, ': ', '(', u, ' ', w, ')')
                    yield v, (u,w)

    '''
    if Input of type #v; (u, w)$ then
    emit #(u, w); v$
    if Input of type #(u, v); ∅$ then
    emit #(u, v); $$
    '''
    def map_two(self, v, node_pair):
        if node_pair is None:
            yield (v[0], v[1]), None
        else:
            yield None, 1#((node_pair[0], node_pair[1]), v)

    def reduce_two(self, v, values):
        if v is None:
            yield "Triangles: ", sum(values)#len(values)#1#sum(1 if x is not None else 0 for x in values)

if __name__ == '__main__':
    MapReduce.run()
