# !/usr/bin/env python
# -*- coding: utf-8

"""
@file       : read_chinese_path.py
@author     : Minghui Guo
@email      : mh.guo@foxmail.com
@time       : 2021-05-17 16:36
@description:

"""
import cv2
import numpy as np


def cv_imread(file_path=''):
    """
    解决cv2读取中文问题
    注：如果是灰度图，则会正常读取称为灰度图（和cv2.imread默认将灰度图读成三通道不同）
    :param file_path:文件名
    :return:返回文件读取的图像
    """
    cv_img = cv2.imdecode(np.fromfile(file_path, dtype=np.uint8), -1)
    return cv_img


def cv_imwrite(image, image_name:str):
    cv2.imencode('.' + image_name.split('.')[-1], image)[1].tofile(image_name)