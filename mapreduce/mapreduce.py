from mrjob.job import MRJob
from mrjob.step import MRStep

class MapReduce(MRJob):

    # In this function, we specify a customized order of steps to be
    # performed. This is because we will need to gather the edge
    # count information of each vertex in a final reducer.
    def steps(self):
        return [
            MRStep(mapper=self.mapper_find_neighbors,
                   reducer=self.forward_neighbors),
            MRStep(mapper=self.map_two,
                   reducer=self.reduce_two),
            # We had some issues collecting the count in the second reducer,
            # so we performed a third step with a reducer collecting the sum
            # of triangle counts.
            MRStep(reducer=self.sum_values)
        ]

    # Finds all vertices' neighbors.
    def mapper_find_neighbors(self, _, line):
        vertices = line.split()
        u, v = vertices[0], vertices[1]
        yield u, v
        yield v, u

    # As we want the mapper in step two to receive all neighbors per
    # vertex at a time, we will have to accumulate those in a reducer
    # before directing them.
    def forward_neighbors(self, v, neighbors):
        yield v, [x for x in neighbors]


    # This mapper receives a vertex v and all neighbors of v. With this information,
    # we can combine each element, x, of the neighbor-lists (generator), with v. This forms
    # tuples, that we can associate to the neighbor-lists. By ordering these
    # tuples in terms of (v,x) when v < x and (x,v) when otherwise, we will get
    # x's neighbor-lists appended to the same (v,x) tuple - indicating that
    # they will hold both v's and x's neighbor-lists. Thereby, in the later step, we can
    # compare the two-neighbor vertices' common neighbors - which forms triangle-
    # relationships.
    def map_two(self, v, node_pair):

        neighbors = [x for x in node_pair]

        # Ensures that the two-neighboring vertices tuple always is sorted.
        def f(a,b):
            return (a, b) if a < b else (b, a)

        return ((f(v, x), neighbors) for x in neighbors)

    # Now we need to find neighbor vertices that two-neighbor vertices has
    # in common.
    def reduce_two(self, k, values):
        # Store the two-neighbor vertices in different variables.
        u, v = k[0], k[1]

        # Removes duplicates from a list, this is performed in order to
        # discard any additional neighboring lists that appears when
        # two-neighboring nodes have more than one edge between each other.
        def remDup(collection):
            to_return = []
            [to_return.append(uniq) for uniq in collection if uniq not in to_return]
            return to_return
        values = remDup(values)

        # c represents the two-neighbor vertices, which should not be included
        # among the common neighbors set.
        c = set([u,v])
        #c.add(u)
        #c.add(v)

        #length = 0

        #if len(lst) > 1:
        a, b = set(values[0]), set(values[1])

        #print(k, ' > ', values, ' ----> ', (a & b) - c)

        # Now we find all neighbors that u and v has in common (again, excluding
        # u and v themselves by performing set difference with c).
        tmp_neighbors = (a & b) - c

        # In order to avoid adding duplicate triangles, we discard any neighbor, w,
        # where w < u or w < v.
        neighbors = set()
        while tmp_neighbors:
            w = tmp_neighbors.pop()
            if w > u and w > v:
                neighbors.add(w)

        # The amount of new neighbors will indicate the amount
        # of new triangle counts to be emitted.
        yield None, len(neighbors)



    # The third reducer sums up the triangle counts.
    def sum_values(self, _, values):
        yield 'Triangle count: ', sum(values)

if __name__ == '__main__':
    MapReduce.run()
