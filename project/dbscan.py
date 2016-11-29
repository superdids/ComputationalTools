import scipy.sparse as ss
import pickle
import time
import math


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

    def start(self):

        M = 2
        eps = 0.85

        data_set = []
        with open('positions_test.txt', 'rb') as f:
            contents = f.readlines()
            for l in contents:
                positions_list = l.split('\t')
                data_set.append((float(positions_list[0]), float(positions_list[1].strip('\n'))))

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
                                               'point': P}

        # Determines neighborhood between the points. This code portion is the ultimate
        # bottleneck when running the larger files. Only half the data is investigated,
        # because each neighborhood will be symmetrically added. Also note that
        # this portion of code omits the region query function.
        size = D.shape[0]
        for i, _ in enumerate(D):
            for j in range(i, size):
                distance = self.__compute_distance(self.__point_information[i]['point'],
                                                   self.__point_information[j]['point']) / 100

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

        # Initialization of values.
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
    Computes the euclidean-distance between two given points.
    @param  {set} A  The first point for the distance calculation
    @param  {set} B  The second point for the distance calculation
    """

    @staticmethod
    def __compute_distance(A, B):
        return math.sqrt(math.pow(A[0] - B[0], 2) + math.pow(A[1] + B[1], 2))


# Some simple print function to format the results.
def pretty_print(result):
    print('Results for positions:')
    print(' { clusters: ', result['count'], ', amount in biggest cluster: ', result['max'], '}')
    print('Point initialization time: ', result['initialization_time'],
          ' cluster computation time: ', result['cluster_time'])
    print('Total execution time: ', result['initialization_time'] + result['cluster_time'], '\n')


instance = Dbscan()

pretty_print(instance.start())
