import numpy as np
import pandas as pd
import os,shutil
import tensorflow as tf
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

GAP1 = 60
GAP2 = 40
all = 0
g20 = 0
g30 = 0
sh = []
xs = []
ys = []
yes = []
xs_test = []
ys_test = []
sc = MinMaxScaler(feature_range=(0, 1))
c = 50
for file in os.listdir("D:\\stocks"):
    if file.startswith('sz.30'):
        continue
    # print(file)
    c -= 1
    if c == 0 or len(xs) > 6000:
        break
    dataset = pd.read_csv("D:\\stocks\\" + file, encoding='gbk')
    num = dataset.to_numpy()
    if num.shape[0] == 0:
        continue
    for i in range(int(num.shape[0]/4), num.shape[0], 20):
        if i + GAP1 + GAP2 < num.shape[0]:
            all += 1
            if num[i, 0].startswith('2020'):
                xs_test.append((num[i:i+GAP1, 1]/num[i, 1] - 1) * 100)
            else:
                ps = []
                for z in range(i,i+GAP1):
                    # if (num[z, 1] > num[z-1, 1]):
                    #     ps.append(1)
                    # else: ps.append(-1)
                    ps.append((num[z, 1]/num[z-1, 1] -1) * 100)
                xs.append(ps)
                sh.append(num[i:i+GAP1,1])
                if (num[i+GAP1+GAP2,1] > num[i+GAP1, 1]) * 1.2 :
                    ys.append(1)
                else : ys.append(0)
# num_points = 100
# dimensions = 60
# points = np.random.uniform(0, 1000, [num_points, dimensions])
xs = np.array(xs)
ys = np.array(ys)
shuffle_ix = np.random.permutation(np.arange(len(xs)))
xs = xs[shuffle_ix]
ys = ys[shuffle_ix]
points = np.array(xs)

def input_fn():
    return tf.compat.v1.train.limit_epochs(
        tf.convert_to_tensor(points, dtype=tf.float32), num_epochs=1)


num_clusters = 50
kmeans = tf.compat.v1.estimator.experimental.KMeans(
    num_clusters=num_clusters, use_mini_batch=False)

# train
num_iterations = 50
for i in range(num_clusters):
    fs = 'D:/image1/'+str(i)
    if os.path.exists(fs):
        shutil.rmtree(fs)
    os.mkdir(fs)
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
js = [[] for x in range(num_clusters)]
for i, point in enumerate(points):
    cluster_index = cluster_indices[i]
    center = cluster_centers[cluster_index]
    # print('is in cluster',cluster_index)
    js[cluster_index].append(ys[i])
    if i > 2000:
        continue
    plt.clf()
    # plt.plot([x for x in range(len(point))], point,':m')
    plt.plot([x for x in range(len(point))], sh[i],'--g')
    plt.savefig('D:/image1/'+str(cluster_index)+"/" +str(i)+".png")
print(sum(ys)/len(ys))
for i in range(len(js)):
    if len(js[i]) > 0:
        print(i, sum(js[i])/len(js[i]), len(js[i]))