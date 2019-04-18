import numpy as np


class Scaler:
    def __init__(self,
                 calc_mean: bool = True,
                 calc_std: bool = True,
                 inplace: bool = False,
                 axis: int = 0):
        self.__calc_mean = calc_mean
        self.__calc_std = calc_std
        self.__inplace = inplace
        self.__axis = axis
        
        self.mean_vector = None
        self.std_vector = None

    @staticmethod
    def __mean(data: np.ndarray, axis: int):
        return np.mean(data, axis=axis)

    @staticmethod
    def __std(data: np.ndarray, axis: int):
        return np.std(data, axis=axis)

    def transform(self, data: np.ndarray):
        if self.__calc_mean:
            self.mean_vector = self.__mean(data, self.__axis)
        if self.__calc_std:
            self.std_vector = self.__std(data, self.__axis)
        
        if not self.__inplace: 
            result = np.full(data.shape, np.nan)

        if self.__axis == 0:
            for i in range(result.shape[1]):
                u = self.mean_vector[i] if self.__calc_mean else 0
                s = self.std_vector[i] if (self.__calc_std and self.std_vector[i] != 0) else 1

                if self.__inplace:
                    data[:, i] = (data[:, i] - u) / s
                else:
                    result[:, i] = (data[:, i] - u) / s
        else:
            for j in range(result.shape[0]):
                u = self.mean_vector[j] if self.__calc_mean else 0
                s = self.std_vector[j] if (self.__calc_std and self.std_vector[j] != 0) else 1

                if self.__inplace:
                    data[j] = (data[j] - u) / s
                else:
                    result[j] = (data[j] - u) / s

        if not self.__inplace:
            return result
            
        
class Squarer:
    def __init__(self, 
                 axis: int = 0):
        self.axis = axis

    def transform(self, 
                  data: np.ndarray):
        if self.axis:
            return np.dot(data.T, data)
        else:
            return np.dot(data, data.T)


def covariance(data: np.ndarray, axis: int = 0, biased: bool = True):
    return Squarer(axis=axis).transform(data) / (data.shape[axis] - (1 if biased else 0))
