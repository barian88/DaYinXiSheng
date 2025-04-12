import torch.nn as nn
import torch

#refer to 18&34
class BasicBlock(nn.Module):
    expansion = 1
    #判断卷积核个数是否变化

    #in_channel：输入特征矩阵深度
    #out_channel：输出特征矩阵深度——主分支上卷积核的个数
    #downsample：卷积3x、4x、5x，每层开头有一层虚线的残差结构，将上一层的维度缩放到需要的维度，downsample对应1x1的卷积层
    def __init__(self, in_channel, out_channel, stride=1, downsample=None, **kwargs):
        super(BasicBlock, self).__init__()
        #kernel_size=3：卷积核大小为3x3
        #stride = 1：对应实线残差结构，不对长宽进行修改
        #bias=False：不使用偏置
        self.conv1 = nn.Conv2d(in_channels=in_channel, out_channels=out_channel,
                               kernel_size=3, stride=stride, padding=1, bias=False)
        #out_channel：对应输入特征矩阵的深度
        self.bn1 = nn.BatchNorm2d(out_channel)
        #定义激活函数
        self.relu = nn.ReLU()
        #定义第二个卷积层
        self.conv2 = nn.Conv2d(in_channels=out_channel, out_channels=out_channel,
                               kernel_size=3, stride=1, padding=1, bias=False)
        # 定义第二个BN层，out_channel：对应输入特征矩阵的深度
        self.bn2 = nn.BatchNorm2d(out_channel)
        # 定义下采样方法，downsample=None
        self.downsample = downsample

    def forward(self, x):
        #x：特征矩阵
        #identity：捷径分支（曲线分支）上的特征值
        identity = x
        if self.downsample is not None:
            #如果没有定义下采样的话，就对应实线的残差结构，跳过这个部分；
            #如果定义了，那么就将特征矩阵x输入到下采样当中，得到捷径分支的输出
            identity = self.downsample(x)

        #定义主线上的输出
        out = self.conv1(x)
        out = self.bn1(out)
        out = self.relu(out)

        out = self.conv2(out)
        out = self.bn2(out)
        #注意，这里没有经过relu激活函数

        #将主线输出与捷径上的输出相加
        out += identity
        #再次激活，得到最终输出
        out = self.relu(out)

        #返回expansion = 1，也就是resnet18/34的输出
        return out


#refer to 50&101&152
class Bottleneck(nn.Module):
    """
    注意：原论文中，在虚线残差结构的主分支上，第一个1x1卷积层的步距是2，第二个3x3卷积层步距是1。
    但在pytorch官方实现过程中是第一个1x1卷积层的步距是1，第二个3x3卷积层步距是2，
    这么做的好处是能够在top1上提升大概0.5%的准确率。
    可参考Resnet v1.5 https://ngc.nvidia.com/catalog/model-scripts/nvidia:resnet_50_v1_5_for_pytorch
    """

    #输出深度为原来的4倍
    expansion = 4

    def __init__(self, in_channel, out_channel, stride=1, downsample=None,
                 groups=1, width_per_group=64):
        super(Bottleneck, self).__init__()

        width = int(out_channel * (width_per_group / 64.)) * groups

        self.conv1 = nn.Conv2d(in_channels=in_channel, out_channels=width,
                               kernel_size=1, stride=1, bias=False)  # squeeze channels
        self.bn1 = nn.BatchNorm2d(width)
        # -----------------------------------------
        self.conv2 = nn.Conv2d(in_channels=width, out_channels=width, groups=groups,
                               kernel_size=3, stride=stride, bias=False, padding=1)
        self.bn2 = nn.BatchNorm2d(width)
        # -----------------------------------------
        self.conv3 = nn.Conv2d(in_channels=width, out_channels=out_channel*self.expansion,
                               kernel_size=1, stride=1, bias=False)  # unsqueeze channels
        self.bn3 = nn.BatchNorm2d(out_channel*self.expansion)
        self.relu = nn.ReLU(inplace=True)
        self.downsample = downsample

    def forward(self, x):
        identity = x
        if self.downsample is not None:
            identity = self.downsample(x)

        out = self.conv1(x)
        out = self.bn1(out)
        out = self.relu(out)

        out = self.conv2(out)
        out = self.bn2(out)
        out = self.relu(out)

        out = self.conv3(out)
        out = self.bn3(out)

        out += identity
        out = self.relu(out)

        return out


