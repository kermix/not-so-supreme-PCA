from nssPCA.decomposition._base import BaseDecompostion as __BaseDecompostion

import numpy as np


class EigenDecomposition(__BaseDecompostion):
    @staticmethod
    def __check_symmetric(a, tol=1e-8):
        return np.allclose(a, a.T, atol=tol)

    def fit(self, data):  # wymiar zależy od wywolania np.cov(X[, y])
        if self.__check_symmetric(data):
            eigenvalues, oMatrix = np.linalg.eigh(data)
        else: 
            eigenvalues, oMatrix = np.linalg.eig(data)
            
        eigen_vectors = []
        for i in range(len(eigenvalues)):
            eigen_vectors.append(oMatrix[:,i])
        self.components = np.array(eigen_vectors)
        
        self.eigen_values = np.array(eigenvalues)
        super(EigenDecomposition, self)._sort_pairs()
