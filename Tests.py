import nssPCA.data as data
import nssPCA.decomposition as decomposition
import nssPCA.preprocessing as preprocessing

print("Witaj Świecie")  # TODO: help

yes_answers = ['T', 't', 'Y', 'y']
no_answers = ['N', 'n']

answers = yes_answers + no_answers

file_name = input("Proszę podać ścieżkę do pliku")

index_col = input("Podaj nazwę kolumny z indeksami wierszy: [Protein IDs] ")
index_col = index_col or "Protein IDs"

# file_name = '/home/mateusz/Pobrane/iris.csv'

matrix = data.Holder(file_name, index_col=index_col)

print("Wybór nazw kolumn zawierających dane do analizy: ")
print("\t 1. Intensity")
print("\t 2. Concentration")
print("\t 3. Własne wyrażenie regularne.")

filters = {"1": "^Intensity",
           "2": "^Concentration",
           "3": None}

choice = input("Twórj wybór: ")

while choice not in filters.keys():
    choice = input("Twój wybór: ")

if choice == "3":
    filters[choice] = input("Podaj wyrażenie regularne:").strip()

matrix.data = matrix.data.filter(regex=filters[choice])

center_data = input("Czy przeprowadzić centrowanie danych względem średniej? [T/n]").strip()

while center_data not in answers:
    center_data = input("Czy przeprowadzić centrowanie danych względem średniej? [T/n]").strip()

standarize_data = input("Czy przeskalować dane tak, aby wariancja w kolumnach wnosiła 1?[T/n]").strip()
while standarize_data not in answers:
    standarize_data = input("Czy przeskalować dane tak, aby wariancja w kolumnach wnosiła 1?").strip()

print("Indeksy wymiaru 0: {:<50}...".format(str(matrix.data.index.values)))  # TODO: do poprawy matrix.data
print("Indeksy wymiaru 1: {:<50}...".format(str(matrix.data.columns)))  # TODO: poprawy matrix.data

dimm_to_compress = input("Który z wymiarów poddać kompresji?").strip()
while dimm_to_compress not in ["0", "1"]:
    dimm_to_compress = input("Który z wymiarów poddać kompresji?").strip()
dimm_to_compress = int(dimm_to_compress)

valid_algorithms = {
    'eig': decomposition.EigenDecomposition(),
    'svd': decomposition.SVDecomposition(),
    'qrsvd': decomposition.QRSVDecomposition
}

print("Dostępne algorytmy dekompozycji:")
for alg in valid_algorithms.keys():
    print('\t{}'.format(alg))

algorithm = input("Proszę wybrać algorytm:").strip()
while algorithm not in valid_algorithms.keys():
    algorithm = input("Proszę wybrać algorytm: ").strip()

center_data = True if center_data in yes_answers else False
standarize_data = True if standarize_data in yes_answers else False  # TODO: rename

matrix = matrix.generate()

standarized_matrix = preprocessing.Scaler(calc_mean=center_data,
                                          calc_std=standarize_data,
                                          axis=0 if dimm_to_compress == 1 else 1).transform(matrix)

if algorithm == 'eig':
    cov_matrix = preprocessing.covariance(standarized_matrix, axis=dimm_to_compress)
    PCA = decomposition.EigenDecomposition(axis=dimm_to_compress)
    PCA.fit(cov_matrix)
    print("Ilość wyjaśnianej wariancji przez kolejne zmienne {}".format(PCA.explained_ratio))
    n_components = input("Ilu głównych składowych użyć do rzutowania?")  # TODO: co to ma byc?
    PCA.number_of_components = int(n_components)
    transformed = PCA.transform(standarized_matrix)
elif algorithm == 'svd':
    PCA = decomposition.SVDecomposition(axis=dimm_to_compress)
    PCA.fit(standarized_matrix)
    print("Ilość wyjaśnianej wariancji przez kolejne zmienne {}".format(PCA.explained_ratio))
    n_components = input("Ilu głównych składowych użyć do rzutowania?")  # TODO: co to ma byc?
    n_components = input("Ilu głównych składowych użyć do rzutowania?")  # TODO: co to ma byc?
    PCA.number_of_components = int(n_components)
    transformed = PCA.transform(standarized_matrix)
elif algorithm == 'svd':
    PCA = decomposition.QRSVDecomposition(axis=dimm_to_compress)
    PCA.fit(standarized_matrix)
    print("Ilość wyjaśnianej wariancji przez kolejne zmienne {}".format(PCA.explained_ratio))
    n_components = input("Ilu głównych składowych użyć do rzutowania?")  # TODO: co to ma byc?
    n_components = input("Ilu głównych składowych użyć do rzutowania?")  # TODO: co to ma byc?
    PCA.number_of_components = int(n_components)
    transformed = PCA.transform(standarized_matrix)

import numpy as np

np.savetxt("data.csv", transformed, delimiter=",")
