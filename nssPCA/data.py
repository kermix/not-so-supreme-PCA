import os

import numpy as np
import pandas as pd

_read_methods = {
    'csv': pd.read_csv,
    'xls': pd.read_excel,
    'xlsx': pd.read_excel
}


class Holder:
    def __init__(self, file_name, **kwargs):
        file_name = file_name.strip()

        if os.path.exists(os.path.dirname(file_name)):
            extension = file_name.split('.')[-1].lower()

            if extension in _read_methods.keys():
                self.data = _read_methods[extension](file_name, **kwargs)
            else:
                raise IOError("Bad file extension: {}. Suppored file extensions are {}".format(extension,
                                                                                               _read_methods.keys()))
        else:
            raise IOError("File not found")

    def generate(self):
        return self.data.select_dtypes(include=[np.number]).values
