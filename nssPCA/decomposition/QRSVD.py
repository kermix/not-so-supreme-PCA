from nssPCA.decomposition._base import BaseDecompostion as __BaseDecompostion

import numpy as np

class QRSVDecomposition(__BaseDecompostion):
    def fit(self, data):
        Q, R = np.linalg.qr(data if not self.axis else data.T, mode='complete')
        U, S, V = np.linalg.svd(R.T)
        S*=S
        oMatrix = np.dot(Q, V.T)
        zeros = np.zeros((oMatrix.shape[1]-len(S),))
        eigenvalues = np.concatenate((S, zeros))
        
        eigen_vectors = []
        for i in range(len(eigenvalues)):
            eigen_vectors.append(oMatrix[:,i])
        self.components = np.array(eigen_vectors)
        
        self.eigen_values = np.array(eigenvalues)
        super(QRSVDecomposition, self)._sort_pairs()