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
    if c == 0:
        break
    dataset = pd.read_csv("D:\\stocks\\" + file, encoding='gbk')
    num = dataset.to_numpy()
    if num.shape[0] == 0:
        continue
    for i in range(0, num.shape[0], 5):
        if i + GAP1 + GAP2 < num.shape[0]:
            all += 1
            if num[i, 0].startswith('2020'):
                xs_test.append((num[i:i+GAP1, 1]/num[i, 1] - 1) * 100)
            else:
                xs.append((num[i:i+GAP1, 1]/num[i, 1] - 1) * 100)
                if (num[i+GAP1+GAP2,1] > num[i+GAP1, 1]) * 1.1 :
                    ys.append(1)
                else : ys.append(0)
# num_points = 100
# dimensions = 60
# points = np.random.uniform(0, 1000, [num_points, dimensions])
points = np.array(xs)

def input_fn():
    return tf.compat.v1.train.limit_epochs(
        tf.convert_to_tensor(points, dtype=tf.float32), num_epochs=1)


num_clusters = 10
kmeans = tf.compat.v1.estimator.experimental.KMeans(
    num_clusters=num_clusters, use_mini_batch=False)

# train
num_iterations = 10
previous_centers = None
for _ in range(num_iterations):
    kmeans.train(input_fn)
    cluster_centers = kmeans.cluster_centers()
    if previous_centers is not None:
        print('delta:', cluster_centers - previous_centers)
    previous_centers = cluster_centers
    print('score:', kmeans.score(input_fn))
print('cluster centers:', cluster_centers)
# kmeans.export_saved_model('./test',serving_input_receiver_fn=tf.estimator.export.TensorServingInputReceiver)
# map the input points to their clusters
cluster_indices = list(kmeans.predict_cluster_index(input_fn))
js = [[] for x in range(10)]
for i, point in enumerate(points):
    cluster_index = cluster_indices[i]
    center = cluster_centers[cluster_index]
    # print('is in cluster',cluster_index)
    js[cluster_index].append(ys[i])
for i in range(len(js)):
    print(sum(js[i])/len(js[i]))