class ResNet(nn.Module):

    #block：选择网络——BasicBlock
    #blocks_num：列表，四个数对应2x,3x,4x,5x的层数，比如resnet34就是3、4、6、3
    #num_classes：训练集的分类个数
    #include_top：在此基础上搭建更加复杂的网络？
    def __init__(self,
                 block,
                 blocks_num,
                 num_classes=1000,
                 include_top=True,
                 groups=1,
                 width_per_group=64):
        super(ResNet, self).__init__()
        self.include_top = include_top
        self.in_channel = 64

        self.groups = groups
        self.width_per_group = width_per_group

        #kernel_size=7：最开始的卷积核大小为7x7
        #padding=3：(7-1)/2
        #stride = 2：长宽变一半
        self.conv1 = nn.Conv2d(3, self.in_channel, kernel_size=7, stride=2,
                               padding=3, bias=False)
        self.bn1 = nn.BatchNorm2d(self.in_channel)
        self.relu = nn.ReLU(inplace=True)

        # 最大池化下采样，stride = 2：长宽变一半
        self.maxpool = nn.MaxPool2d(kernel_size=3, stride=2, padding=1)
        #对应2x
        self.layer1 = self._make_layer(block, 64, blocks_num[0])
        # 对应3x
        self.layer2 = self._make_layer(block, 128, blocks_num[1], stride=2)
        # 对应4x
        self.layer3 = self._make_layer(block, 256, blocks_num[2], stride=2)
        # 对应5x
        self.layer4 = self._make_layer(block, 512, blocks_num[3], stride=2)

        if self.include_top:
            #平均池化下采样层，7x7变为1x1
            self.avgpool = nn.AdaptiveAvgPool2d((1, 1))  # output size = (1, 1)
            #全连接层
            self.fc = nn.Linear(512 * block.expansion, num_classes)

        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                nn.init.kaiming_normal_(m.weight, mode='fan_out', nonlinearity='relu')

    #channel：对应残差结构中第一层的卷积核使用的个数，四个resnet都是64、128、256、512
    # blocks_num：列表，四个数对应2x,3x,4x,5x的层数，比如resnet34就是3、4、6、3
    def _make_layer(self, block, channel, block_num, stride=1):
        downsample = None
        #对于18和34的第一层，直接跳过
        #但后面三层，stride=2，都要生成下采样函数
        if stride != 1 or self.in_channel != channel * block.expansion:
            # stride=1时，长宽不变，改变深度
            # stride=2时，长宽变一半，深度也改变
            downsample = nn.Sequential(
                #self.in_channel：输入特征矩阵的深度
                #channel * block.expansion：输出特征矩阵的深度
                nn.Conv2d(self.in_channel, channel * block.expansion, kernel_size=1, stride=stride, bias=False),
                nn.BatchNorm2d(channel * block.expansion))

        layers = []
        # self.in_channel：输入特征矩阵的深度
        # channel：对应残差结构中第一层的卷积核使用的个数，四个resnet都是64、128、256、512
        layers.append(block(self.in_channel,
                            channel,
                            downsample=downsample,
                            stride=stride,
                            groups=self.groups,
                            width_per_group=self.width_per_group))
        # 这里对50、101、152的self.in_channel扩充了，后面循环压入的时候就不用扩充了
        self.in_channel = channel * block.expansion

        #从第二层2x开始
        for _ in range(1, block_num):
            #将网络结构压入
            layers.append(block(self.in_channel,
                                channel,
                                groups=self.groups,
                                width_per_group=self.width_per_group))

        return nn.Sequential(*layers)

    #前向传播
    def forward(self, x):
        x = self.conv1(x)
        x = self.bn1(x)
        x = self.relu(x)
        x = self.maxpool(x)

        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)

        if self.include_top:
            x = self.avgpool(x)
            x = torch.flatten(x, 1)
            x = self.fc(x)

        return x


def resnet34(num_classes=1000, include_top=True):
    # https://download.pytorch.org/models/resnet34-333f7ec4.pth
    return ResNet(BasicBlock, [3, 4, 6, 3], num_classes=num_classes, include_top=include_top)


def resnet50(num_classes=1000, include_top=True):
    # https://download.pytorch.org/models/resnet50-19c8e357.pth
    return ResNet(Bottleneck, [3, 4, 6, 3], num_classes=num_classes, include_top=include_top)


def resnet101(num_classes=1000, include_top=True):
    # https://download.pytorch.org/models/resnet101-5d3b4d8f.pth
    return ResNet(Bottleneck, [3, 4, 23, 3], num_classes=num_classes, include_top=include_top)


def resnext50_32x4d(num_classes=1000, include_top=True):
    # https://download.pytorch.org/models/resnext50_32x4d-7cdf4587.pth
    groups = 32
    width_per_group = 4
    return ResNet(Bottleneck, [3, 4, 6, 3],
                  num_classes=num_classes,
                  include_top=include_top,
                  groups=groups,
                  width_per_group=width_per_group)


def resnext101_32x8d(num_classes=1000, include_top=True):
    # https://download.pytorch.org/models/resnext101_32x8d-8ba56ff5.pth
    groups = 32
    width_per_group = 8
    return ResNet(Bottleneck, [3, 4, 23, 3],
                  num_classes=num_classes,
                  include_top=include_top,
                  groups=groups,
                  width_per_group=width_per_group)
