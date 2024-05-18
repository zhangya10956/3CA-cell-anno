# preprocess.py
#!/usr/bin/env	python3

""" data preprocessing using pytorch

author YaZhang
"""
import numpy as np
import pandas as pd
import scanpy as sc
import matplotlib.pyplot as plt




sc.settings.set_figure_params(dpi=80, facecolor='white', frameon=False, fontsize=12)
plt.rc('font', family='Arial')

#Reading files from h5ad_filepath or 10x_filepath
adata = sc.read_h5ad('h5ad_filepath')   #D:/PyCharm Community Edition 2021.2.3/dataset/DBSY/0701-yixian-BSMX.h5ad

# adata = sc.read_10x_mtx(
#     'mtx_filepath',
#     var_names='gene_symbols')
#adata = sc.read_csv('csv_filepath')


#Read the cell annotation file
adata_anno = np.loadtxt('anno.csv', delimiter=',', dtype=np.int32)
adata.obs['cell_groups'] = pd.Categorical(adata_anno)
print(adata.obs['cell_groups'].unique())

# print(adata.obs['cell_groups'])
# adata.obs['cell_groups'] = pd.Categorical(adata.obs['cell_groups'].to_numpy())
##Re-annotating cell types
# new_cluster_names = ['A cell', 'B cell', 'C cell', 'D cell', 'E cell']
# adata.rename_categories('cell_groups', new_cluster_names)
# print(adata.obs['cell_groups'].unique())

#Preprocessing data
adata.var_names_make_unique()
adata.obs_names_make_unique()
#Plot the top 20 most highly expressed genes
sc.pl.highest_expr_genes(adata, n_top=20, )

sc.pp.filter_cells(adata, min_genes=1)
sc.pp.filter_genes(adata, min_cells=1)
print(adata)

#Calculate the percent of mitochondrial genes
adata.var['mt'] = adata.var_names.str.startswith('MT-')
print(adata.var['mt'])
sc.pp.calculate_qc_metrics(adata, qc_vars=['mt'], percent_top=None, log1p=False, inplace=True)   #计算线粒体基因的比例
print(adata)

#Plotting violin and scatter plots
sc.pl.violin(adata, ['n_genes_by_counts', 'total_counts', 'pct_counts_mt'], jitter=0.4, multi_panel=True)
sc.pl.scatter(adata, x='total_counts', y='pct_counts_mt')
sc.pl.scatter(adata, x='total_counts', y='n_genes_by_counts')

#Retain cells with less than 5% percentage of mitochondrial genes
adata = adata[adata.obs.pct_counts_mt < 5, :]

#Normalize data
sc.pp.normalize_total(adata, target_sum=1e4)
#Log1p data
sc.pp.log1p(adata)

#Write data to data-preprocess.h5ad file
adata.write('./data-preprocess.h5ad')


