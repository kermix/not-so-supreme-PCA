import base64
import io
import os

import numpy as np
import pandas as pd

_read_methods = {
    'csv': pd.read_csv,
    'xls': pd.read_excel,
    'xlsx': pd.read_excel
}


def read_data(file_name: str, buffer=None, **kwargs) -> pd.DataFrame:
    """

    Reads data from buffer or fileas pandas.DataFrame. Gets the same arguments like pandas.read_csv and
    pandas.read_xlsx.Uses proper function depending on file extension.

    :param file_name: (string) Absolute file directory.
    :param buffer: ioBuffer of file to load
    :param kwargs: keyworded arguments compatible with pandas read functions.

    :return: (pd.DataFrame) Pandas DataFrame with data from buffer or file.



    """

    file_name = file_name.strip()

    extension = file_name.split('.')[-1].lower()

    if extension in _read_methods.keys():
        if not buffer:
            if os.path.exists(os.path.dirname(file_name)):
                data = _read_methods[extension](file_name, **kwargs)
            else:
                raise IOError("File not found")
        else:
            decoded = base64.b64decode(buffer)
            if 'csv' == extension:
                buffer = io.StringIO(decoded.decode('utf-8'))
            elif extension in ['xls', 'xlsx']:
                buffer = io.BytesIO(decoded)
            data = _read_methods[extension](buffer, **kwargs)
    else:
        raise IOError("Bad file extension: {}. Supported file extensions are {}. ".format(extension,
                                                                                          _read_methods.keys()))

    return data


def generate(data: pd.DataFrame) -> np.ndarray:
    """

    Extracts numeric data from data frame.

    :return: (numpy.ndarray) numeric data from DataFrame

    """
    # TODO tests
    return data.apply(pd.to_numeric, errors='coerce')


def get_invalid_data(data: pd.DataFrame) -> list:
    # TODO docs and tests
    invalid_tuples = []
    for _, r in data.iterrows():
        if r.isnull().values.any():
            invalid_tuples.append(
                {str(r.name): str(r.index[r.isna()].tolist())})
    return invalid_tuples
