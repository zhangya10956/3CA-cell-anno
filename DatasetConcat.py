###CODE by YaZhang, 2023,11,30

import anndata as ad
import pandas as pd
import numpy as np
import scanpy as sc


####用于多个数据集合并取共同基因。多个数据集请自行添加adata变量
adata1 = sc.read_h5ad('h5ad_filepath1')      #  #0314Baron_withoutX.h5ad
adata2 = sc.read_h5ad('h5ad_filepath2')
adata3 = sc.read_h5ad('h5ad_filepath3')
#添加数据集名称来源
adata1 = adata1[adata1.obs['dataname'] == 'DatasetNAME1', :]
adata2 = adata2[adata2.obs['dataname'] == 'DatasetNAME2', :]
adata3 = adata3[adata3.obs['dataname'] == 'DatasetNAME3', :]
#获得有共同基因的数据集
adata = ad.concat([adata1, adata2, adata3], uns_merge="same")
print(adata.obs['dataname'].unique())
print(adata.obs['cell_groups'].unique())
# 提取前2000个高变异基因highly variable features（HVGs）
sc.pp.highly_variable_genes(adata, n_top_genes=2000)   #这一步之前必须取对数sc.pp.log1p(adata)
#对高变异基因可视化：
sc.pl.highly_variable_genes(adata)
# 获取只有高变异基因的数据集
adata = adata[:, adata.var.highly_variable]
adata.write_h5ad('DatasetConcat.h5ad')

#拆分合并完有共同高变异基因的数据集
adata1 = adata[adata.obs['dataname'] == 'TestDataNAME', :]
adata.write_h5ad('TestData.h5ad')
adata2 = adata[adata.obs['dataname'] != 'TestDataNAME', :]
adata.write_h5ad('ReferenceData.h5ad')

'''
##################以下是可视化过程
# 按零均值单位方差标准化数据；
sc.pp.scale(adata) 
#运行PCA
sc.tl.pca(adata, svd_solver='arpack')
#绘制PCA图
sc.pl.pca(adata, color='GeneNAME')    #小鼠：Sox17    #人：A1CF
sc.pl.pca_variance_ratio(adata, log=True)
sc.pp.neighbors(adata)        
sc.tl.umap(adata)
sc.pl.umap(adata, color='GeneNAME')
sc.tl.leiden(adata)
#聚类结果可视化
sc.pl.umap(adata, color=['leiden'])   #, 'S100B', 'AA06'
# ###添加图例
# plt.legend()     
# sc.pl.umap(adata, color=['leiden'], legend_loc='on data')    #legend_loc= 若默认不写，把图例放在图的右上    #, 'S100B'
# ###添加图例
#想要直观地显示某个基因在不同簇中的表达，可以使用：
sc.pl.violin(adata, ['GeneNAME1', 'GeneNAME2', 'GeneNAME3'], groupby='cell_groups')
sc.pl.violin(adata, ['GeneNAME1', 'GeneNAME2', 'GeneNAME3'], groupby='dataname')
#根据注释再次可视化：
sc.pl.umap(adata, color='cell_groups', title='title', frameon=False)      # save='.pdf'    #legend_loc='on data',
#气泡图显示：
sc.pl.dotplot(adata, ['GeneNAME1', 'GeneNAME2', 'GeneNAME3'], groupby='cell_groups')
#小提琴图显示
sc.pl.stacked_violin(adata, ['GeneNAME1', 'GeneNAME2', 'GeneNAME3'], groupby='cell_groups', rotation=90)
##################以下是可视化过程
'''

