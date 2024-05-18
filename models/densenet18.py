#卷积神经网络（高级篇）练习    2 ResNet改进DenseNet,根据代码了解原理

import torch
import torch.nn.functional as F
import torch.nn as nn

from torchvision import transforms
from torchvision import datasets
from torch.utils.data import DataLoader
import torch.optim as optim
import matplotlib.pyplot as plt



batch_size = 8
'''
transform = transforms.Compose([
    transforms.ToTensor(),         #将PIL（python image library）转变成Tensor。将像素范围由0-255变成0-1之间。
    transforms.Normalize((0.1307, ), (0.3081, ))    #均值归一化，均值为0.1307，标准差为0.3081
])
'''
#1.Prepare data
train_dataset = r'E:\Hep-2 dataset'
    datasets.MNIST(root='../dataset/mnist/',
                               train=True,
                               download=False,       #本来就下载好了，不需要再下载
                               transform=transform)
train_loader = DataLoader(train_dataset,
                          shuffle=True,
                          batch_size=batch_size)
test_dataset = datasets.MNIST(root='../dataset/mnist/',
                               train=False,
                               download=False,
                               transform=transform)
test_loader = DataLoader(test_dataset,
                          shuffle=False,
                          batch_size=batch_size)


#2.Design model using Class
#定义残差块模型ResidualBlock

class DensenetBlock(nn.Module):
    def __init__(self, channels):
        super(DensenetBlock, self).__init__()
        self.channels = channels
        self.conv1 = nn.Conv2d(channels, channels,
                               kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(channels, channels,
                               kernel_size=3, padding=1)

    def forward(self, x):
        xc1 = self.conv1(x)     #有修改
        x1 = F.relu(xc1+x)      #有修改
        xc2 = self.conv2(x1)    #有修改
        x2 = F.relu(xc2+xc1+x)  #有修改
        #y = self.conv2(y)
        #return F.relu(y+x)
        return x2
''''''
#定义网络模型
class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(1, 16, kernel_size=5)
        self.conv2 = nn.Conv2d(16, 32, kernel_size=5)

        self.denseblock1 = DensenetBlock(channels=16)
        self.denseblock2 = DensenetBlock(channels=32)

        self.mp = nn.MaxPool2d(2)
        self.fc = nn.Linear(512, 6)

    def forward(self, x):
        in_size = x.size(0)   #x的维度为B*C*W*H,  batch_size *channel * width *height ,此处取得是batch_size
        x = self.mp(F.relu(self.conv1(x)))
        x = self.denseblock1(x)
        x = self.mp(F.relu(self.conv2(x)))
        x = self.denseblock2(x)

        x = x.view(in_size, -1)   #-1代表可以获得任意给的值
        x = self.fc(x)
        return x


model = Net()

def densenet18():
    return model()


#设置GPU
device = torch.device("cuda:0"if torch.cuda.is_available() else "cpu")
model.to(device)

# 3. Construct loss and optimizer
criterion = torch.nn.CrossEntropyLoss()     #多分类用交叉熵损失函数
optimizer = optim.SGD(model.parameters(), lr=0.01, momentum=0.5)


#4. Training cycle
def train(epoch):
    running_loss = 0.0
    for batch_idx, data in enumerate(train_loader, 0):
        inputs, target = data
        # 训练数据设置GPU
        inputs, target = inputs.to(device), target.to(device)
        optimizer.zero_grad()
        #outputs + backward + update
        outputs = model(inputs)
        loss = criterion(outputs, target)
        loss.backward()
        optimizer.step()

        running_loss += loss.item()
        if batch_idx % 300 == 299:
            print('[%d,%5d] loss: %.3f' % (epoch+1, batch_idx+1, running_loss/2000))
            running_loss = 0.0


def test():
    correct = 0
    total = 0
    #test_running_loss = 0.0      #保存最优模型参数用
    with torch.no_grad():
        for data in test_loader:
            inputs, target = data
            # 测试数据设置GPU
            inputs, target = inputs.to(device), target.to(device)
            outputs = model(inputs)
            #test_loss = criterion(outputs, target)    #保存最优模型参数用
            #test_running_loss += test_loss.item()     #保存最优模型参数用
            _, predicted = torch.max(outputs.data, dim=1)
            total += target.size(0)
            correct += (predicted == target).sum().item()
    #acc_list.append(correct / total)    #画正确分类图用
    ##print('Accuracy on test set:%d %% [%d/%d]' % (100 * correct / total, correct, total))


if __name__ == '__main__':
    for epoch in range(10):
        #epoch_list.append(epoch+1)    #画正确分类图用
        train(epoch)
        test()

