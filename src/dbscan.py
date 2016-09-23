import numpy as np
import pandas as pd
from pandas import Series, DataFrame, Index
import scipy.sparse as ss
import pickle

class Dbscan:

    #visited? noisy
    __point_information = dict()

    #__point_information['0'] = {'visited': 1, 'noise': 0}


    def start(self):
        data = '../files/data_10points_10dims.dat'
        small_set = pickle.load(open(data, 'rb'), encoding='latin1')
        matr = ss.csr_matrix(small_set).todense()

        print(matr)

    def __set_point_information(self, P, visited=None, noise=None):
        if not self.__point_information[P]:
            self.__point_information[P] = { 'visited': 0, 'noise': 0}
        if visited != None:
            self.__point_information[P]['visited'] = visited
        if noise != None:
            self.__point_information[P]['noise'] = noise

    def __is_visited(self, P):
        point_information = self.__point_information(P)
        return point_information and point_information['visited'] == 1

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
                ++current_cluster
                C[current_cluster] = list()
                C[current_cluster] = self.__expand_cluster(D, current_index, P, neighbor_points, C[current_cluster], eps, min_pts)


        self.__point_information = dict()




    def __expand_cluster(self, D, start_at, P, neighbor_points, current_cluster, eps, min_pts):

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


'''

    expandCluster(P, NeighborPts, C, eps, MinPts) {
   add P to cluster C
   for each point P' in NeighborPts {
      if P' is not visited {
         mark P' as visited
         NeighborPts' = regionQuery(P', eps)
         if sizeof(NeighborPts') >= MinPts
            NeighborPts = NeighborPts joined with NeighborPts'
      }
      if P' is not yet member of any cluster
         add P' to cluster C
   }
}

expandCluster(P, NeighborPts, C, eps, MinPts) {
   add P to cluster C
   for each point P' in NeighborPts {
      if P' is not visited {
         mark P' as visited
         NeighborPts' = regionQuery(P', eps)
         if sizeof(NeighborPts') >= MinPts
            NeighborPts = NeighborPts joined with NeighborPts'
      }
      if P' is not yet member of any cluster
         add P' to cluster C
   }
}

DBSCAN(D, eps, MinPts) {
   C = 0
   for each point P in dataset D {
      if P is visited
         continue next point
      mark P as visited
      NeighborPts = regionQuery(P, eps)
      if sizeof(NeighborPts) < MinPts
         mark P as NOISE
      else {
         C = next cluster
         expandCluster(P, NeighborPts, C, eps, MinPts)
      }
   }
}

dist(P,x) <= eps -> append to neighbourhood

regionQuery(D, P, eps)
    'distance measure function is used here. '
   return all points within P's eps-neighborhood (including P)
'''


