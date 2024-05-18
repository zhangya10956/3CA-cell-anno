# !/usr/bin/env python
# -*- coding: utf-8 -*

"""
 @file       : copy_image_from_txt.py
 @author     : xbfreedreams
 @email      : xbfreedreams@163.com
 @time       : 2021-05-08 20:15
 @description: 

"""
import os
import shutil


if __name__ == '__main__':
    path = r'E:\Python\pytorch-cifar100-master\tools\xsd_0.95_image_path.txt'
    save_folder = r'D:\Desktop\image'
    with open(path, 'r') as f:
        texts = f.readlines()
    for index in range(0, len(texts), 3):
        ori_image_path = texts[index][4:].strip()
        new_image_path = texts[index+1][4:].strip()
        class_name = ori_image_path.split('\\')[3]
        date = ori_image_path.split('\\')[4]
        ori_image_name = ori_image_path.split('\\')[-1]
        new_image_name = new_image_path.split('\\')[-1]

        print(class_name)
        print(date)
        print(ori_image_path)
        print(new_image_path)

        if not os.path.exists(os.path.join(save_folder, class_name, date)):
            os.makedirs(os.path.join(save_folder, class_name, date))

        shutil.copyfile(ori_image_path, os.path.join(save_folder, class_name, date, ori_image_name))
        shutil.copyfile(os.path.join('D:\Desktop\TUSP_move', new_image_name), os.path.join(save_folder, class_name, date, new_image_name))