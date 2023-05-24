import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


load_path = r"C:\Users\王晨浩\Desktop\论文\1.csv"
pv_path = r"C:\Users\王晨浩\Desktop\GPU_test\bt1.csv"

load = pd.read_csv(load_path)
x  =load['列1.1'].tolist()
x1 =load['列1.2'].tolist()
x2 =load['列1.3'].tolist()

# print(load['列1.1'])
# print(load['列1.2'])
# print(load['列1.3'])
ht = 8000
soc = []
x5 =0.2
print(sum(x1))
print(sum(x2))













