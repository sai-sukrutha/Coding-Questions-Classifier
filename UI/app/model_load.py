import os
import collections
import pandas as pd
import numpy as np
import joblib

from config import Config


def get_modeldata():
    model = joblib.load(Config.MODEL_FILE)
    lb = joblib.load(Config.LB_FILE)
    le = joblib.load(Config.LE_FILE)
    return model,lb,le