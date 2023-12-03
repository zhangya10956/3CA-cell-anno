# preprocess.py
#!/usr/bin/env	python3

""" data preprocessing using pytorch

author YaZhang
"""

import argparse
import os
import torch
from conf import settings
from utils import get_network, get_best_acc_weights_path, get_most_recent_folder_path, get_test_dataloader_3CA
from tools.confusion_matrix import cm_plot
import time
import pandas as pd

start = time.gmtime()
print(time.strftime("%Y-%m-%d %H:%M:%S", start))

if __name__ == '__main__':

    net_name = 'resnet18'
    resize = 100
    CA_path = r'filepath_IMG'
    test_path = os.path.join(CA_path, 'test')


    best_weight_path = get_best_acc_weights_path(get_most_recent_folder_path(os.path.join(os.getcwd(), settings.CHECKPOINT_PATH, net_name), settings.DATE_FORMAT))
    # best_weight_path = 'checkpoint/best_weight_path'
    print(best_weight_path)

    parser = argparse.ArgumentParser()
    parser.add_argument('-net', type=str, default=net_name, help='net type')          # required=True
    parser.add_argument('-weights', type=str, default=best_weight_path, help='the weights file you want to test')
    parser.add_argument('-gpu', action='store_true', default=True, help='use gpu or not')
    parser.add_argument('-b', type=int, default=16, help='batch size for dataloader')
    args = parser.parse_args()
    net = get_network(args)
    print(net)

    CA_test_loader = get_test_dataloader_3CA(test_path, resize, batch_size=args.b)

    net.load_state_dict(torch.load(args.weights))

    net.eval()

    correct_1 = 0.0
    correct_5 = 0.0
    total = 0
    true_label = []
    pred_label = []
    pred_label_2 = []
    softconf_1 = []
    softconf_2 = []

    with torch.no_grad():
        for n_iter, (image, label) in enumerate(CA_test_loader):
            print("iteration: {}\ttotal {} iterations".format(n_iter + 1, len(CA_test_loader)))

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
            ###
            # pred_label_2.extend(pred[:, 1:2].view(1, -1).squeeze(0).cpu().numpy().tolist())
            # softconf_1.extend(softconf[:, :1].view(1, -1).squeeze(0).cpu().detach().numpy().tolist())
            # softconf_2.extend(softconf[:, 1:2].view(1, -1).squeeze(0).cpu().detach().numpy().tolist())

            label = label.view(label.size(0), -1).expand_as(pred)
            correct = pred.eq(label).float()
            #compute top 5
            correct_5 += correct[:, :5].sum()
            #compute top1
            correct_1 += correct[:, :1].sum()

    ####
    # df_pred = pd.concat([pd.DataFrame({'label': true_label}), pd.DataFrame({'pred_1': pred_label}), pd.DataFrame({'pred_1_conf': softconf_1}).mul(100),
    #                      pd.DataFrame({'pred_2': pred_label_2}), pd.DataFrame({'pred_2_conf': softconf_2}).mul(100)], axis=1)      #ignore_index=True
    ###
    df_pred = pd.concat([pd.DataFrame({'label': true_label}), pd.DataFrame({'pred_1': pred_label})], axis=1)  # ignore_index=True
    df_pred_filepath = 'df_pred_filepath'
    df_pred.to_csv(df_pred_filepath)

    if args.gpu:
        print('GPU INFO.....')
        print(torch.cuda.memory_summary(), end='')

    print()
    print("Top 1 err: ", 1 - correct_1 / len(CA_test_loader.dataset))
    print("Top 5 err: ", 1 - correct_5 / len(CA_test_loader.dataset))
    print("Parameter numbers: {}".format(sum(p.numel() for p in net.parameters())))

    label = ['A cell', 'B cell', 'C cell', 'D cell']
    print(type(label))
    ###
    cm_plot(true_label, pred_label, label, pic=best_weight_path[:-4])


end = time.gmtime()
print(time.strftime("%Y-%m-%d %H:%M:%S", end))