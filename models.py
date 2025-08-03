""" 
models.py

Stores the model used to make verdicts on the Radar Tool. Is trained on a
synthetic set of data that aims to capture real-world mental health data.

"""

import torch
import torch, torch.nn as nn, torch.optim as optim
import numpy

class ANNModel(nn.Module):
  def __init__(self):
    super(ANNModel,self).__init__()
    
    self.fc1 = nn.Linear(5,8)
    self.fc2 = nn.Linear(8,16)
    self.fc3 = nn.Linear(16,32)
    self.fc4 = nn.Linear(32,4)

    self.dropout = nn.Dropout(p=0.25)

    self.relu = nn.ReLU()
  
  def forward(self,x):
    x = self.relu(self.fc1(x))
    x = self.relu(self.fc2(x))
    x = self.relu(self.fc3(x))
    x = self.dropout(x)
    x = self.fc4(x)
    return x

def make_radar_verdict(score):
  def manually_scale_score(score, mean, variance):
    scaled_score = (score - mean) / numpy.sqrt(variance)
    return scaled_score
  
  mean = numpy.array([
    13.54867257, 
    10.31969027, 
    19.35619469, 
    10.27323009, 
    5.30973451])
  variance = numpy.array([
    64.18347169, 
    41.98961229, 
    147.62976251,
    43.91981435, 
    12.00583444
  ])
  
  score = manually_scale_score(numpy.array(score), mean, variance)
  score = torch.tensor(score, dtype=torch.float32).unsqueeze(0)

  model = ANNModel()
  model.load_state_dict(torch.load('model/RadarTorchS87.pth'))
  model.eval()
  
  with torch.no_grad():
      p = model(score)
  risks = ["NONE", "MILD", "MOD", "SEV"]
  max_idx = torch.argmax(p).item()
  return risks[max_idx]