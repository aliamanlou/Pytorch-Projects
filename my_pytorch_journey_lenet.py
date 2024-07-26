
# Imports

import torch
import torch.nn as nn

class LeNet(nn.Module):
  def __init__(self):
    super(LeNet,self).__init__()

    self.conv1 = nn.Conv2d(1,6, kernel_size=5,stride=1, padding=0)
    self.pool = nn.AvgPool2d(kernel_size=2, stride=2, padding=0)
    self.conv2 = nn.Conv2d(6,16,kernel_size=5,stride=1,padding=0)
    self.conv3 = nn.Conv2d(16,120, kernel_size=5, stride=1,padding=0)
    self.fc1 = nn.Linear(120,84)
    self.fc2 = nn.Linear(84,10)
    self.relu = nn.ReLU()

  def forward(self,x):
    x = self.relu(self.conv1(x))
    x = self.relu(self.pool(x))
    x = self.relu(self.conv2(x))
    x = self.relu(self.pool(x))
    x = self.relu(self.conv3(x))
    # N (Batch Size) * 120 (Number of Channels) * 1 (Height) * 1 (Width) ->  N * 120
    x = x.reshape(x.shape[0],-1)

    x = self.relu(self.fc1(x))
    x = self.fc2(x)
    return x

# Testing the network architecture with batch_size = 7
input = torch.rand(7,1,32,32)
model = LeNet()
output = model(input)
output.shape

