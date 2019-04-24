import numpy as np

from nssPCA.decomposition._base import BaseDecompostion as __BaseDecompostion


class QRSVDecomposition(__BaseDecompostion):
    def fit(self, data: np.ndarray):
        """
        Performs decomposition of data matrix according to qrsvd decomposition algorithm introduced here:
        https://link-1springer-1com-1htv89mdl09c7.hansolo.bg.ug.edu.pl/article/10.1007/s13042-012-0131-7 .
        It is super fast for large matrixes over 1000x10 when using H*H^T covariance matrix.
        Uses numpy.linalg to achive the goal.

        :param data: (np.ndarray) Matrix to decomposition.
        """
        # perform decomposition
        Q, R = np.linalg.qr(data if not self.axis else data.T, mode='complete')
        U, S, V = np.linalg.svd(R.T)

        # s is singular values which is square root of eigenvalue.
        S *= S

        # generate ortogonal matrix according to article
        orthogonal_matrix = np.dot(Q, V.T)

        # svd returns only non-zero singular values so we have to add missing values corresponding
        # to number of eigen vectors
        zeros = np.zeros((orthogonal_matrix.shape[1] - len(S),))
        eigenvalues = np.concatenate((S, zeros))

        # extract eigen vectors from orthogonal matrix TODO: move to method of BaseDecompostion class
        eigen_vectors = []
        for i in range(len(eigenvalues)):
            eigen_vectors.append(orthogonal_matrix[:, i])
        self.components = np.array(eigen_vectors)
        
        self.eigen_values = np.array(eigenvalues)
        super(QRSVDecomposition, self)._sort_pairs()
