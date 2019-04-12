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


dirs = os.listdir("saved_environments")
files = [os.listdir("saved_environments/"+dirs[i])[0] for i in range(len(dirs))]
i = 22
# print("Showing file " + str(i) + " / " + str(len(files)))
# print(files[i])
for i in range(len(files)):
    print(files[i])
    env = env_core([])
    env.load_results(dirs[i]+"/"+files[i])

    env.generatePlots(name="plots/"+files[i])

    del env