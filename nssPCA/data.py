import os

import numpy as np
import pandas as pd

_read_methods = {
    'csv': pd.read_csv,
    'xls': pd.read_excel,
    'xlsx': pd.read_excel
}


class Holder:
    """

    Container for a data

    """

    def __init__(self, file_name: str, **kwargs):

        """

        Initiates object containing data as pandas.DataFrame. Gets the same arguments like pandas.read_csv and
        pandas.read_xlsx.Uses proper function depending on file extension.

        :param file_name: (string) Absolute file directory.
        :param kwargs: keyworded arguments compatible with pandas read functions.

        """

        file_name = file_name.strip()

        if os.path.exists(os.path.dirname(file_name)):
            extension = file_name.split('.')[-1].lower()

            if extension in _read_methods.keys():
                self.data = _read_methods[extension](file_name, **kwargs)
            else:
                raise IOError("Bad file extension: {}. Supported file extensions are {}".format(extension,
                                                                                                _read_methods.keys()))
        else:
            raise IOError("File not found")

    def generate(self) -> np.ndarray:
        """

        Extracts numeric data from data frame.

        :return: (numpy.ndarray) numeric data from DataFrame

        """
        return self.data.select_dtypes(include=[np.number]).values

# TODO: move to functions
