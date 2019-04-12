import numpy as np
import pandas as pd

class Scaler:
    def __init__(self, 
                 calc_mean: bool = True,
                 calc_std: bool = True,
                 inplace: bool = False):
        self.__calc_mean = calc_mean
        self.__calc_std = calc_std
        self.__inplace = inplace
        
        self.mean_vector = None
        self.std_vector = None
    
    
    @staticmethod
    def __mean(data: np.ndarray):
        return np.mean(data, axis=0)
    
    
    @staticmethod
    def __std(data: np.ndarray):
        return np.std(data, axis=0)
     
        
    def transform(self, data: np.ndarray):
        if self.__calc_mean:
            self.mean_vector = self.__mean(data)
        if self.__calc_std:
            self.std_vector = self.__std(data)
        
        if not self.__inplace: 
            result = np.full((data.shape), np.nan)
        
        for index, x in np.ndenumerate(data):
            row_index, column_index = index[0], index[1]
            u = self.mean_vector[column_index] if self.__calc_mean else 0
            s = self.std_vector[column_index] if self.__calc_std else 1
            
            if self.__inplace:
                data[row_index][column_index] = (data[row_index][column_index] - u) / s
            else:
                result[row_index][column_index] = (data[row_index][column_index] - u) / s
        
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
       
    
class Covariance:
    def __init__(self):
        pass
    
    @staticmethod
    def transform(data: np.ndarray, biased: bool = True):
        return np.cov(data, bias=biased)