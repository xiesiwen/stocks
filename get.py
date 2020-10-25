import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

dataset = pd.read_csv("D:\\res\\sh.600000d.csv", encoding='gbk')
nm = dataset.to_numpy()
x = []
for i in range(0, nm.shape[0]):
    if nm[i,2] > 1:
        x.append(nm[i])
x = np.array(x)
s = x[0:x.shape[0],4]
j = 0
for i in range(0, s.shape[0]):
    if s[i] > 0:
        j += 1
print(j / s.shape[0])

s = x[0:x.shape[0],5]
j = 0
for i in range(0, s.shape[0]):
    if s[i] > 0:
        j += 1
print(j / s.shape[0])

s = x[0:x.shape[0],6]
j = 0
for i in range(0, s.shape[0]):
    if s[i] > 0:
        j += 1
print(j / s.shape[0])
plt.figure()
plt.subplot(2,2,1)
plt.scatter(x[0:x.shape[0],2],x[0:x.shape[0],4])			#把x_data和y_data传进来

plt.subplot(2,2,2)
plt.scatter(x[0:x.shape[0],2],x[0:x.shape[0],5])			#把x_data和y_data传进来

plt.subplot(2,2,3)
plt.scatter(x[0:x.shape[0],2],x[0:x.shape[0],6])			#把x_data和y_data传进来

plt.subplot(2,2,4)
plt.scatter(x[0:x.shape[0],2],x[0:x.shape[0],7])			#把x_data和y_data传进来
plt.show()


