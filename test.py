
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import time
import os 
from tensorflow.python.keras.optimizer_v2.adam import Adam
def getK(Y):
    X = (np.arange(Y.shape[0]) + 1) /2
    X = np.array(X, dtype=np.float)
    Y = np.array(Y, dtype=np.float)
    model = tf.keras.Sequential()
    model.add(tf.keras.layers.Dense(1, input_shape=(1, )))
    model.compile(optimizer=Adam(0.01), loss='mse')
    model.fit(X, Y, epochs=4000, verbose=0)
    return model.get_weights()[0][0][0]   

def r2(x):
    return round(x, 2)

def compute(name):
    dataset = pd.read_csv("D:\\stocks\\" + name, encoding='gbk')
    num = dataset.to_numpy()
    len_ = int(num.shape[0] / 5)
    result = []
    gap = 40
    g = int(gap/2)
    for i in range(len_):
        if i*5 + gap*2 > num.shape[0]:
            break
        d = gap + i*5
        start = time.clock()
        k1 = getK((num[i*5 : i*5 + gap, 1] / num[i*5, 1] - 1) * 100)
        k2 = getK((num[i*5 + g : i*5 + gap, 1] / num[i*5 + g, 1] - 1) * 100)
        print(k1, k2, i, len_)
        if (k1 > 0 and k2 >= k1):
            p = num[d, 1]
            r = [num[i*5][0], num[d][0], r2(k1), r2(k2), r2((num[d + 5][1] / p -1)*100), r2((num[d + 10][1] / p -1)*100), r2((num[d + 20][1] / p -1) * 100),r2((np.max(num[d: 20 + d, 1]) /p - 1) * 100), r2((np.min(num[d: 20 + d, 1])/p-1)*100)]
            print('find!!!')
            result.append(r)
            
    rs = pd.DataFrame(np.array(result))
    rs.to_csv("D:\\res1\\"+name, index=False)

for file in os.listdir("D:\\test"):
      compute(file)  
# plt.figure()									#打印样本点
# plt.scatter(X,Y)						#把x_data和y_data传进来
# plt.plot(X,model.predict(X),'r*',lw = 5)
# plt.show()