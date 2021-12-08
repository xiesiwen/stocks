import matplotlib.pyplot as plt
import numpy as np

L = 5
lz = [2515,1600,902,1033,3500,3111,1111,2985,3311,1974,2591,3098,2727,3014,2710,3023,1230,3828,1277,3295,2417,2396,
2304,1976,1545,1615,2884,3220,1097,2642,958,1715]
res = []
for i in range(L, len(lz) + 1):
    res.append(np.mean(lz[i-L:i-1]))
print(res)
x = [x for x in range(1,len(res) + 1)]
plt.plot(x,res)
plt.plot(x, [2342 for x in range(0,len(res))])
plt.show()