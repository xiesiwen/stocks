import os 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
c = 0
path = "./stock-today/"
sh = pd.read_csv(path + "sh.000001.csv", encoding='gbk').to_numpy()
map = [0 for _ in range(0,len(sh))]
mi = [0 for _ in range(0,len(sh))]
for file in os.listdir(path):
    if file.startswith(('sh.60','sz.00','sz.30','sh.68')):
        dataset = pd.read_csv(path + file, encoding='gbk')
        num = dataset.to_numpy()
        if len(num) >= 225 and num[0,0] == sh[0,0]:
            for i in range(30, 225):
                if num[i, 1] >= np.max(num[0:i,1]):
                    map[i] += 1
                if num[i, 1] <= np.min(num[0:i,1]):
                    mi[i] += 1
        c+=1
print(c)
v = map
L = 5
res = []
rm = []
for i in range(L, len(v)):
    res.append(np.mean(v[i-L+1:i+1]))
for i in range(L, len(mi)):
    rm.append(np.mean(mi[i-L+1:i+1]))
x = [x for x in range(L, len(map))]
plt.plot(x,res)
plt.plot(x,rm)
plt.plot(x,sh[L:,1] - 3350)
plt.show()

# num = sh.to_numpy()[L-1:]
# if len(num) != len(res):
#     print("error")
# else:
#     print("equals")
# b = 0
# r = []
# z = 0
# R = 1
# for i in range(0, len(res)):
#     if res[i] < c*0.333 and b == 0:
#         b = num[i, 1]
#         print("buy " + num[i,0])
#     if res[i] > c*0.666 and b > 0:
#         w = (num[i,1]/b - 1) * 100
#         R *= (num[i,1]/b)
#         if w > 0:
#             z += 1
#         print("sale " + num[i,0], w)
#         r.append(w)
#         b = 0
# print(r, z/len(r), R)
