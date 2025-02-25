# preprocess.py
#!/usr/bin/env	python3

""" scCAM train using pytorch

author YaZhang
"""


from torchcam.methods import LayerCAM
from torchcam.utils import overlay_mask

import argparse
import os
import torch
from conf import settings
from utils import get_network, get_best_acc_weights_path, get_most_recent_folder_path, get_test_dataloader_scCAM
from tools.confusion_matrix import cm_plot
import time
import pandas as pd
import scanpy as sc
import numpy as np
from scipy import sparse
import anndata as ad
import h5py


start = time.gmtime()
print(time.strftime("%Y-%m-%d %H:%M:%S", start))

if __name__ == '__main__':

    net_name = 'resnet18'
    resize = 100
    scCAM_path = r'filepath_IMG'
    test_path = os.path.join(scCAM_path, 'test')

    #Read the optimal weights for training
    best_weight_path = get_best_acc_weights_path(get_most_recent_folder_path(os.path.join(os.getcwd(), settings.CHECKPOINT_PATH, net_name), settings.DATE_FORMAT))
    # best_weight_path = 'checkpoint/best_weight_path'
    print(best_weight_path)

    #Parameter settings same with training
    parser = argparse.ArgumentParser()
    parser.add_argument('-net', type=str, default=net_name, help='net type')          # required=True
    parser.add_argument('-weights', type=str, default=best_weight_path, help='the weights file you want to test')
    parser.add_argument('-gpu', action='store_true', default=True, help='use gpu or not')
    parser.add_argument('-b', type=int, default=16, help='batch size for dataloader')
    args = parser.parse_args()
    net = get_network(args)
    print(net)

    scCAM_test_loader = get_test_dataloader_scCAM(test_path, resize, batch_size=args.b)

    net.load_state_dict(torch.load(args.weights))

    net.eval()

    #LayerCAM
    cam_extractor = LayerCAM(net, 'conv2_x')

    #read the gene expression matrix (actually just read the gene names, csv, h5ad files are fine)
    adata = sc.read_h5ad('h5ad_filepath', backed='r')  #D:/PyCharm Community Edition 2021.2.3/dataset/DBSY/0701-yixian-BSMX/0701-BS-HVG2000-noscale.h5ad
    print(adata)
    gene_list = adata.var_names.tolist()
    gene_num = adata.n_vars
    #Turning gene_lists into DataFrame
    PD_gene_list = pd.DataFrame({'gene_list': gene_list})
    print(PD_gene_list)
    #Define an NUM_CLASSES * gene_num array with all zeros inside.
    high_attention_gene_list = [[0] * gene_num for i in range(settings.NUM_CLASSES)]    # 定义一个内部全部为0的数组。


    correct_1 = 0.0
    correct_5 = 0.0
    total = 0
    true_label = []
    pred_label = []
    pred_label_2 = []
    softconf_1 = []
    softconf_2 = []

    with torch.no_grad():
        for n_iter, (image, label) in enumerate(scCAM_test_loader):
            print("iteration: {}\ttotal {} iterations".format(n_iter + 1, len(scCAM_test_loader)))

            if args.gpu:
                image = image.cuda()
                label = label.cuda()
                # print('GPU INFO.....')
                # print(torch.cuda.memory_summary(), end='')

            output = net(image)
            conf, pred = output.topk(2, 1, largest=True, sorted=True)

            # discovery novel cell type
            '''
            softconf = torch.softmax(conf, dim=1)  #             
            # 
            for i in range(len(softconf)):
                if softconf[i, :1] < 0.99:
                    pred[i, :1] = settings.NUM_CLASSES
            '''
            # discovery novel cell type


            true_label.extend(label.cpu().numpy().tolist())
            pred_label.extend(pred[:, :1].view(1, -1).squeeze(0).cpu().numpy().tolist())

            ###Get the prediction label 2 and the corresponding confidence score
            # pred_label_2.extend(pred[:, 1:2].view(1, -1).squeeze(0).cpu().numpy().tolist())
            # softconf_1.extend(softconf[:, :1].view(1, -1).squeeze(0).cpu().detach().numpy().tolist())
            # softconf_2.extend(softconf[:, 1:2].view(1, -1).squeeze(0).cpu().detach().numpy().tolist())
            ###Get the prediction label 2 and the corresponding confidence score

            label = label.view(label.size(0), -1).expand_as(pred)
            correct = pred.eq(label).float()
            #compute top 5
            correct_5 += correct[:, :5].sum()
            #compute top1
            correct_1 += correct[:, :1].sum()
            out_list = pred[:, :1].view(1, -1).squeeze(0).cpu().numpy().tolist()
            # print(out_list)
            # print(pred[:, :1])
            # print(pred[:, :1].view(1, -1))       #tensor([[2, 2, 2, 2, 2, 2, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2]])
            # print(pred[:, :1].view(1, -1).squeeze(0))   #tensor([2, 2, 2, 2, 2, 2, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2])

            #Get layer class activation maps for each batch
            activation_map = cam_extractor(out_list, output)

            #Sum the LayerCAM maps of the same category in each batch
            for num_class in range(settings.NUM_CLASSES):
                # In each batch, get the  label_index (0 or 1 list) for each category
                label_index = (pred[:, :1].view(1, -1).squeeze(0) == num_class).nonzero().view(1, -1).squeeze(
                    0).cpu().numpy().tolist()
                for label_i in label_index:
                    #Convert LayerCAM maps to array
                    overlay_activation_map = np.asarray(activation_map[0][label_i].cpu())
                    #Convert the array to one-dimensional format, and Performs a sort for value from smallest to largest according to the model attention, and return the index of the position
                    overlay_AM_sort = np.reshape(overlay_activation_map, [1, -1]).argsort()  # [::-1]
                    #gene_weight means select the top 100 high attention locations
                    gene_weight = 100
                    #Reverse overlay_AM_sort and get the top 100 high attention locations
                    for gene_i in overlay_AM_sort[0][::-1][:100].tolist():  # 变不变成list都能运行，numpy.ndarray也可以参与for循环
                        #For each category and each image, high attention locations correspond to genes and add 1 weight
                        high_attention_gene_list[num_class][gene_i] += 1


        PD_high_attention_gene_list = pd.DataFrame(high_attention_gene_list)
        #Concat two gene DataFrame
        PD_HAGs_gene_list = pd.concat([PD_gene_list, PD_high_attention_gene_list.T], axis=1)
        print(PD_HAGs_gene_list)
        #Write the HAGs_gene_list to filepath
        PD_HAGs_gene_list_filepath = './HAGs_gene_list-100.csv'
        PD_HAGs_gene_list.to_csv(PD_HAGs_gene_list_filepath)

    ##Concat the label, prediction label and confidence score
    # df_pred = pd.concat([pd.DataFrame({'label': true_label}), pd.DataFrame({'pred_1': pred_label}), pd.DataFrame({'pred_1_conf': softconf_1}).mul(100),
    #                      pd.DataFrame({'pred_2': pred_label_2}), pd.DataFrame({'pred_2_conf': softconf_2}).mul(100)], axis=1)      #ignore_index=True


    df_pred = pd.concat([pd.DataFrame({'label': true_label}), pd.DataFrame({'pred_1': pred_label})], axis=1)  # ignore_index=True
    df_pred_filepath = './df_pred_filepath.csv'
    df_pred.to_csv(df_pred_filepath)

    if args.gpu:
        print('GPU INFO.....')
        print(torch.cuda.memory_summary(), end='')

    print()
    print("Top 1 err: ", 1 - correct_1 / len(scCAM_test_loader.dataset))
    print("Top 5 err: ", 1 - correct_5 / len(scCAM_test_loader.dataset))
    print("Parameter numbers: {}".format(sum(p.numel() for p in net.parameters())))

    label = ['A cell', 'B cell', 'C cell', 'D cell']
    print(type(label))
    ###Drawing the confusion matrix
    cm_plot(true_label, pred_label, label, pic=best_weight_path[:-4])


end = time.gmtime()
print(time.strftime("%Y-%m-%d %H:%M:%S", end))
