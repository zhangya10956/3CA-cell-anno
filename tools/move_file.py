# !/usr/bin/env python
# -*- coding: utf-8 -*

"""
 @file       : move_file.py
 @author     : xbfreedreams
 @email      : xbfreedreams@163.com
 @time       : 2021-05-08 13:15
 @description: 

"""
import os
import cv2


if __name__ == '__main__':

    ori_path = r'D:\Desktop\20210508_TUSP_image_total\6LPLT'
    bz_path = r'D:\Desktop\20210508_TUSP_image_total\bz\10'

    for root, dirs, files in os.walk(ori_path):
        for file in files:
            image_path = os.path.join(root, file)
            bz_image_path = os.path.join(bz_path, file.replace('.bmp', '_10.png'))
            # print(bz_image_path)
            if os.path.exists(bz_image_path):
                # 如果存在标注信息
                ori_image = cv2.imread(image_path)
                bz_img = cv2.imread(bz_image_path)
                _, result_img = cv2.threshold(bz_img, 1, 255, cv2.THRESH_BINARY)
                # 黑底白色对象的轮廓
                contours, hierarchy = cv2.findContours(result_img[:, :, 0], cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
                if len(contours) <= 0:
                    print('无轮廓信息')
                    print(image_path)
                    cv2.imshow(image_path, bz_img)
                    cv2.waitKey()
                else:
                    # 有轮廓信息
                    # 获取最大的轮廓信息
                    max_contour = contours[0]
                    if len(contours) > 1:
                        for contour in contours:
                            if len(contour) > len(max_contour):
                                max_contour = contour
                    # 将轮廓画入原始图像
                    for contour in max_contour:
                        cv2.drawContours(ori_image, [contour], 0, (255, 255, 255), 1)
                    # cv2.imshow('test', ori_image)
                    # cv2.waitKey(0)
                    if not os.path.exists(os.path.join(root, 'bz')):
                        os.makedirs(os.path.join(root, 'bz'))
                    cv2.imwrite(os.path.join(root, 'bz', file), ori_image)
                    os.renames(image_path, os.path.join(root, 'ori', file))
                print('image_path: ', image_path)