import numpy as np

from nssPCA.decomposition._base import BaseDecompostion as _BaseDecompostion


class QRSVDecomposition(_BaseDecompostion):
    def __init__(self, axis: int = 1):
        _BaseDecompostion.__init__(self, axis)

        self.__Q = None
        self.__V = None
        self.__S = None
        self.__number_of_components = None

    def calc_orthogonal_matrix(self):
        return np.dot(self.__Q, self.__V[:, :self.number_of_components])

    def fit(self, data: np.ndarray):
        """
        Performs decomposition of data matrix according to qrsvd decomposition algorithm introduced here:
        https://link-1springer-1com-1htv89mdl09c7.hansolo.bg.ug.edu.pl/article/10.1007/s13042-012-0131-7 .
        It is super fast for large matrixes over 1000x10 when using H*H^T covariance matrix.
        Uses numpy.linalg to achive the goal.

        :param data: (np.ndarray) Matrix to decomposition.
        """
        # perform decomposition
        self.__Q, r = np.linalg.qr(data if not self.axis else data.T, mode='complete')
        u, self.__S, self.__V = np.linalg.svd(r.T)

        # s is singular values which is square root of eigenvalue.
        self.__S *= self.__S

        # generate ortogonal matrix according to article
        orthogonal_matrix = self.calc_orthogonal_matrix()

        # svd returns only non-zero singular values so we have to add missing values corresponding
        # to number of eigen vectors
        zeros = np.zeros((orthogonal_matrix.shape[1] - len(self.__S),))
        eigenvalues = np.concatenate((self.__S, zeros))

        # extract eigen vectors from orthogonal matrix TODO: move to method of BaseDecompostion class
        eigen_vectors = []
        for i in range(len(eigenvalues)):
            eigen_vectors.append(orthogonal_matrix[:, i])
        self.components = np.array(eigen_vectors)
        
        self.eigen_values = np.array(eigenvalues)
        super(QRSVDecomposition, self)._sort_pairs()

    @property
    def number_of_components(self) -> int:
        """
        :return: (int) Actual number of PCs to use for PCA.
        """
        return self.__number_of_components

    @number_of_components.setter
    def number_of_components(self, value: int):
        """
        Sets number of PCs to use for PCA.
        :param value: (int) Number of PCs to use for PCA. For example no. components
        explaining over 90% of variance in data set.
        """
        self.__number_of_components = value  # TODO: find better solution

        orthogonal_matrix = self.calc_orthogonal_matrix()
        no_zeros = (orthogonal_matrix.shape[1] - len(self.__S))
        zeros = np.zeros((no_zeros,) if (no_zeros > 0) else (0,))
        eigenvalues = np.concatenate((self.__S, zeros))

        eigen_vectors = []
        for i in range(len(eigenvalues)):
            if i < orthogonal_matrix.shape[1]:
                eigen_vectors.append(orthogonal_matrix[:, i])
        self.components = np.array(eigen_vectors)

        self.eigen_values = np.array(eigenvalues)
        super(QRSVDecomposition, self)._sort_pairs()
