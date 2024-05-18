# !/usr/bin/env python
# -*- coding: utf-8 -*

"""
Confusion matrix parameter settings
"""

import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
import numpy as np
from sklearn.metrics import classification_report
import os


def cm_plot(original_label, predict_label, label, pic=None):    #Xlabel,
    # 混淆矩阵
    cm = confusion_matrix(original_label, predict_label)  # 由原标签和预测标签生成混淆矩阵
    # plt.legend(loc="upper right")
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签,字体为黑体 Times New Roman
    plt.rcParams['axes.unicode_minus'] = False    # 用来正常显示负号
    plt.title('Confusion Matrix', fontsize=14)
    num_local = np.array(range(len(label)))
    #Xnum_local = np.array(range(len(Xlabel)))
    plt.xticks(num_local, label, rotation=90)  # 将标签印在x轴坐标上 rotation=90
    #plt.xticks(Xnum_local, Xlabel, rotation=45)
    plt.yticks(num_local, label)                  # 将标签印在y轴坐标上
    plt.xlabel('Predicted Label', fontsize=14)
    plt.ylabel('True Label', fontsize=14)


    # 画混淆矩阵，配色风格使用
    cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]  # 归一化，为了使矩阵颜色的深浅
    plt.imshow(cm_normalized, cmap=plt.cm.Blues)      #原来为Greys
    plt.tick_params(labelsize=10)
    for x in range(len(cm)):
        for y in range(len(cm)):
            if x == y:
                plt.annotate(cm[x, y], xy=(x, y), color='black',   #原来是'white'
                             horizontalalignment='center', verticalalignment='center', fontsize=10)
            else:
                plt.annotate(cm[y, x], xy=(x, y), horizontalalignment='center', verticalalignment='center', fontsize=10)
            # annotate主要在图形中添加注释
            # 第一个参数添加注释
            # 第二个参数是注释的内容
            # xy设置箭头尖的坐标
            # horizontalalignment水平对齐
            # verticalalignment垂直对齐
            # 其余常用参数如下：
            # xytext设置注释内容显示的起始位置
            # arrowprops 用来设置箭头
            # facecolor 设置箭头的颜色
            # headlength 箭头的头的长度
            # headwidth 箭头的宽度
            # width 箭身的宽度
    result = classification_report(original_label, predict_label, digits=4)  # digits=4 表示保留四位小数
    print(result)

    plt.colorbar()  # 添加自定义颜色条
    if pic is not None:
        # 保存结果
        with open(str(pic) + '_result.txt', 'w') as f:
            f.write(result)
        # 保存混淆矩阵
        plt.savefig(str(pic) + '_result.png', dpi=120, bbox_inches='tight')  # bbox_inches='tight' 为了使保存的图片不会不完整
    plt.show()

