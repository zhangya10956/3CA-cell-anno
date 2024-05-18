# !/usr/bin/env python
# -*- coding: utf-8

"""
@file       : get_xsd.py
@author     : Minghui Guo
@email      : mh.guo@foxmail.com
@time       : 2021-05-17 16:25
@description: 获取两张图片的相似度

"""
import cv2
from skimage.metrics import structural_similarity

def get_xsd(image1, image2):
    """
    计算两张图片的结构相似度
    :param image1:
    :param image2:
    :return: 返回图片的相似概率
    """
    if image1.shape != image2.shape:
        image1 = cv2.resize(image1, (image2.shape[1], image2.shape[0]))
    return structural_similarity(image1, image2, multichannel=True)