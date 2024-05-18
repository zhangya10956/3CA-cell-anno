## scCAM-cell-anno
scCAM: An interpretable deep learning method to automatically annotate cell type and discovery of new differentially expressed genes in scRNA-seq data with residual network and layer class activation maps.


##Data and file running processes
1、preprocess.py
2、dataset-concat.py
3、h5ad2IMG.py
4、split_data_scCAM.py (not necessary)
5、train-scCAM.py
6、test-scCAM.py

All of the above files require changes to the input and output paths.


## Requirements

anaconda3
python 3.7

python packages:
torch 1.12.0, torchcam 0.3.2, keras 2.9.0,
tensorboard 2.9.1, tensorflow 2.9.1, torchvision 0.13.0,
numpy 1.21.2, pandas 1.3.5, Pillow 9.2.0, matplotlib 3.5.0, scipy 1.7.1, argparse 3.2
scanpy 1.9.1, anndata 0.8.0, h5py 3.7.0,

All gene expression matrices should be stored in h5ad files.


## Issues

If you encounter any bugs or have any specific feature requests, please [file an
issue](https://github.com/zhangya10956/scCAM-cell-anno/issues).

---