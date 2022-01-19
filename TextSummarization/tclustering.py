import requests
from multiprocessing import Pool
import numpy as np
from sklearn.cluster import KMeans
import re
from sklearn.metrics import pairwise_distances_argmin_min
import time
from TextSummarization.baas import generate_sentence_embeddings
from transformers import BertModel
import json

def req(sentence):
    model = BertModel.from_pretrained('bert-base-uncased',
                                    output_hidden_states = True, # Whether the model returns all hidden-states.
                                    )
    sentence_embedding = generate_sentence_embeddings(model,sentence)
    sentence_embedding = {"sentence_embedding":sentence_embedding}
    return sentence_embedding['sentence_embedding']

def clean(sentences):
    sentences= [re.sub("\\n","",i) for i in sentences.values()]
    return sentences

def gen_summary(sentences,n_clusters):
    sentence_embed=req(sentences.values())
    vectors = np.array(sentence_embed)
    kmeans = KMeans(n_clusters=n_clusters, random_state=0)
    kmeans = kmeans.fit(vectors)
    avg = []
    closest = []
    for j in range(n_clusters):
        idx = np.where(kmeans.labels_ == j)[0]
        avg.append(np.mean(idx))
    closest, _ = pairwise_distances_argmin_min(kmeans.cluster_centers_,vectors)
    clustering_ordering = sorted(range(n_clusters), key=lambda k: avg[k])
    ordering = [closest[idx].item() for idx in clustering_ordering]
    n_ordering =[]
    for i in ordering:
        n_ordering.append(i)
        if i==0:
            n_ordering.append(i+1)
            n_ordering.append(i+2)
        if i==1:
            n_ordering.append(i-1)
            n_ordering.append(i+1)
            n_ordering.append(i+2)
        if i == len(sentences)-1:
            n_ordering.append(i-1)
            n_ordering.append(i-2)
        if i == len(sentences)-2:
            n_ordering.append(i-1)
            n_ordering.append(i-2)
            n_ordering.append(i+1)
        if i!=0 and i!=len(sentences)-1 and i!=1 and i!=len(sentences)-2:
            n_ordering.append(i-1)
            n_ordering.append(i-2)
            n_ordering.append(i+1)
            n_ordering.append(i+2)
    n_ordering=set(n_ordering)
    ordering = sorted(list(n_ordering))
    summary_sentences = {j[0]:j[1] for i,j in enumerate(sentences.items()) if i in ordering}
    print(summary_sentences)
    print('Clustering Finished')
    return summary_sentences        

