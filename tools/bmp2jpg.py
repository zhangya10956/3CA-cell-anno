import os
import cv2
import numpy as np

def bmp2jpg(path:str):
    """
    将文件夹内的所有bmp格式的图像转化成jpg格式图像
    """
    for root, dirs, files in os.walk(path):
        for file in files:
            image_path = os.path.join(root, file)
            if os.path.isfile(image_path):
                if file.split('.')[-1] == 'bmp':
                    image = cv2.imread(image_path)
                    new_image_path = image_path.replace('.bmp', '.jpg')
                    cv2.imwrite(new_image_path, image)
                    # remove old image
                    os.remove(image_path)
                    print(new_image_path)


def cv_imread(file_path):
    cv_img = cv2.imdecode(np.fromfile(file_path, dtype = np.uint8), -1)
    return cv_img


def jpg2bmp(path:str):
    """
    将文件夹内的所有jpg格式的图像转化成bmp格式图像
    """
    for root, dirs, files in os.walk(path):
        for file in files:
            image_path = os.path.join(root, file)
            if os.path.isfile(image_path):
                if file.split('.')[-1] == 'jpg':
                    image = cv_imread(image_path)
                    new_image_path = image_path.replace('.jpg', '.bmp')
                    cv2.imwrite(new_image_path, image)
                    # remove old image
                    os.remove(image_path)
                    print(new_image_path)


if __name__ == '__main__':
    path = r'D:\Desktop\TUSP_total'
    jpg2bmp(path)