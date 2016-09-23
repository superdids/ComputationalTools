import numpy as np
import pandas as pd
from pandas import Series, DataFrame, Index
import scipy.sparse as ss
import pickle

class Dbscan:

    __point_information = dict()

    def start(self):
        data = '../files/data_10points_10dims.dat'
        small_set = pickle.load(open(data, 'rb'), encoding='latin1')
        matr = ss.csr_matrix(small_set).toarray()
        '''
        a = [1,0,0]
        b = [1,1,1]
        u = set()
        v = set()
        for idx,i in enumerate(a):
            if i == 1:
                u.add(idx)

        for idx,i in enumerate(b):
            if i == 1:
                v.add(idx)

        print((len(u & v)/len(u | v)))

        print(matr)
        '''
        self.__dbscan(matr, 0.4, 2)


    def __set_point_information(self, P, visited=None, noise=None, cluster=None):
        if P not in self.__point_information:
            self.__point_information[P] = { 'visited': 0, 'noise': 0, 'cluster': -1}
        if visited is not None:
            self.__point_information[P]['visited'] = visited
        if noise is not None:
            self.__point_information[P]['noise'] = noise
        if cluster is not None:
            self.__point_information[P]['cluster'] = cluster

    def __is_visited(self, P):
        if P not in self.__point_information:
            self.__set_point_information(P)
            return False
        return self.__point_information[P]['visited'] == 1

    def __is_in_cluster(self, P):
        if P not in self.__point_information:
            self.__set_point_information(P)
            return False
        return self.__point_information[P]['cluster'] > -1


    def __dbscan(self, D, eps, min_pts):
        current_cluster = -1
        C = []

        for current_index,P in enumerate(D):

            if self.__is_visited(current_index):
                continue

            self.__set_point_information(current_index, visited=1)

            neighbor_points = self.__region_query(D, P, eps)

            if len(neighbor_points) < min_pts:
                self.__set_point_information(current_index, noise=1)
            else:
                current_cluster += 1
                C.append([None])
                #C[current_cluster] = list()
                C[current_cluster] = self.__expand_cluster(D, P, current_index, neighbor_points, C[current_cluster], eps, min_pts, current_cluster)

        print(C)
        self.__point_information = dict()


    def __expand_cluster(self, D, P, P_index, neighbor_points, current_cluster, eps, min_pts, current_cluster_index):
        current_cluster.append(P)
        self.__set_point_information(P_index, cluster=current_cluster_index)

        for i, P_m in enumerate(neighbor_points):
            if not self.__is_visited(i):
                self.__set_point_information(i, visited=1)
                # TODO: Add arguments when Galin has implemented the below function.
                neighbor_points_m = self.__region_query(D, P_m, eps)
                if len(neighbor_points_m) >= min_pts:
                    neighbor_points = neighbor_points + neighbor_points_m

            if not self.__is_in_cluster(i):
                current_cluster.append(P_m)
                self.__set_point_information(P_index, cluster=current_cluster_index)

        return current_cluster

    """
    Computes the distance between two given points.
    @param  {set} A  The first point for the distance calculation
    @param  {set} B  The second point for the distance calculation
    """
    def __compute_distance(self, A, B):
        return 1 - len(A & B) / len(A | B)

    """
    Converts a vector (a list of 0s and 1s) into a set, where the values of the set are the indexes of the elements in
    the given list that have value 1.
    @param  {list} point     The list to be converted to a set
    """
    def __convert_vector_to_set(self, point):
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
        for point in D:
            point_as_set = self.__convert_vector_to_set(point)
            # list_sets.append(point_as_set) #--> uncommend this line if you want to have a GLOBAl list of the points as sets
            if self.__compute_distance(__P, point_as_set) <= eps:
                neighbourhood.append(point)
        return neighbourhood


Dbscan().start()
