import numpy as np


class BaseDecompostion:
    def __init__(self, axis=1):
        self.axis = axis
        
        self.components = None
        self.eigen_values = None
        
        self.__number_of_components = None

    @property
    def explained_ratio(self):
        sum_of_evals = sum(self.eigen_values)
        return np.array([x/sum_of_evals for x in self.eigen_values])

    @explained_ratio.setter
    def explained_ratio(self, arg):
        pass
    
    @property
    def number_of_components(self):
        return self.__number_of_components
    
    @number_of_components.setter
    def number_of_components(self, value):
        self.__number_of_components = value
    
    def _sort_pairs(self):
        eigenpairs = [(self.eigen_values[i], self.components[i]) for i in range(len(self.eigen_values))]
        eigenpairs.sort(key=lambda eigpair: eigpair[0], reverse=True)
        
        eigenvalues, components = [], []
        
        for eigenpair in eigenpairs:
            eigenvalues.append(eigenpair[0])
            components.append(np.array(eigenpair[1]))
            
        self.eigen_values = np.array(eigenvalues)
        self.components = np.array(components)

    def fit(self, data):
        pass
      
    def transform(self, data):
        if self.axis:
            return np.dot(data, self.components[:self.number_of_components].T)
        else:
            return np.dot(data.T, self.components[:self.number_of_components].T)

    def inverse_transform(self, transformed_data):
        if self.axis:
            return np.dot(transformed_data, self.components[:self.number_of_components])
        else:
            return np.dot(transformed_data.T, self.components[:self.number_of_components])
