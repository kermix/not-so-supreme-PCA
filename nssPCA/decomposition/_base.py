import numpy as np
import pandas as pd

class BaseDecompostion:
    def __init__(self, axis=0):
        self.__axis = axis
        
        self.eigen_vectors = None
        self.eigen_values = None

        
    @property
    def explained_ratio(self):
        sum_of_evals = sum(eigen_values)
        return np.array([x/sum_of_evals for x in eigenvalues])
    
    
    @explained_ratio.setter
    def explained_ratio(self, arg):
        pass
     
        
    @staticmethod
    def __extract_eigenvectors(v):
        V = []
        for i in range(n_eigenvectors) if n_eigenvectors else range(len(v)):
            V.append(v[:,i])
        return np.array(V)

    
    def __sort_pairs(self):
        eigenpairs = [(self.eigen_values[i], self.eigen_values[i]) for i in range(len(self.eigen_values))]
        eigenpairs.sort(key=lambda eigpair: eigpair[0], reverse=True)
        
        eigenvalues, eigenvectors = [], []
        
        for eigenpair in eigenpairs:
            eigenvalues.append(eigenpair[0])
            eigenvectors.append(np.array(eigenpair[1]))
            
        self.eigen_values = eigenvalues
        self.eigen_vectors = eigen_vectors
       
    
    def set_n_of_components(self, n):
        self.eigen_vectors = self.eigen_vectors[:n]
        self.eigen_values = self.eigen_values[:n]
    
    
    def fit(self, data):
        pass
      
        
    def transform(self, data):
        pass
       
        
    def inverse_transform(self, data):
        pass
    
    
    #dodać wpływ self.axis na fit/transform/inverse_transform
    