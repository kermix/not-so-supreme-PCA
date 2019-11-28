import numpy as np

from nssPCA.decomposition._base import BaseDecompostion as __BaseDecompostion


class TruncatedSVDecomposition(__BaseDecompostion):
    def fit(self, data: np.ndarray):
        """
        Performs decomposition of data matrix according to svd decomposition algorithm. It is faster and numerically
        safer method, because it do not require calculating covariance matrix of data.
        Uses numpy.linalg to achive the goal.

        :param data: (np.ndarray) Matrix to decomposition.
        """
        # perform decomposition
        u, s, v = np.linalg.svd(data, full_matrices=False)

        # s is singular values which is square root of eigenvalue.
        s *= s

        # u of transposed v (depending on decomposiotion axis) is equal to orthogonal_matrix of covariance matrix
        # in eigen decomposition algorithm.
        orthogonal_matrix = u if not self.axis else v.T

        # svd returns only non-zero singular values so we have to add missing values corresponding
        # to number of eigen vectors
        zeros = np.zeros((orthogonal_matrix.shape[1] - len(s),))
        eigenvalues = np.concatenate((s, zeros))

        # extract eigen vectors from orthogonal matrix TODO: move to method of BaseDecompostion class
        eigen_vectors = []
        for i in range(len(eigenvalues)):
            eigen_vectors.append(orthogonal_matrix[:, i])
        self.components = np.array(eigen_vectors)

        self.eigen_values = np.array(eigenvalues)
        super(TruncatedSVDecomposition, self)._sort_pairs()
