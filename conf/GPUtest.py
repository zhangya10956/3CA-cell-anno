"""
Test the GPU is available
"""

import torch

print(torch.__version__)
print(torch.cuda.is_available())
print(torch.cuda.device_count())  # 查看可用的CUDA数量
print(torch.version.cuda)  # 查看CUDA的版本号