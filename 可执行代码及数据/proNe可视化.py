import numpy as np
import networkx as nx

import scipy.sparse
from scipy import io
import scipy.sparse as sp
from scipy import linalg
from scipy.special import iv
from sklearn import preprocessing
from sklearn.utils.extmath import randomized_svd
import argparse
import time

matrix = io.mmread('../source_link.mtx')
result = []
with open('./emb/blogcatalog.emb','r+') as f:
    for i in f:
        line = [float(k.strip()) for k in i.split(' ')]
        if len(line) == 3 :
            result.append([line[1],line[2]])
result = np.array(result)
import networkx as nx
import matplotlib.pyplot as plt
G = nx.from_scipy_sparse_matrix(matrix)
# nx.draw_networkx(G, result)
# plt.axis('off')
# plt.show()
nx.draw(G, result, node_size=8)
plt.tight_layout()
plt.savefig("Graph.png", node_size=0.0001,width=0.000001,format="PNG",node_color = 'b',edge_color = 'r')
plt.show()