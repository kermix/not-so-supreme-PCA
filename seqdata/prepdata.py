import pandas as pd
import re
import csv

def sane_data(in_dir, out_dir):
    data = ''
    with open(in_dir, 'r') as file:
        regex = re.compile(r'(?:(?=[^\r\n])\s+)')
        for line in file.readlines()[1:]:
            data += re.sub(regex, ' ', line)
    with open(out_dir, 'w') as saned_matrix:
        saned_matrix.write(data)
        matrix = pd.read_csv(out_dir, sep=" ", index_col=0, header=None)
        matrix.columns = matrix.index.values
        matrix.to_csv(out_dir, header=True)

if __name__ == "__main__":
    sane_data('/home/mateusz/pca/dist.mat', "/home/mateusz/pca/saned_dist_mat.csv")


