from nssPCA.decomposition._base import BaseDecompostion as __BaseDecompostion

class EigenDecomposition(__BaseDecompostion):
    def __check_symmetric(a, tol=1e-8):
        return np.allclose(a, a.T, atol=tol)
    
    
    def fit(self, data):
        if self.__check_symmetric(data):
            eigenvalues, oMatrix = np.linalg.eigh(data)
        else: 
            eigenvalues, oMatrix = np.linalg.eig(data)
            
        self.eigen_vectors = self.extract_eigenvectors(oMatrix, len(eigenvalues))
        self.eigen_values = eigenvalues
        self.__sort_pairs()
        
        
    def transform(self, data):
        pass
       
        
    def inverse_transform(self, data):
        pass