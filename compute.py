import numpy as np
import pandas as pd
import os 
import tensorflow as tf
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

GAP1 = 60
GAP2 = 20
all = 0
g20 = 0
g30 = 0
xs = []
ys = []
yes = []
xs_test = []
ys_test = []
sc = MinMaxScaler(feature_range=(0, 1)) 
c = 100
for file in os.listdir("D:\\stocks"):
    if file.startswith('sz.30'):
        continue
    # print(file)
    c -= 1
    if c== 0:
        break
    dataset = pd.read_csv("D:\\stocks\\" + file, encoding='gbk')
    num = dataset.to_numpy()
    if num.shape[0] == 0:
        continue
    for i in range(0,num.shape[0],5):
        
        if i + GAP1 + GAP2 < num.shape[0]:
            all += 1
            if num[i,0].startswith('2020'):
                xs_test.append((num[i:i+GAP1,1]/num[i,1] - 1) * 100)
            else:
                xs.append((num[i:i+GAP1,1]/num[i,1] - 1) * 100)
            b = num[i+GAP1,1]
            s = num[i+GAP1 + GAP2,1]
            if s / b > 1.2:
                g20 += 1
            if s/b > 1.2:
                g30 += 1
                if num[i,0].startswith('2020'):
                    ys_test.append(1)
                else:
                    ys.append(1)
                    yes.append((num[i:i+GAP1,1]/num[i,1] - 1) * 100)
            else:
                if num[i,0].startswith('2020'):
                    ys_test.append(0)
                else:
                    ys.append(0)

yes = [val for val in yes for i in range(5)]
xs.extend(yes)
ys.extend(np.ones(len(yes)).tolist())
print(len(xs), len(ys), sum(ys)/len(ys))
xs = np.array(xs)
ys = np.array(ys)
shuffle_ix = np.random.permutation(np.arange(len(xs)))
xs = xs[shuffle_ix]
ys = ys[shuffle_ix]
xs_test = np.array(xs_test)
ys_test = np.array(ys_test)
model = tf.keras.Sequential([
    # tf.keras.layers.Flatten(input_shape=(1,60)),
    tf.keras.layers.Dense(20,input_shape=(60,),activation="relu"),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(2,activation="softmax")
])
# checkpoint_save_path = "g60-30"
# if os.path.exists(checkpoint_save_path + '.index'):
#     print('-------------load the model-----------------')
#     model.load_weights(checkpoint_save_path)

#设置训练参数
model.compile(
    optimizer=tf.keras.optimizers.Adam(0.001),
    loss="sparse_categorical_crossentropy",
    metrics=['accuracy']
)

# cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_save_path,
#                                                  save_weights_only=True,
#                                                  save_best_only=True,
#                                
#                   monitor='val_loss')
print(xs.shape,ys.shape, g30, g30/len(xs))
xs = xs.astype('float64')
xs_test = xs_test.astype('float64')
#训练并查看训练进度
history = model.fit(xs,ys,epochs=500,validation_data=(xs_test, ys_test), validation_freq=1)
model.save('the_save_model.h5')
model.summary()
