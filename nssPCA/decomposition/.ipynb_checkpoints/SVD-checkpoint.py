from nssPCA.decomposition._base import BaseDecompostion as __BaseDecompostion

class SVDecomposition(__BaseDecompostion):
    def fit(self, data, gen_HHtransposed=False):
        u,s,v = np.linalg.svd(data)
        s*=s
        oMatrix = u if gen_HHtransposed else v.T
        zeros = np.zeros((oMatrix.shape[1]-len(s),))
        diagonal = np.concatenate((s, zeros))
        
        self.eigen_vectors = self.extract_eigenvectors(oMatrix, len(diagonal))
        self.eigen_values = diagonal
        self.__sort_pairs()
        
        
    def transform(self, data):
        pass
       
        
    def inverse_transform(self, data):
        pass