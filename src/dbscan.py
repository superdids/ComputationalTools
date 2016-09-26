import scipy.sparse as ss
import pickle
# For formating.
import json
import time

class Dbscan:
    __point_information = dict()

    def start(self, dim):

        M = 2
        eps = 0.15
        if dim == 10:
            data = '../files/data_10points_10dims.dat'
            eps = 0.4
        elif dim == 100:
            data = '../files/data_100points_100dims.dat'
            eps = 0.3
        elif dim == 1000:
            data = '../files/data_1000points_1000dims.dat'
        elif dim == 10000:
            data = '../files/data_10000points_10000dims.dat'
        elif dim == 100000:
            data = '../files/data_100000points_100000dims.dat'
        else:
            raise ValueError('Invalid dimension specification.')
            return
        '''data = '../files/data_100points_100dims.dat'
            M = 2
            eps = 0.3'''
        data_set = pickle.load(open(data, 'rb'), encoding='latin1')
        matr = ss.csr_matrix(data_set)
        #for i in enumerate(ss_matr):
            #print(i)
        #matr = ss_matr.toarray()

        return self.__dbscan(matr, eps, M)

    """
    Updates information of a point (whether it is marked as noise, visited and/or
    has been assigned to a cluster). If there is no current information of the
    requested point, an entry for the point will be initialized with:
    NOT visited (visited = 0), NOT noise (noise = 0) and NOT in a cluster (cluster = -1).
    @param  {int} P_i  The index of point P, which is used as unique key in the
    __point_information dict-object.
    @param  {int} visited (optional, default value is None) If this value is assigned, the
    P_i entry will be overridden with the assigned value of visited.
    @param  {int} noise (optional, default value is None) If this value is assigned, the
    P_i entry will be overridden with the assigned value of noise.
    @param  {int} cluster (optional, default value is None) If this value is assigned, the
    P_i entry will be overridden with the assigned value of cluster.
    """

    def __set_point_information(self, P_i, visited=None, noise=None, cluster=None):
        if P_i not in self.__point_information:
            self.__point_information[P_i] = {'visited': 0, 'noise': 0, 'cluster': -1}
        if visited is not None:
            self.__point_information[P_i]['visited'] = visited
        if noise is not None:
            self.__point_information[P_i]['noise'] = noise
        if cluster is not None:
            self.__point_information[P_i]['cluster'] = cluster

    """
    Determines whether a point has been visited.
    @param  {int} P_i  The index of point P, which is used as unique key in the
    __point_information dict-object.
    """

    def __is_visited(self, P_i):
        return self.__point_information[P_i]['visited'] == 1

    """
    Determines whether a point is placed in a cluster.
    @param  {int} P_i  The index of point P, which is used as unique key in the
    __point_information dict-object.
    """

    def __is_in_cluster(self, P_i):
        return self.__point_information[P_i]['cluster'] > -1

    """
      Determines whether a point is marked as noise.
      @param  {int} P_i  The index of point P, which is used as unique key in the
      __point_information dict-object.
    """

    def __is_noise(self, P_i):
        return self.__point_information[P_i]['noise'] == 1

    """
    Inititalizes the point information dictionary. The key (index of a point)
    is associated with information regarding noise, visited and cluster assignment,
    as well as a set representing the indices of points that have a jaccard distance
    of eps less close to the given point.
    @param {matrix} D   The matrix dataset, loaded from the file
    @param {double} eps The epsilon for the dataset
    """

    def __initialize_point_information(self, D, eps):

        for index, P in enumerate(D):

            #TODO: ADDED below
            P = P.toarray()[0]

            self.__point_information[index] = {'visited': 0, 'noise': 0, 'cluster': -1, 'neighbors': set(),
                                               'set': self.__convert_vector_to_set(P)}
            del P

        size = D.shape[0]
        for i, X in enumerate(D):
            for j in range(i, size):
                distance = self.__compute_distance(self.__point_information[i]['set'], self.__point_information[j]['set'])
                if distance <= eps:
                    self.__point_information[i]['neighbors'].add(j)
                    self.__point_information[j]['neighbors'].add(i)

        print('__initialize_point_information() complete!!')

    '''
    Before docing this, make sure the variables have proper names.
    '''

    def __dbscan(self, D, eps, min_pts):
        current_cluster_index = -1
        C = []

        self.__initialize_point_information(D, eps)


        for current_index, P in enumerate(D):
            #TODO: ADDED
            P = P.toarray()[0]
            if self.__is_visited(current_index):
                continue

            self.__set_point_information(current_index, visited=1)

            # TODO: Uncommented
            #neighbor_points = self.__region_query(D, current_index, eps)
            neighbor_points = self.__point_information[current_index]['neighbors']


            if len(neighbor_points) < min_pts:
                self.__set_point_information(current_index, noise=1)
            else:
                current_cluster_index += 1
                # C.append(self.__expand_cluster(D, (P, current_index), neighbor_points, eps, min_pts, current_cluster_index))
                C.append(
                    self.__expand_cluster(D, P, current_index, neighbor_points, eps, min_pts, current_cluster_index))

            del P


        # Print the amount of clusters
        # print(len(C))

        # Print information for each point.
        # print(json.dumps(self.__point_information, indent=2))

        cluster_count = len(C) + 1  # + 1 to add the special cluster (points that are not assigned to a cluster)
        largest_cluster = max([len(x) for x in C])

        self.__point_information = dict()

        return {'count': cluster_count, 'max': largest_cluster}

    def __expand_cluster(self, D, P, P_index, neighbor_points, eps, min_pts, current_cluster_index):
        C = [P]
        self.__set_point_information(P_index, cluster=current_cluster_index, noise=0)

        iterated_indices = set()

        while neighbor_points:
            neighbor_index = neighbor_points.pop()
            iterated_indices.add(neighbor_index)
            if not self.__is_visited(neighbor_index):
                self.__set_point_information(neighbor_index, visited=1)
                #TODO: Uncommented
                neighbor_points_m = self.__point_information[neighbor_index]['neighbors']
                #neighbor_points_m = self.__region_query(D, neighbor_index, eps)

                if len(neighbor_points_m) >= min_pts:
                    neighbor_points = (neighbor_points | neighbor_points_m) - iterated_indices

            if not self.__is_in_cluster(neighbor_index):
                C.append(D[neighbor_index])
                self.__set_point_information(neighbor_index, cluster=current_cluster_index, noise=0)
        return C


    """
    Computes the distance between two given points.
    @param  {set} A  The first point for the distance calculation
    @param  {set} B  The second point for the distance calculation
    """

    @staticmethod
    def __compute_distance(A, B):
        if len(A) == 0 and len(B) == 0:
            return 0
        return 1 - (len(A & B) / len(A | B))

    """
    Converts a vector (a list of 0s and 1s) into a set, where the values of the set are the indexes of the elements in
    the given list that have value 1.
    @param  {list} point     The list to be converted to a set
    """

    @staticmethod
    def __convert_vector_to_set(point):
        current_point = set()
        for i, el in enumerate(point):
            if el == 1:
                current_point.add(i)
        return current_point

    """
    Gathers the neghbourhood of points, for a given point
    @param  {matrix} D   The matrix dataset, loaded from the file
    @param  {list}   P   The point, of which to gather the neighbourhood
    @param  {double} eps The epsilon for the dataset
    """
    def __region_query(self, D, P_index, eps):
        neighborhood = set()
        neighborhood.add(P_index)

        A = self.__point_information[P_index]['set']
        for index, point in enumerate(D):
            if P_index not in self.__point_information[index]['neighbors']:
                B = self.__point_information[index]['set']
                distance = self.__compute_distance(A, B)
                if distance <= eps:
                    self.__point_information[index]['neighbors'].add(P_index)
                    self.__point_information[P_index]['neighbors'].add(index)
                    neighborhood.add(index)
            else:
                neighborhood.add(index)

        return neighborhood
    '''def __region_query(self, D, P, eps):
        neighbourhood = []
        A = self.__convert_vector_to_set(P)
        for index, point in enumerate(D):
            B = self.__convert_vector_to_set(point)
            # list_sets.append(point_as_set) #--> uncommend this line if you want to have a GLOBAl list of the points as sets
            if self.__compute_distance(A, B) <= eps:
                neighbourhood.append((index, point))
        return neighbourhood'''


def pretty_print(dim, start_time,result):
    print('Results for ', dim, 'x', dim, ': { clusters: ', result['count'], ', amount in biggest cluster: ',
          result['max'], '}', ' execution time: ', time.time() - start_time)


instance = Dbscan()


pretty_print(10, time.time(), instance.start(10))
pretty_print(100, time.time(), instance.start(100))
pretty_print(1000, time.time(), instance.start(1000))
pretty_print(10000, time.time(), instance.start(10000))
pretty_print(100000, time.time(), instance.start(100000))