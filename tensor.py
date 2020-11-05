import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

arrays1 = []
arrays2 = []
for i in range(5000):
    k1 = np.random.random(1)
    x = np.linspace(1, 60, 60)[:, np.newaxis]
    noise = np.random.normal(0, 0.02, x.shape)
    y = (x**2) * k1[0] + noise

    y1 = x*np.random.random(1)[0] + np.random.normal(0, 0.02, x.shape)
    arrays1.append(y.tolist())
    arrays1.append(y1.tolist())
    arrays2.append(1)
    arrays2.append(0)

xs = np.array(arrays1)
ys = np.array(arrays2)
shuffle_ix = np.random.permutation(np.arange(len(xs)))
xs = xs[shuffle_ix]
ys = ys[shuffle_ix]

model = tf.keras.Sequential([
    tf.keras.layers.Flatten(input_shape=(60,1)),
    tf.keras.layers.Dense(10,activation="relu"),
    tf.keras.layers.Dense(2,activation="softmax")
])

#设置训练参数
model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=['accuracy']
)
print(xs.shape, ys.shape)
#训练并查看训练进度
history = model.fit(xs,ys,epochs=500)
model.save('the_save_model.h5')
# new_model = tf.keras.models.load_model('the_save_model.h5')
x = np.linspace(1, 60, 60)[:, np.newaxis]
k1 = 0.6
k2 = 0.4
noise = np.random.normal(0, 0.02, x.shape)
y1 = (x**2) * k1 + noise
y2 = x * k2 + noise
rs = [y1.tolist(), y2.tolist()]
y_predict2 = model.predict(np.array(rs))
print(y_predict2)

# plt.scatter(x,y)
# plt.plot(x,y_predict,'r')
# plt.show()