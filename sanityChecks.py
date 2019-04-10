# -*- coding: utf-8 -*-
"""
"""

import numpy as np
import logging
import pickle
from pathlib import Path
from matplotlib import pyplot as plt
import os
from gifGen import gif
from Player import *
from core import *

env = env_core([])
files = os.listdir("saved_environments")
i = 22
print("Showing file " + str(i) + " / " + str(len(files)))
print(files[i])
env.load_results(filename=files[i])
env.displayResults()