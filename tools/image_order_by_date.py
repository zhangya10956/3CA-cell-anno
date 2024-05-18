# !/usr/bin/env python
# -*- coding: utf-8 -*

"""
 @file       : image_order_by_date.py
 @author     : xbfreedreams
 @email      : xbfreedreams@163.com
 @time       : 2021-05-06 15:05
 @description: 按照时间循序进行排序

"""
import os
import cv2
from skimage.metrics import structural_similarity
import shutil

def order_images_by_date(path:str):
    """将同一个日期的图片放入同一个文件夹"""
    for root, dirs, files in os.walk(path):
        for file in files:
            image_path = os.path.join(root, file)
            date = image_path.split('_')[2]
            print(image_path)
            print(date)
            os.renames(image_path, os.path.join(root, date, file))


def get_xsd(image1, image2):
    """计算结构相似度"""
    if image1.shape != image2.shape:
        image1 = cv2.resize(image1, (image2.shape[1], image2.shape[0]))
    return structural_similarity(image1, image2, multichannel=True)


if __name__ == '__main__':
    path = r'D:\Desktop\TUSP_total'
    # order_images_by_date(path)
    count = 0
    for root, dirs, files in os.walk(path):
        if len(files) > 0:
            count = count + 1
            if count < 2:
                continue
            class_date = root.split('\\')[-1]
            print(root)
            print(files)
            for index in range(len(files)):
                # 第一张图片
                image1_path = os.path.join(root, files[index])
                image1 = cv2.imread(image1_path)
                # 从第二张图片开始
                for i in range(index+1, len(files)):
                    image2_path = os.path.join(root, files[i])
                    image2 = cv2.imread(image2_path)
                    # 计算相似度
                    try:
                        xsd = get_xsd(image1, image2)
                        if xsd >= 0.95:
                            text = 'ori: ' + image1_path + '\n' + 'new: ' + image2_path + '\n' + 'xsd: ' + str(xsd)
                            with open('xsd_0.95_image_path.txt', 'a') as f:
                                f.writelines(text)
                            shutil.move(image2_path, 'D:\Desktop\TUSP_move')
                    except Exception:
                        print(image1_path)
                        print(image2_path)