from typing import Union

import numpy as np


class Scaler:
    def __init__(self,
                 calc_mean: bool = True,
                 calc_std: bool = True,
                 inplace: bool = False,
                 axis: int = 0):
        """

        Initializes and configures object to Z-normalize data.

        :param calc_mean: (bool) True to calculate mean vector of data. If False mean is set to 0.
        :param calc_std: (bool)  True to calculate standard deviation of data. If False standard deviation is set to 1
        :param inplace: (bool)  False to create new object with standardized data.
        :param axis: (int)      Axis to standardized over.

        """
        self.__calc_mean = calc_mean
        self.__calc_std = calc_std
        self.__inplace = inplace
        self.__axis = axis

        self.__mean_vector = None
        self.__std_vector = None

    @property
    def mean_vector(self):
        return self.__mean_vector

    @property
    def std_vector(self):
        return self.__std_vector

    @staticmethod
    def __mean(data: np.ndarray, axis: int) -> np.ndarray:
        return np.mean(data, axis=axis)

    @staticmethod
    def __std(data: np.ndarray, axis: int) -> np.ndarray:
        return np.std(data, axis=axis)

    def transform(self, data: np.ndarray) -> Union[np.ndarray, None]:
        """

        Applies custom Z-normalization according to object configuration.

        :param data: (np.ndarray) Data to transform

        :return: (np.ndarray) If self.__inplace is not set returns Z-normalised data.

        """
        if self.__calc_mean:
            self.__mean_vector = self.__mean(data, self.__axis)
        if self.__calc_std:
            self.__std_vector = self.__std(data, self.__axis)
        
        if not self.__inplace: 
            result = np.full(data.shape, np.nan)

        if self.__axis == 0:
            for j in range(data.shape[1]):

                # set u as mean  and s as standard deviation of j-th column of data
                u = self.__mean_vector[j] if self.__calc_mean else 0
                s = self.__std_vector[j] if (self.__calc_std and self.__std_vector[j] != 0) else 1

                # apply Z-normalization
                if self.__inplace:
                    data[:, j] = (data[:, j] - u) / s
                else:
                    result[:, j] = (data[:, j] - u) / s
        else:
            for i in range(data.shape[0]):

                # set u as mean  and s as standard deviation of i-th row of data
                u = self.__mean_vector[i] if self.__calc_mean else 0
                s = self.__std_vector[i] if (self.__calc_std and self.__std_vector[i] != 0) else 1

                # apply Z-normalization
                if self.__inplace:
                    data[i] = (data[i] - u) / s
                else:
                    result[i] = (data[i] - u) / s

        if not self.__inplace:
            return result
            
        
class Squarer:
    def __init__(self, 
                 axis: int = 0):
        """

        Initialises object for data symmetrizing.

        :param axis: (int) Axis to symmetrize over.

        """
        self.axis = axis

    def transform(self,
                  data: np.ndarray) -> np.ndarray:
        """
        Applies symmetrization on data with n rows and p columns.

        :param data: (np.ndarray) Data to symmetrize.

        :return:
        """

        if self.axis:
            return np.dot(data.T, data)  # p x p matrix
        else:
            return np.dot(data, data.T)  # n x n matrix


def covariance(data: np.ndarray, axis: int = 0, biased: bool = True) -> np.ndarray:
    """

    Calculates covariance matrix of data. For n x p matrix if axis == 0 result is n x n else p x p.

    :param data: (np.ndarray) Data to calculate covariance matrix.
    :param axis: (int) Axis to calculate covariance matrix over.
    :param biased: (bool) Use Bessel's correction. (A*A^T)/(N-1) instead (A*A^T)/N.

    :return: (np.ndarray) Covariance matrix.

    """
    return Squarer(axis=axis).transform(data) / (data.shape[0 if axis else 1] - (1 if biased else 0))

# TODO: add calculating covariance matrix as part of eigen decomposition fitting
