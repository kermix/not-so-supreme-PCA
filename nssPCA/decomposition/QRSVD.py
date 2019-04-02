from nssPCA.decomposition._base import BaseDecompostion as __BaseDecompostion

class QRSVDecomposition(__BaseDecompostion):
    def qrsvd_decomposition(data, gen_HHtransposed=False):
        Q, R = np.linalg.qr(data if gen_HHtransposed else data.T)
        U, S, V = np.linalg.svd(R.T)
        S*=S
        oMatrix = np.dot(Q, V.T)
        zeros = np.zeros((oMatrix.shape[1]-len(S),))
        diagonal = np.concatenate((S, zeros))
        
        self.eigen_vectors = self.extract_eigenvectors(oMatrix, len(diagonal))
        self.eigen_values = diagonal
        self.__sort_pairs()
      
    
    def transform(self, data):
        pass
       
        
    def inverse_transform(self, data):
        pass