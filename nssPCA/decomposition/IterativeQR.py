from nssPCA.decomposition._base import BaseDecompostion as __BaseDecompostion

import numpy as np

class IterativeQRDecomposition(__BaseDecompostion):
    def fit(self, data):
        X = data
        oMatrix = np.diag([1 for _ in range(data.shape[1])])
        while not np.allclose(X, np.triu(X)):
            Q, R = np.linalg.qr(X)
            oMatrix = np.dot(oMatrix, Q)
            X = np.dot(R, Q)
        eigenvalues = np.diagonal(X)
        
        eigen_vectors = []
        for i in range(len(eigenvalues)):
            eigen_vectors.append(oMatrix[:,i])
        self.components = np.array(eigen_vectors)
    
        self.eigen_values = np.array(eigenvalues)
        super(IterativeQRDecomposition, self)._sort_pairs()