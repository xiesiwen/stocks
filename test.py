
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import time
import os 

for file in os.listdir("D:\\stocks"):
    os.rename("D:\\stocks\\" + file, "D:\\stocks\\" + file[0:9] + ".csv")