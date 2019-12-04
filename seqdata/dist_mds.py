import nssPCA.data as data
import seqdata.data as sdata
import seqdata.plot as plot

import pandas as pd
import plotly.graph_objects as go
from sklearn.manifold import MDS
from sklearn.cluster import KMeans

N_COMPONENTS = 3
N_CLUSTERS = 7

matrix = sdata.read_distance_matrix('/home/mateusz/pca/dist.mat')
num_matrix = data.generate(matrix).values

emb = MDS(n_components=N_COMPONENTS, dissimilarity='precomputed')
transformed = emb.fit_transform(matrix)

result = pd.DataFrame(transformed,
                      index=matrix.index,
                      columns=["".join(("PC", str(i + 1))) for i in range(1, N_COMPONENTS+1)])

y_pred = KMeans(n_clusters=N_CLUSTERS).fit_predict(transformed)


if N_COMPONENTS == 3:
    plot.plot3d(transformed, y_pred, matrix.index)
else:
    plot.plot2d_subplots(transformed, y_pred, matrix.index)
