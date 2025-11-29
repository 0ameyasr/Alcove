"""
models.py

Stores the model used to make verdicts on the Radar Tool. Is trained on a
synthetic set of data that aims to capture real-world mental health data.

"""

import numpy
import torch
import torch.nn as nn

from catboost import CatBoostClassifier


# ==== Radar-V2 (Deprecated, ANN) ====
class ANNModel(nn.Module):
    def __init__(self):
        super(ANNModel, self).__init__()

        self.fc1 = nn.Linear(5, 8)
        self.fc2 = nn.Linear(8, 16)
        self.fc3 = nn.Linear(16, 32)
        self.fc4 = nn.Linear(32, 4)

        self.dropout = nn.Dropout(p=0.25)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.relu(self.fc2(x))
        x = self.relu(self.fc3(x))
        x = self.dropout(x)
        x = self.fc4(x)
        return x


# ==== Radar-V3 (Improved CatBoost) ====
radar_v3 = CatBoostClassifier()
radar_v3.load_model("model/radar/v3/radar-v3.cbm")

# ==== Risks Constant ====
RISKS = ["NONE", "MILD", "MODERATE", "SEVERE"]


def make_radar_verdict_v2(score):
    """Make RADAR prediction using the v2 model (ANN, Deprecated!)"""

    def manually_scale_score(score, mean, variance):
        scaled_score = (score - mean) / numpy.sqrt(variance)
        return scaled_score

    mean = numpy.array([13.54867257, 10.31969027, 19.35619469, 10.27323009, 5.30973451])
    variance = numpy.array(
        [64.18347169, 41.98961229, 147.62976251, 43.91981435, 12.00583444]
    )

    score = manually_scale_score(numpy.array(score), mean, variance)
    score = torch.tensor(score, dtype=torch.float32).unsqueeze(0)

    model = ANNModel()
    model.load_state_dict(torch.load("model/RadarTorchS87.pth"))
    model.eval()

    with torch.no_grad():
        p = model(score)
    max_idx = torch.argmax(p).item()
    return RISKS[max_idx]


def make_radar_verdict_v3(score):
    """Make RADAR prediction using the v3 model (CatBoost)"""
    rclass = radar_v3.predict(score)
    return RISKS[rclass[0]]
