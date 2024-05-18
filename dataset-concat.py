# preprocess.py
#!/usr/bin/env	python3

""" Concat datasets from different sources using pytorch

author YaZhang
"""

import anndata as ad
import pandas as pd
import numpy as np
import scanpy as sc

#Reading data from h5ad_files
adata1 = sc.read_h5ad('h5ad_filepath1')      #D:/PyCharm Community Edition 2021.2.3/dataset/DBSY/0701-yixian-BSMX.h5ad
adata2 = sc.read_h5ad('h5ad_filepath2')
adata3 = sc.read_h5ad('h5ad_filepath3')

#Naming the different datasets
adata1 = adata1[adata1.obs['dataname'] == 'DatasetNAME1', :]
adata2 = adata2[adata2.obs['dataname'] == 'DatasetNAME2', :]
adata3 = adata3[adata3.obs['dataname'] == 'DatasetNAME3', :]

#Concat datasets from different sources
adata = ad.concat([adata1, adata2, adata3], uns_merge="same")
print(adata.obs['dataname'].unique())
print(adata.obs['cell_groups'].unique())

#Extract the 2000 highly variable genes（HVGs）
#This step must be preceded by sc.pp.log1p(adata)
sc.pp.highly_variable_genes(adata, n_top_genes=2000)   #这一步之前必须取对数sc.pp.log1p(adata)
#Plot the 2000 highly variable genes（HVGs）
sc.pl.highly_variable_genes(adata)

#Save data that extract the 2000 highly variable genes
adata = adata[:, adata.var.highly_variable]
adata.write_h5ad('DatasetConcat.h5ad')

#Divide the total adata into sub-datasets or trainset and testset according to dataname
adata1 = adata[adata.obs['dataname'] == 'TestDataNAME', :]
adata.write_h5ad('TestData.h5ad')
adata2 = adata[adata.obs['dataname'] != 'TestDataNAME', :]
adata.write_h5ad('ReferenceData.h5ad')

'''
##################
#Graphing and visualizing adata, such as pca, umap, violin, dotplot, stacked_violin
sc.pp.scale(adata) 

sc.tl.pca(adata, svd_solver='arpack')

sc.pl.pca(adata, color='GeneNAME')    #小鼠：Sox17    #人：A1CF
sc.pl.pca_variance_ratio(adata, log=True)
sc.pp.neighbors(adata)        
sc.tl.umap(adata)
sc.pl.umap(adata, color='GeneNAME')
sc.tl.leiden(adata)

sc.pl.umap(adata, color=['leiden'])   #, 'S100B', 'AA06'

# plt.legend()     
# sc.pl.umap(adata, color=['leiden'], legend_loc='on data')    #legend_loc= 若默认不写，把图例放在图的右上    #, 'S100B'


sc.pl.violin(adata, ['GeneNAME1', 'GeneNAME2', 'GeneNAME3'], groupby='cell_groups')
sc.pl.violin(adata, ['GeneNAME1', 'GeneNAME2', 'GeneNAME3'], groupby='dataname')

sc.pl.umap(adata, color='cell_groups', title='title', frameon=False)      # save='.pdf'    #legend_loc='on data',

sc.pl.dotplot(adata, ['GeneNAME1', 'GeneNAME2', 'GeneNAME3'], groupby='cell_groups')

sc.pl.stacked_violin(adata, ['GeneNAME1', 'GeneNAME2', 'GeneNAME3'], groupby='cell_groups', rotation=90)
##################
'''

