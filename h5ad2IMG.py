# preprocess.py
#!/usr/bin/env	python3

""" data preprocessing using pytorch

author YaZhang
"""

import numpy as np
import scanpy as sc
from PIL import Image
import time
import os


start_time = time.gmtime()
print(time.strftime('%Y-%m-%d %H:%M:%S', start_time))

adata = sc.read_h5ad('h5ad_filepath')
print(adata.obs['dataname'].unique())
print(adata.obs['cell_groups'].unique())
print(adata.n_obs)
print(adata.n_vars)

def normalization(data):
    _range = np.max(data) - np.min(data)
    print(np.max(data))
    print(np.min(data))
    print(_range)
    return (data - np.min(data)) / _range*255
X1 = adata.X
X1 = normalization(X1)
adata.X = X1


for i in adata.obs['dataname'].unique():
    adata_i = adata[adata.obs['dataname'] == i, :]
    for j in adata.obs['cell_groups'].unique():
        adata_ij = adata_i[adata_i.obs['cell_groups'] == j, :]
        trainX = adata_ij.X
        trainX = np.int32(trainX.toarray())
        cellnum = adata_ij.n_obs
        genenum = adata_ij.n_vars

        file_path = 'save_IMG_filepath' + '/' + str(i) + '/' + str(j)
        if not os.path.exists(file_path):
            os.makedirs(file_path)

        for cell_i in range(cellnum):
            gene_features_i = trainX[cell_i:cell_i + 1, :]
            gene_features_i = gene_features_i.reshape(40, 50)
            img_i = Image.fromarray(gene_features_i)

            file_path_IMG = 'save_IMG_filepath' + '/' + str(i) + '/' + str(j) + '/' + str(cell_i) + '.png'
            img_i.convert('L').save(file_path_IMG, format='png')

end_time = time.gmtime()
print(time.strftime('%Y-%m-%d %H:%M:%S', end_time))
