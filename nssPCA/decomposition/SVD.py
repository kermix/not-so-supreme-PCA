from nssPCA.decomposition._base import BaseDecompostion as __BaseDecompostion

import numpy as np

class SVDecomposition(__BaseDecompostion):
    def fit(self, data):
        u,s,v = np.linalg.svd(data)
        s*=s
        oMatrix = u if not self.axis else v.T
        zeros = np.zeros((oMatrix.shape[1]-len(s),))
        eigenvalues = np.concatenate((s, zeros))
         
        eigen_vectors = []
        for i in range(len(eigenvalues)):
            eigen_vectors.append(oMatrix[:,i])
        self.components = np.array(eigen_vectors)
        
        self.eigen_values = np.array(eigenvalues)
        super(SVDecomposition, self)._sort_pairs()