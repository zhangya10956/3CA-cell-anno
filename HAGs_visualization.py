# HAGs_visualization.py
#!/usr/bin/env	python3

"""
visualization high_attention_genes using pytorch
author YaZhang
"""

import scanpy as sc
import matplotlib.pyplot as plt
from matplotlib.pyplot import rc_context


# 设置
# sc.settings.set_figure_params(dpi=80, frameon=False, fontsize=12)  #, figsize=[1.5, 1.5], color_map='viridis_r', facecolor='white '    #fontsize设置标题的字体大小     color_map好像没有用，调节不了颜色
plt.rc('font', family='Arial')

adata = sc.read_h5ad('test_h5ad_filepath')
print(adata)

high_attention_genes_TOP20 = [
'FEV', 'CAMK2G', 'IRX1', 'C5orf38',
'INS', 'PAX6', 'FXYD2', 'IAPP', 'HADH', 'SLC39A14',
'SST', 'LEPR', 'SSTR1',
'PPY', 'STMN2', 'SCGB2A1', 'NR0B1', 'PCDH9',
]


#气泡图显示
sc.pl.dotplot(adata, high_attention_genes_TOP20, groupby='cell_groups')
#小提琴图显示
sc.pl.stacked_violin(adata, high_attention_genes_TOP20, groupby='cell_groups', rotation=90)
###绘制热图
sc.pl.heatmap(adata, high_attention_genes_TOP20, groupby='cell_groups', cmap='RdPu', swap_axes=True)

#想要直观地显示某个基因在不同簇中的表达，可以使用小提琴图：
sc.pl.violin(adata, 'IRX1', groupby='cell_groups')




#############################cmap图谱
# 'Accent', 'Accent_r', 'Blues', 'Blues_r', 'BrBG', 'BrBG_r', 'BuGn', 'BuGn_r', 'BuPu', 'BuPu_r', 'CMRmap', 'CMRmap_r', \
# 'Dark2', 'Dark2_r', 'GnBu', 'GnBu_r', 'Greens', 'Greens_r', 'Greys', 'Greys_r', 'OrRd', 'OrRd_r', 'Oranges', 'Oranges_r',\
# 'PRGn', 'PRGn_r', 'Paired', 'Paired_r', 'Pastel1', 'Pastel1_r', 'Pastel2', 'Pastel2_r', 'PiYG', 'PiYG_r', 'PuBu', 'PuBuGn',\
# 'PuBuGn_r', 'PuBu_r', 'PuOr', 'PuOr_r', 'PuRd', 'PuRd_r', 'Purples', 'Purples_r', 'RdBu', 'RdBu_r', 'RdGy', 'RdGy_r', \
# 'RdPu', 'RdPu_r', 'RdYlBu', 'RdYlBu_r', 'RdYlGn', 'RdYlGn_r', 'Reds', 'Reds_r', 'Set1', 'Set1_r', 'Set2', 'Set2_r', 'Set3',\
# 'Set3_r', 'Spectral', 'Spectral_r', 'Wistia', 'Wistia_r', 'YlGn', 'YlGnBu', 'YlGnBu_r', 'YlGn_r', 'YlOrBr', 'YlOrBr_r', \
# 'YlOrRd', 'YlOrRd_r', 'afmhot', 'afmhot_r', 'autumn', 'autumn_r', 'binary', 'binary_r', 'bone', 'bone_r', 'brg', 'brg_r',\
# 'bwr', 'bwr_r', 'cividis', 'cividis_r', 'cool', 'cool_r', 'coolwarm', 'coolwarm_r', 'copper', 'copper_r', 'cubehelix', \
# 'cubehelix_r', 'flag', 'flag_r', 'gist_earth', 'gist_earth_r', 'gist_gray', 'gist_gray_r', 'gist_heat', 'gist_heat_r', \
# 'gist_ncar', 'gist_ncar_r', 'gist_rainbow', 'gist_rainbow_r', 'gist_stern', 'gist_stern_r', 'gist_yarg', 'gist_yarg_r', \
# 'gnuplot', 'gnuplot2', 'gnuplot2_r', 'gnuplot_r', 'gray', 'gray_r', 'hot', 'hot_r', 'hsv', 'hsv_r', 'inferno', 'inferno_r',\
# 'jet', 'jet_r', 'magma', 'magma_r', 'nipy_spectral', 'nipy_spectral_r', 'ocean', 'ocean_r', 'pink', 'pink_r', 'plasma', \
# 'plasma_r', 'prism', 'prism_r', 'rainbow', 'rainbow_r', 'seismic', 'seismic_r', 'spring', 'spring_r', 'summer', 'summer_r',\
# 'tab10', 'tab10_r', 'tab20', 'tab20_r', 'tab20b', 'tab20b_r', 'tab20c', 'tab20c_r', 'terrain', 'terrain_r', 'turbo', \
# 'turbo_r', 'twilight', 'twilight_r', 'twilight_shifted', 'twilight_shifted_r', 'viridis', 'viridis_r', 'winter', 'winter_r'
#############################cmap图谱

