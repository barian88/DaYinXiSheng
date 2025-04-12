import os
import torch as t
import model
from trainer import Trainer
import sys
import torchvision as tv

epoch = 19

#TODO: Enter your model here
net = model.ResNet()  # 假设你的模型类名为ResNet

crit = t.nn.BCELoss()
trainer = Trainer(net, crit)
trainer.restore_checkpoint(epoch)
trainer.save_onnx('checkpoint_{:03d}.onnx'.format(epoch))
