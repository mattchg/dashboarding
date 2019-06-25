# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 19:45:46 2019

@author: Matthew
"""


import numpy as np
import pandas as pd
import random

class KMeans:
    """performs k-means clustering"""
    def __init__ (self,k):
        self.k = k
        self.means = None
        self.errors = None
        self.clusters = None
        
    """Wraps the distance metric function so it can be called using map()"""
    def classify(self, input):
        means = np.array(self.means)
        value = np.array(input)
        distances = []
        for mean in means:
            distances.append(np.square(mean - value).sum())
        return distances.index(min(distances))
    def train(self, inputs):
        self.means = random.sample(inputs, self.k)
        self.errors = [0]*self.k
        assignments = None
        while True:
            new_assignments = list(map(self.classify,inputs))
            if assignments == new_assignments:
                return
            assignments = new_assignments
            cluster_indices = []
            for i in range(self.k):
                self.errors[i] = 0
                cluster = []
                indices = []
                for j,k in enumerate(assignments):
                    if k == i:
                        cluster.append(inputs[j])
                        indices.append(j)
                self.means[i] = np.mean(cluster,0)
                cluster_indices.append(indices)
                for clus in cluster:
                    self.errors[i] += np.sqrt(np.square(clus - self.means[i]).sum())
            self.clusters = cluster_indices