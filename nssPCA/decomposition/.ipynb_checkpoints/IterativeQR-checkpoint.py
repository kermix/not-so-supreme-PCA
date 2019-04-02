from nssPCA.decomposition._base import BaseDecompostion as __BaseDecompostion

class IterativeQRDecomposition(__BaseDecompostion):
    def qr_decomposition(data, extract_vectors=False):
        X = data
        oMatrix = np.diag([1 for _ in range(data.shape[1])])
        while not np.allclose(X, np.triu(X)):
            Q, R = np.linalg.qr(X)
            oMatrix = np.dot(oMatrix, Q)
            X = np.dot(R, Q)
        diagonal = np.diagonal(X)
        
        self.eigen_vectors = self.extract_eigenvectors(oMatrix, len(diagonal))
        self.eigen_values = diagonal
        self.__sort_pairs()
        
        
    def transform(self, data):
        pass
       
        
    def inverse_transform(self, data):
        pass