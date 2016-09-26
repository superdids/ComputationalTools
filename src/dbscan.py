import scipy.sparse as ss
import pickle
#For formating.
import json

class Dbscan:

    __point_information = dict()

    def start(self):
        data = '../files/data_10points_10dims.dat'
        small_set = pickle.load(open(data, 'rb'), encoding='latin1')
        matr = ss.csr_matrix(small_set).toarray()
        print(matr)
        M = 2
        eps = 0.4
        self.__dbscan(matr, eps, M)

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
            self.__point_information[P_i] = { 'visited': 0, 'noise': 0, 'cluster': -1}
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
        if P_i not in self.__point_information:
            self.__set_point_information(P_i)
            return False
        return self.__point_information[P_i]['visited'] == 1

    """
    Determines whether a point is placed in a cluster.
    @param  {int} P_i  The index of point P, which is used as unique key in the
    __point_information dict-object.
    """
    def __is_in_cluster(self, P_i):
        if P_i not in self.__point_information:
            self.__set_point_information(P_i)
            return False
        return self.__point_information[P_i]['cluster'] > -1

    """
      Determines whether a point is marked as noise.
      @param  {int} P_i  The index of point P, which is used as unique key in the
      __point_information dict-object.
    """
    def __is_noise(self, P_i):
        if P_i not in self.__point_information:
            self.__set_point_information(P_i)
            return False
        return self.__point_information[P_i]['noise'] == 1

    '''
    Before docing this, make sure the variables have proper names.
    '''
    def __dbscan(self, D, eps, min_pts):
        current_cluster_index = -1
        C = []

        for current_index,P in enumerate(D):

            if self.__is_visited(current_index) and not self.__is_noise(current_index):
                continue

            self.__set_point_information(current_index, visited=1)

            neighbour_points = self.__region_query(D, P, eps)

            if len(neighbour_points) < min_pts:
                self.__set_point_information(current_index, noise=1)
            else:
                current_cluster_index += 1
                C.append(self.__expand_cluster(D, P, current_index, neighbour_points, eps, min_pts, current_cluster_index))

        #Print each cluster and it's contents
        #for c in C:
            #print(c)

        #Print the amount of clusters
        #print(len(C))

        # Print information for each point.
        #print(json.dumps(self.__point_information, indent=2))
        self.__point_information = dict()


    def __expand_cluster(self, D, P, P_index, neighbor_points, eps, min_pts, current_cluster_index):
        C = [P]
        self.__set_point_information(P_index, cluster=current_cluster_index, noise=0)
        index = 0

        def contains(item, collection):
            return len(list(filter(lambda x: x[0] == item[0], collection))) > 0
        #This loop was changed from a foor loop, in order to be able to
        #iterate through all items in the neighbor_points - in case
        #it get updated within the loop itself.
        while index < len(neighbor_points):
            P_tuple = neighbor_points[index]
            if not self.__is_visited(P_tuple[0]):
                self.__set_point_information(P_tuple[0], visited=1)
                neighbor_points_m = self.__region_query(D, P_tuple[1], eps)
                if len(neighbor_points_m) >= min_pts:
                    # Don't add duplicates when joining the two lists.
                    neighbor_points = neighbor_points + [x for x in neighbor_points_m if not contains(x, neighbor_points)]

            if not self.__is_in_cluster(P_tuple[0]):
                C.append(P_tuple[1])
                self.__set_point_information(P_index, cluster=current_cluster_index, noise=0)
            index += 1

        return C

    """
    Computes the distance between two given points.
    @param  {set} A  The first point for the distance calculation
    @param  {set} B  The second point for the distance calculation
    """
    @staticmethod
    def __compute_distance(A, B):
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
    def __region_query(self, D, P, eps):
        neighbourhood = []
        __P = self.__convert_vector_to_set(P)
        for index,point in enumerate(D):
            point_as_set = self.__convert_vector_to_set(point)
            # list_sets.append(point_as_set) #--> uncommend this line if you want to have a GLOBAl list of the points as sets
            if self.__compute_distance(__P, point_as_set) <= eps:
                neighbourhood.append((index, point))
        return neighbourhood

Dbscan().start()
