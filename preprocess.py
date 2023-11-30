###CODE by YaZhang, 2023,11,30

import numpy as np
import pandas as pd
import scanpy as sc
import matplotlib.pyplot as plt


#先对未进行normalize的合并数据集进行UMAP操作，在UMAP之前要先进行PCA降维操作，才能正确使用UMAP。
# 设置
sc.settings.set_figure_params(dpi=80, facecolor='white', frameon=False, fontsize=12)
plt.rc('font', family='Arial')

# 载入文件
adata = sc.read_h5ad('h5ad_filepath')
#其他类型文件读取方法
# adata = sc.read_10x_mtx(
#     'mtx_filepath',  # mtx 文件目录
#     var_names='gene_symbols')            # 使用 gene_symbols 作为变量名
#adata = sc.read_csv('csv_filepath')
#其他类型文件读取方法

#添加注释
adata_anno = np.loadtxt('anno.csv', delimiter=',', dtype=np.int32)
adata.obs['cell_groups'] = pd.Categorical(adata_anno)
print(adata.obs['cell_groups'].unique())
# ##若读入的h5ad文件中已有注释，rename注释名称使用下面代码：
# print(adata.obs['cell_groups'])      #读入数据中带的adata.obs['cell_groups']的dtype: int64，实际应该是dtype: category，所以需要转换一下。
# adata.obs['cell_groups'] = pd.Categorical(adata.obs['cell_groups'].to_numpy())
# new_cluster_names = ['A cell', 'B cell', 'C cell', 'D cell', 'E cell']       #对细胞注释进行重新命名
# adata.rename_categories('cell_groups', new_cluster_names)
# print(adata.obs['cell_groups'].unique())

#消除重复的列
adata.var_names_make_unique()
adata.obs_names_make_unique()
sc.pl.highest_expr_genes(adata, n_top=20, )     #画出表达量最高的前20个基因
#过滤细胞
sc.pp.filter_cells(adata, min_genes=1)
sc.pp.filter_genes(adata, min_cells=1)
print(adata)
# 将线粒体基因组保存为注释 var.mt
adata.var['mt'] = adata.var_names.str.startswith('MT-')
print(adata.var['mt'])
sc.pp.calculate_qc_metrics(adata, qc_vars=['mt'], percent_top=None, log1p=False, inplace=True)   #计算线粒体基因的比例
print(adata)
#画小提琴图
sc.pl.violin(adata, ['n_genes_by_counts', 'total_counts', 'pct_counts_mt'], jitter=0.4, multi_panel=True)
#画散点图，过滤异常细胞数据
sc.pl.scatter(adata, x='total_counts', y='pct_counts_mt')
sc.pl.scatter(adata, x='total_counts', y='n_genes_by_counts')
###获取线粒体基因占比在 5% 以下的细胞样本
adata = adata[adata.obs.pct_counts_mt < 5, :]

#函数normalize_total可以对每个细胞进行标准化，以便每个细胞在标准化后沿着基因方向求和具有相同的总数target_sum；使细胞间的基因表达量具有可比性；
sc.pp.normalize_total(adata, target_sum=1e4)
#为了适当扩大表达的差异，对数据取对数；
sc.pp.log1p(adata)

# # #将处理完的数据写入新h5ad文件
adata.write('data-preprocess.h5ad')
################预处理过程到此为止，提取HVGs在合并数据集过程中进行。

