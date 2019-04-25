import numpy as np

from nssPCA.decomposition._base import BaseDecompostion as __BaseDecompostion


class EigenDecomposition(__BaseDecompostion):

    def fit(self, data: np.ndarray):
        """
        Performs decomposition of data matrix according to eigen decomposition algorithm.
        Uses numpy.linalg to achive goal.

        :param data: (np.ndarray) Matrix to decomposition.
        """

        # use proper decomposing according to numpy docs depending on matrix symetricity.
        if check_symmetric(data):
            eigenvalues, orthogonal_matrix = np.linalg.eigh(data)
        else:
            eigenvalues, orthogonal_matrix = np.linalg.eig(data)

        # extract eigen vectors from orthogonal matrix TODO: move to method of BaseDecompostion class
        eigen_vectors = []
        for i in range(len(eigenvalues)):
            eigen_vectors.append(orthogonal_matrix[:, i])
        self.components = np.array(eigen_vectors)
        
        self.eigen_values = np.array(eigenvalues)
        super(EigenDecomposition, self)._sort_pairs()


def check_symmetric(data: np.ndarray, tol: float = 1e-8) -> bool:
    """
    Checks if matrix is symmetric by comparing values of A and A.T matrix.
    
    :param data: (np.ndarray) Data to test for symmetricity.
    :param tol: (float) tolerance for comaring values.
    :return: (bool) True if matrix is symmetric.
    """
    return np.allclose(data, data.T, atol=tol)
