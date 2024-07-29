
# Imports

import torch
import torch.nn as nn

class block(nn.Module):
  def __init__(self,in_channels,out_channels, **kwargs):
    super(block,self).__init__()
    self.layers = nn.Sequential(nn.Conv2d(in_channels,out_channels, **kwargs),
                                nn.BatchNorm2d(out_channels),
                                nn.ReLU())

  def forward(self,x):
    return self.layers(x)

class inception(nn.Module):
  def __init__(self, in_channels, out_1x1, red_3x3, out_3x3, red_5x5, out_5x5, out_1x1pool):
    super(inception,self).__init__()


    self.branch1 = block(in_channels, out_1x1, kernel_size=1)
    self.branch2 = nn.Sequential(block(in_channels, red_3x3, kernel_size=1),
                                 block(red_3x3, out_3x3, kernel_size=3, padding=1))
    self.branch3 = nn.Sequential(block(in_channels, red_5x5, kernel_size=1),
                                 block(red_5x5, out_5x5, kernel_size=5,padding=2))
    self.branch4 = nn.Sequential(nn.MaxPool2d(kernel_size=3, stride=1, padding=1),
                                 block(in_channels, out_1x1pool, kernel_size=1))



  def forward(self,x):
    return torch.cat([self.branch1(x), self.branch2(x), self.branch3(x), self.branch4(x)], 1)

class GoogLeNet(nn.Module):
  def __init__(self, num_classes=1000):
    super(GoogLeNet,self).__init__()

    self.conv1 = nn.Conv2d(in_channels= 3, out_channels=64, kernel_size=7,stride=2, padding=3)
    self.pool1 = nn.MaxPool2d(kernel_size=3,stride=2, padding=1)
    self.conv2 = nn.Conv2d(64,192, kernel_size=3,stride=1, padding=1)
    self.pool2 = nn.MaxPool2d(kernel_size=3,stride=2, padding=1)

    self.inception3a = inception(192,64,96,128,16,32,32)
    self.inception3b = inception(256,128,128,192,32,96,64)
    self.pool3 = nn.MaxPool2d(kernel_size=3,stride=2, padding=1)

    self.inception4a = inception(480,192,96,208,16,48,64)
    self.inception4b = inception(512,160,112,224,24,64,64)
    self.inception4c = inception(512,128,128,256,24,64,64)
    self.inception4d = inception(512,112,144,288,32,64,64)
    self.inception4e = inception(528,256,160,320,32,128,128)
    self.pool4 = nn.MaxPool2d(kernel_size=3,stride=2, padding=1)

    self.inception5a = inception(832, 256,160,320,32,128,128)
    self.inception5b = inception(832,384,192,384,48,128,128)

    self.pool5 = nn.AvgPool2d(kernel_size=7,stride=1, padding=0)
    self.dropout = nn.Dropout(p=0.4)
    self.fc = nn.Linear(1024,num_classes)

  def forward(self,x):
    x = self.conv1(x)
    x = self.pool1(x)
    x = self.conv2(x)
    x = self.pool2(x)
    x = self.inception3a(x)
    x = self.inception3b(x)

    x = self.pool3(x)

    x = self.inception4a(x)
    x = self.inception4b(x)
    x = self.inception4c(x)
    x = self.inception4d(x)
    x = self.inception4e(x)

    x = self.pool4(x)

    x = self.inception5a(x)
    x = self.inception5b(x)

    x = self.pool5(x)

    x = x.reshape(x.shape[0],-1)

    x = self.fc(x)

    return x

input = torch.rand(2,3,224,224)
model = GoogLeNet()
output = model(input)
output.shape

