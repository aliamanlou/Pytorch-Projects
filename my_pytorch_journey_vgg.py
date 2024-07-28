# -*- coding: utf-8 -*-
"""My Pytorch Journey - VGG.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1oJjxV-q34RL-qgEJHWPCRkOVl7Oq0Ifw
"""

# Imports

import torch
import torch.nn as nn

VGG_types = {
    'VGG11': [64, 'M', 128, 'M', 256, 256, 'M', 512, 512, 'M', 512, 512, 'M'],
    'VGG13': [64, 64, 'M', 128, 128, 'M', 256, 256, 'M', 512, 512, 'M', 512, 512, 'M'],
    'VGG16': [64, 64, 'M', 128, 128, 'M', 256, 256, 256, 'M', 512, 512, 512, 'M', 512, 512, 512, 'M'],
    'VGG19': [64, 64, 'M', 128, 128, 'M', 256, 256, 256, 256, 'M', 512, 512, 512, 512, 'M', 512, 512, 512, 512, 'M'],
}

class VGG_net(nn.Module):
  def __init__(self, in_channels=3, num_classes=1000):
    super(VGG_net,self).__init__()


    self.in_channels = in_channels

    self.conv_layers = self.create_conv_layers(VGG_types['VGG16'])

    self.fcs = nn.Sequential(nn.Linear(512*7*7,4096),
                             nn.ReLU(),
                             nn.Dropout(p=0.5),
                             nn.Linear(4096,4096),
                             nn.ReLU(),
                             nn.Dropout(p=0.5),
                             nn.Linear(4096,num_classes))

  def forward(self,x):
    x = self.conv_layers(x)
    x = x.reshape(x.shape[0], -1)
    x = self.fcs(x)
    return x

  def create_conv_layers(self,architecture):


    layers = []
    in_channels = self.in_channels

    for i in architecture:
      if type(i) == int:
        out_channels = i

        layers += [nn.Conv2d(in_channels=in_channels, out_channels=out_channels, kernel_size=3, stride=1, padding=1),
                   nn.BatchNorm2d(out_channels),
                   nn.ReLU()]
        in_channels = i

      elif i == "M":
        layers += [nn.MaxPool2d(kernel_size=2, stride=2, padding=0)]



    return nn.Sequential(*layers)

input = torch.rand(13,3,224,224)
model = VGG_net()
output = model(input)
output.shape

