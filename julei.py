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
ys1 = []
ys2 = []
yes = []
xs_test = []
ys_test = []
files = []
dates = []
sc = MinMaxScaler(feature_range=(0, 1))
for file in os.listdir("/Users/gentlewen/Desktop/stocksdata"):
    if file.startswith('sz.30'):
        continue
    # if len(xs) > 20000:
    #     break
    dataset = pd.read_csv("/Users/gentlewen/Desktop/stocksdata/" + file, encoding='gbk')
    num = dataset.to_numpy()
    if num.shape[0] == 0:
        continue
    for i in range(int(num.shape[0]/4), num.shape[0], 5):
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
                files.append((file,num[i, 0]))
                if num[i+GAP1+GAP2,1] > num[i+GAP1, 1] * 1.2 :
                    ys.append(1)
                else : ys.append(0)
                if num[i+GAP1+GAP2,1] > num[i+GAP1, 1] * 1.3 :
                    ys1.append(1)
                else : ys1.append(0)
                if num[i+GAP1+60,1] > num[i+GAP1, 1] * 1.3 :
                    ys2.append(1)
                else : ys2.append(0)
# num_points = 100
# dimensions = 60
# points = np.random.uniform(0, 1000, [num_points, dimensions])
print(sum(ys), sum(ys1), sum(ys2))
xs = np.array(xs)
ys = np.array(ys)
ys1 = np.array(ys1)
ys2 = np.array(ys2)
shuffle_ix = np.random.permutation(np.arange(len(xs)))
xs = xs[shuffle_ix]
ys = ys[shuffle_ix]
ys1 = ys2[shuffle_ix]
ys2 = ys2[shuffle_ix]
points = np.array(xs)

def input_fn():
    return tf.compat.v1.train.limit_epochs(
        tf.convert_to_tensor(points, dtype=tf.float32), num_epochs=1)


num_clusters = 50
kmeans = tf.compat.v1.estimator.experimental.KMeans(
    num_clusters=num_clusters, use_mini_batch=False)

# train
num_iterations = 80
for i in range(num_clusters):
    fs = '/Users/gentlewen/Desktop/image1/'+str(i)
    if os.path.exists(fs):
        shutil.rmtree(fs)
    os.mkdir(fs)
previous_centers = None
for i in range(num_iterations):
    kmeans.train(input_fn)
    cluster_centers = kmeans.cluster_centers()
    if previous_centers is not None:
        print('delta:', cluster_centers - previous_centers)
    previous_centers = cluster_centers
    print('score:', kmeans.score(input_fn),i)
print('cluster centers:', cluster_centers)
# kmeans.export_saved_model('./test',serving_input_receiver_fn=tf.estimator.export.TensorServingInputReceiver)
# map the input points to their clusters
cluster_indices = list(kmeans.predict_cluster_index(input_fn))
js = [[] for x in range(num_clusters)]
js1 = [[] for x in range(num_clusters)]
js2 = [[] for x in range(num_clusters)]
fss = [[] for x in range(num_clusters)]
for i, point in enumerate(points):
    cluster_index = cluster_indices[i]
    center = cluster_centers[cluster_index]
    # print('is in cluster',cluster_index)
    js[cluster_index].append(ys[i])
    fss[cluster_index].append(files[i])
    js1[cluster_index].append(ys1[i])
    js2[cluster_index].append(ys2[i])
    # if i > 2000:
    #     continue
    # plt.clf()
    # # plt.plot([x for x in range(len(point))], point,':m')
    # plt.plot([x for x in range(len(point))], sh[i],'--g')
    # plt.savefig('/Users/gentlewen/Desktop/image1/'+str(cluster_index)+"/" +str(i)+".png")
print(sum(ys)/len(ys),sum(ys1)/len(ys1),sum(ys2)/len(ys2),'\n----------',len(ys))
cs = 0
win0 = 0
win1 = 0
win2 = 0
for i in range(len(js)):
    cs += len(js[i])
    y0 = 0
    y1 = 0
    y2 = 0
    if len(js[i]) > 0:
        y0 = sum(js[i])/len(js[i])
        y1 = sum(js1[i])/len(js1[i])
        y2 = sum(js2[i])/len(js2[i])
    print(i, y0, len(js[i]), y1, len(js1[i]) ,y2, len(js2[i]))
    if y0 > 0.7:
        win0 += len(js[i])
        print(fss[i])
    if y1 > 0.7:
        win1 += len(js1[i])
    if y2 > 0.7:
        win2 += len(js2[i])
print(cs, win0, win0/cs, win1, win1/cs, win2, win2/cs)