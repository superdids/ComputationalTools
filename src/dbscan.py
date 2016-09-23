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

    def __jaccard_distance(self, p1, p2):
        return (p1 & p2) / (p1 | p2)


    def __region_query(self, D, P, eps):
        neighbours = [None] * 0
        row = len(P)
        for i in range(row):
            if i != P:
                if self.__jaccard_distance(D[i][P[1]], P) <= eps:
                    neighbours.append(i)
        return neighbours


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


