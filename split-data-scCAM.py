import scipy.io as scio
import os
import shutil
import random

""" 
Random split data using pytorch
"""

if __name__ == '__main__':
    # split data 8:2
    #Just change the file path
    path = r'filepath\IMG'
    radio = 0.8
    dirs = [os.path.join(path, i) for i in os.listdir(path)]
    print(dirs)
    for dir in dirs:
        images = [os.path.join(dir, i) for i in os.listdir(dir)]
        #Random split
        random.shuffle(images)
        num_files = len(images)
        print(num_files)
        train_num = int(radio * num_files)

        train_images = images[:train_num]
        test_images = images[train_num:]
        for j in train_images:
            os.renames(j, j.replace('IMG', 'IMG\\train'))
            pass
        for j in test_images:
            os.renames(j, j.replace('IMG', 'IMG\\test'))
            pass
