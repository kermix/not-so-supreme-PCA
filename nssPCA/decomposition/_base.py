import numpy as np


class BaseDecompostion:
    def __init__(self, axis: int = 1):
        """

        Initializes and configures object to perform PCA. This is base class which provides vital features for PCA.
        Child classes overloads BaseDecompositon.fit() method acording to their algorithms.

        :param axis: (int) Axis to perform PCA over.

        """
        self.axis = axis
        
        self.components = None
        self.eigen_values = None
        
        self.__number_of_components = None

    @property
    def explained_ratio(self) -> np.ndarray:
        """

        Calculates explained variance in percents for each principal component. Sum is equal to 1.

        :return: (np.ndarray) Array containg percent of explained variance for PC in the same order as PCs.

        """
        sum_of_evals = sum(self.eigen_values)
        return np.array([x/sum_of_evals for x in self.eigen_values])
    
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
        self.__number_of_components = value
    
    def _sort_pairs(self):
        """
        Sorts eigenvalues with corresponding eigenvectors in decreasing order of eigenvalues.
        """

        # create pairs of eigenvalue and corresponding eigenvalue and sort in decreasing order of eigen values
        eigenpairs = sorted(zip(self.eigen_values, self.components),
                            key=lambda eigpair: eigpair[0], reverse=True)

        # split pairs to eigenvalues and eigenvectors
        eigenvalues, components = [], []
        
        for eigenpair in eigenpairs:
            eigenvalues.append(eigenpair[0])
            components.append(np.array(eigenpair[1]))
            
        self.eigen_values = np.array(eigenvalues)
        self.components = np.array(components)

    def fit(self, data: np.ndarray):
        """
        Method to overload by child classes according to their algorithms. Performs decomposition of matrix.

        :param data: (np.ndarray) Data matrix to decompose.
        """
        pass

    def transform(self, data: np.ndarray) -> np.ndarray:
        """
        Applies PCA transformation. Compresses matrix from n x p dimmensions to n x self.number_of_components
        self.number_of_components x p.

        :param data: (np.ndarray) Data which was used to fit model to preform transformation on it.

        :return: (np.ndarray) Data set with reduced dimmensionality.
        """
        if self.axis:
            return np.dot(data, self.components[:self.number_of_components].T)  # n x self.number_of_components
        else:
            return np.dot(data.T, self.components[:self.number_of_components].T)  # self.number_of_components x p

    def inverse_transform(self, transformed_data):
        """
        Inverses applied on data set transformation. NOT TESTED.

        :param transformed_data: (np.ndarray) Data set after transformation.

        :return: Data set with restored full dimmensionality.
        """
        if self.axis:
            return np.dot(transformed_data, self.components[:self.number_of_components])
        else:
            return np.dot(transformed_data.T, self.components[:self.number_of_components])
