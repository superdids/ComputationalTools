import scipy.sparse as ss
import pickle
import time


class Dbscan:

    """
    State information of each point. The dictionary will contain
    the following key-value pairs per point index:
    * visited {int}     Whether the point has been visited (1 = visited,
                        0 = not visited)
    * noise {int}       Whether the point is marked as noise (1 = noisy,
                        0 = not noisy)
    * cluster {int}     Which cluster the point has been assigned to. -1
                        means that it is not (currently) assigned to any
                        cluster.
    * set {set}:        A set consisting of every index in the point that
                        pertains to the cell value 1.
    * neighbors {set}:  A set consisting of all neighbors of the point,
                        which are also depicted using indices.
    """
    __point_information = dict()


    """
    The entry point of the program. The necessary data is initialized
    before executing the algorithm.
    @param dim {int} Indicates which file that is going to be run.
    """
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

        data_set = pickle.load(open(data, 'rb'), encoding='latin1')
        matr = ss.csr_matrix(data_set)

        return self.__dbscan(matr, eps, M)

    """
    Updates information of a point (whether it is marked as noise, visited and/or
    has been assigned to a cluster). If there is no current information of the
    requested point.
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
    Initializes the point information dictionary. The key (index of a point)
    is associated with information of the given point, described in
    __point_information.
    @param {csr_matrix} D   The matrix dataset
    @param {double} eps     Maximum allowed neighborhood distance.
    """

    def __initialize_point_information(self, D, eps):

        for index, P in enumerate(D):
            # The below statement loads a compressed csr_matrix row and converts
            # it to an [1 x n] np matrix. After that, the first position of this
            # matrix is retrieved, so that only the vector (point) is left.
            P = P.toarray()[0]

            self.__point_information[index] = {'visited': 0, 'noise': 0, 'cluster': -1, 'neighbors': set(),
                                               'set': self.__convert_vector_to_set(P)}

        # Determines neighborhood between the points. This code portion is the ultimate
        # bottleneck when running the larger files. Only half the data is investigated,
        # because each neighborhood will be symmetrically added. Also note that
        # this portion of code omits the region query function.
        size = D.shape[0]
        for i, _ in enumerate(D):
            for j in range(i, size):
                distance = self.__compute_distance(self.__point_information[i]['set'], self.__point_information[j]['set'])
                # If the distance is valid between the two points add i to j's neighborhood and vice versa.
                if distance <= eps:
                    self.__point_information[i]['neighbors'].add(j)
                    self.__point_information[j]['neighbors'].add(i)


    '''
    The entry point of the DBSCAN algorithm.
    @param {csr_matrix} D   The matrix dataset
    @param {double} eps     Maximum allowed neighborhood distance.
    @param {int} min_pts    Minimum points needed to form a cluster.
    '''

    def __dbscan(self, D, eps, min_pts):

        #Initialization of values.
        current_cluster_index = -1
        C = []
        initialization_start = time.time()
        self.__initialize_point_information(D, eps)
        initialization_duration = time.time() - initialization_start

        cluster_start = time.time()
        for current_index, P in enumerate(D):
            # The below statement loads a compressed csr_matrix row and converts
            # it to an [1 x n] np matrix. After that, the first position of this
            # matrix is retrieved, so that only the vector (point) is left.
            P = P.toarray()[0]

            if self.__is_visited(current_index):
                continue

            # Mark the current point as visited.
            self.__set_point_information(current_index, visited=1)

            # Retrieve the neighbors of the current point. The neighbor list
            # has been precomputed in the __initialize_point_information function.
            # Thereby, there is no 'regionQuery' function present.
            neighbor_points = self.__point_information[current_index]['neighbors']

            # Mark the point as noise if it lacks the required amount of neighbors.
            if len(neighbor_points) < min_pts:
                self.__set_point_information(current_index, noise=1)
            # Form a cluster otherwise.
            else:
                current_cluster_index += 1
                C.append(
                    self.__expand_cluster(D, current_index, neighbor_points, min_pts, current_cluster_index))

        # The amount of clusters is equivalent to the length of C plus the
        # 'special cluster' (points that have not been assigned to a cluster)
        cluster_count = len(C) + 1

        # A simple list comprehension to compute the largest cluster.
        largest_cluster = max([len(x) for x in C])

        # Reset the point information.
        self.__point_information = dict()

        cluster_duration = time.time() - cluster_start

        return {'count': cluster_count, 'max': largest_cluster,
                'initialization_time': initialization_duration,
                'cluster_time': cluster_duration}

    """
    Expands a cluster by merging the neighborhood of a given point's neighbors
    into the current cluster.
    @param {csr_matrix} D           The matrix dataset
    @param {int} P_index            The index of the current point to be
                                    investigated.
    @param {set} neighbor_points    The neighbors of the current_point, stored
                                    in a set of indices.
    @param {int} min_pts            Minimum points needed in a neighbor set
                                    to merge neighborhood.
    @param {int} current_cluster_index  The index of the cluster that is going
                                        to be expanded.
    """

    def __expand_cluster(self, D, P_index, neighbor_points, min_pts, current_cluster_index):
        # Retrieve the point to be considered from the dataset and store it in the cluster.
        P = D[P_index].toarray()[0]
        C = [P]

        # Assign the point to the current cluster, and ensure it is no longer noise.
        self.__set_point_information(P_index, cluster=current_cluster_index, noise=0)

        # Represents indices of the points that has been iterated past in the
        # while-loop.
        iterated_indices = set()

        while neighbor_points:
            neighbor_index = neighbor_points.pop()
            iterated_indices.add(neighbor_index)

            if not self.__is_visited(neighbor_index):
                self.__set_point_information(neighbor_index, visited=1)

                neighbor_points_m = self.__point_information[neighbor_index]['neighbors']

                if len(neighbor_points_m) >= min_pts:
                    # Takes the union of the neighbor sets. It is then performed set
                    # difference on the result of this operation. This will omit the
                    # indices that has been visited in the final result, stored in
                    # neighbor_points.
                    neighbor_points = (neighbor_points | neighbor_points_m) - iterated_indices

            if not self.__is_in_cluster(neighbor_index):
                C.append(D[neighbor_index])
                self.__set_point_information(neighbor_index, cluster=current_cluster_index, noise=0)
        return C


    """
    Computes the jaccard-distance between two given points.
    @param  {set} A  The first point for the distance calculation
    @param  {set} B  The second point for the distance calculation
    """

    @staticmethod
    def __compute_distance(A, B):
        # If both A and B are empty, J(A,B) is defined as 1.
        # The distance will therefore be: 1 - J(A,B) = 0.
        return 1 - (len(A & B) / len(A | B)) if len(A) != 0 or len(B) != 0 else 0

    """
    Converts a vector (a list of 0s and 1s) into a set, where the
    values of the set are the indexes of the elements in the given
    list that have value 1.
    @param  {list} point     The list to be converted to a set
    """

    @staticmethod
    def __convert_vector_to_set(point):
        current_point = set()
        for i, el in enumerate(point):
            if el == 1:
                current_point.add(i)
        return current_point

# Some simple print function to format the results.
def pretty_print(dim, result):
    print('Results for ', dim, 'x', dim, ':')
    print(' { clusters: ', result['count'], ', amount in biggest cluster: ', result['max'], '}')
    print('Point initalization time: ', result['initialization_time'],
          ' cluster computation time: ', result['cluster_time'])
    print('Total execution time: ', result['initialization_time'] + result['cluster_time'], '\n')

instance = Dbscan()

pretty_print(10, instance.start(10))
pretty_print(100, instance.start(100))
pretty_print(1000, instance.start(1000))
pretty_print(10000, instance.start(10000))
pretty_print(100000, instance.start(100000))