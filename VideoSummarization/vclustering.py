import shutil
from typing import OrderedDict
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min
import scipy
from VideoSummarization.extract import get_feat
import cv2
import os 
import shutil
from helper import dirgetcheck

def cosine_distance_between_two_images(v1, v2):
    return (1- scipy.spatial.distance.cosine(v1, v2))

def getfr(ip):
    stream = cv2.VideoCapture(ip)
    fps = stream.get(cv2.CAP_PROP_FPS)  
    frame_count = int(stream.get(cv2.CAP_PROP_FRAME_COUNT))
    dur = frame_count/fps
    lt = [24,20,16,12,8,4]
    i = 0
    while i < len(lt) and dur * lt[i] > 14000:
        i = i+1
    if i < len(lt):
        return lt[i]
    else:
        return lt[-1]

def redundancy_checker(ordering,op):
    final_list=ordering.copy()
    for i in range(len(ordering)-1):
        if cosine_distance_between_two_images(op[ordering[i]],op[ordering[i+1]]) > 0.95:
            final_list.remove(ordering[i])
    return final_list
        
def clean(dir1,op):
    if os.path.isfile(op):
        os.remove(op)
    shutil.rmtree(dir1)
    os.makedirs(dir1)

def vsum(ip,n_clusters):
    dir1 = dirgetcheck('Data','output_images')
    dir2 = dirgetcheck('Data','feat_op')
    fr = getfr(ip)
    opn = ip.split("\\")[-1].split('.')[0]
    opn = opn.replace(r'\.','')
    opn = opn.replace('\\','')
    opn = opn.replace(':','')
    output_file = opn+'op.npy'
    output_file = os.path.join(dir2,output_file)
    clean(dir1,output_file) 
    get_feat(ip,fr,output_file)
    print(output_file)
    op = np.load(output_file)
    kmeans = KMeans(n_clusters=n_clusters, random_state=0)
    kmeans = kmeans.fit(op)
    closest = []
    closest, _ = pairwise_distances_argmin_min(kmeans.cluster_centers_,op)
    ordering = [closest[idx].item() for idx in range(n_clusters)]
    keyframes_vectors = [op[i] for i in ordering]
    print('Clustering Finished')
    return ordering,fr,op.shape[0], keyframes_vectors

