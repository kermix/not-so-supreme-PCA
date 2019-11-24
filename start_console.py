import os
import threading

import numpy as np
import pandas as pd

import nssPCA.data as data
import nssPCA.decomposition as decomposition
import nssPCA.preprocessing as preprocessing
from cli_plot import plot as plt
from misc import get_free_port_number

yes_answers = ['T', 't', 'Y', 'y']
no_answers = ['N', 'n']

answers = yes_answers + no_answers


def start_cli(input_, output, index, columns, regcolumns, groupcolumns, center, standarize, axis, algorithm,
              n_components, plot):
    file_name = input_ or input("Proszę podać ścieżkę do pliku:").strip()

    index_col = index or input("Podaj nazwę kolumny z indeksami wierszy lub \"*\", "
                               "aby użyć domyślnych indeksów: [Protein IDs] ").strip() or "Protein IDs"

    index_col = None if index_col == "*" else index_col

    matrix = data.read_data(file_name, index_col=index_col)

    print("Wybór nazw kolumn zawierających dane do analizy:")
    print("\t 1. All")
    print("\t 2. Intensity")
    print("\t 3. Concentration")

    filters = {"1": r"^(.*)$",
               "2": r"^Intensity(?:\s(?:P|F)\d){2}$",
               "3": r"^Concentration(?:\s(?:P|F)\d){2}$"}

    if not columns and not regcolumns:
        choice = input("Twój wybór: [1] ").strip() or "1"

        while choice not in filters.keys():
            choice = input("Twój wybór: [1] ").strip() or "1"
    elif regcolumns:
        choice = '4'
        filters['4'] = regcolumns
    elif columns:
        choice = str(columns)

    filtered_matrix = matrix.filter(regex=filters[choice])

    for error in data.get_invalid_data(filtered_matrix):
        print('Invalid value in: {}'.format(error))

    if groupcolumns:
        groups = [group.split(',') for group in groupcolumns]
        grouped_data = pd.DataFrame(index=matrix.data.index)
        for group in groups:
            grouped_data[', '.join(group)] = matrix.data[group].mean(axis=1)
        filtered_matrix = grouped_data

    if center is None:
        center_data = input("Czy przeprowadzić centrowanie danych względem średniej? [T/n]").strip() or "T"

        while center_data not in answers:
            center_data = input("Czy przeprowadzić centrowanie danych względem średniej? [T/n]").strip() or "T"
    else:
        center_data = center

    if standarize is None:
        standarize_data = input("Czy przeskalować dane tak, aby wariancja w kolumnach wnosiła 1? [T/n]").strip() or "T"

        while standarize_data not in answers:
            standarize_data = input(
                "Czy przeskalować dane tak, aby wariancja w kolumnach wnosiła 1? [T/n]").strip() or "T"
    else:
        standarize_data = standarize

    if axis is None:
        print("Indeksy wymiaru 0: {}...".format(str(list(filtered_matrix.index.values))[:50]))
        print("Indeksy wymiaru 1: {}...".format(str(list(filtered_matrix.columns))[:50]))

        dimm_to_compress = input("Który z wymiarów poddać kompresji? [1] ").strip() or "1"
        while dimm_to_compress not in ["0", "1"]:
            dimm_to_compress = input("Który z wymiarów poddać kompresji? [1] ").strip() or "1"
        dimm_to_compress = int(dimm_to_compress)
    else:
        dimm_to_compress = axis

    valid_algorithms = {
        'eig': decomposition.EigenDecomposition(),
        'svd': decomposition.SVDecomposition(),
        'qrsvd': decomposition.QRSVDecomposition
    }

    if algorithm is None:
        print("Dostępne algorytmy dekompozycji:")
        for alg in valid_algorithms.keys():
            print('\t{}'.format(alg))

        algorithm = input("Proszę wybrać algorytm: [eig] ").strip() or "eig"
        while algorithm not in valid_algorithms.keys():
            algorithm = input("Proszę wybrać algorytm: [eig] ").strip() or "eig"
    else:
        algorithm = algorithm

    num_matrix = data.generate(filtered_matrix).values

    scaler = preprocessing.Scaler(calc_mean=center_data,
                                  calc_std=standarize_data,
                                  axis=0 if dimm_to_compress == 1 else 1)

    standarized_matrix = scaler.transform(num_matrix)
    standarized_matrix = pd.DataFrame(standarized_matrix,
                                      index=filtered_matrix.index,
                                      columns=filtered_matrix.columns)

    if algorithm == 'eig':
        cov_matrix = preprocessing.covariance(standarized_matrix, axis=dimm_to_compress)
        PCA = decomposition.EigenDecomposition(axis=dimm_to_compress)
        PCA.fit(cov_matrix)
    elif algorithm == 'svd':
        PCA = decomposition.SVDecomposition(axis=dimm_to_compress)
        PCA.fit(standarized_matrix)
    elif algorithm == 'qrsvd':
        PCA = decomposition.QRSVDecomposition(axis=dimm_to_compress)
        PCA.fit(standarized_matrix)

    if n_components is None:
        with np.printoptions(precision=5, suppress=True):
            print("Ilość wyjaśnianej wariancji przez kolejne zmienne {}".format(PCA.explained_ratio))

        n_components = input("Ilu głównych składowych użyć do rzutowania? [{}]".format(len(PCA.components))) \
                       or str(len(PCA.components))
    else:
        n_components = n_components

    PCA.number_of_components = int(n_components)
    transformed = PCA.transform(standarized_matrix)

    result = pd.DataFrame(transformed,
                          index=filtered_matrix.index if dimm_to_compress else filtered_matrix.columns,
                          columns=["".join(("PC", str(i + 1))) for i in range(int(n_components))])

    if output is None:
        output = './'
    matrix.to_csv(os.path.join(output, "original_data.csv"))
    filtered_matrix.to_csv(os.path.join(output, "filtered_data.csv"))

    columns = standarized_matrix.columns if axis else standarized_matrix.index
    pd.DataFrame(scaler.mean_vector, index=columns).to_csv(os.path.join(output, 'mean.csv'))
    pd.DataFrame(scaler.std_vector, index=columns).to_csv(os.path.join(output, 'std.csv'))

    standarized_matrix.to_csv(os.path.join(output, 'normalized_data.csv'))

    columns = ["".join(("PC", str(i))) for i in range(1, int(len(PCA.explained_ratio)) + 1)]
    pd.DataFrame(PCA.explained_ratio, index=columns).to_csv(os.path.join(output, 'variance.csv'))
    pd.DataFrame(PCA.eigen_values, index=columns).to_csv(os.path.join(output, 'eigenvalues.csv'))

    columns = standarized_matrix.columns
    index = ["".join(("PC", str(i))) for i in range(1, int(len(PCA.components)) + 1)]
    pd.DataFrame(PCA.components, index=index, columns=columns).to_csv(os.path.join(output, 'eigenvectors.csv'))

    result.to_csv(os.path.join(output, "transformed_data.csv"))

    if plot:
        port = get_free_port_number()

        threading.Thread(target=plt, args=(port, result), daemon=False).start()

if __name__ == "__main__":
    print("Start program using run.py")
