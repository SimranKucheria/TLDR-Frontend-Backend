import requests
from multiprocessing import Pool
import numpy as np
from sklearn.cluster import KMeans
import re
from sklearn.metrics import pairwise_distances_argmin_min
import time
from TextSummarization.baas import generate_sentence_embeddings
from transformers import BertTokenizer, BertModel
import json

def req(sentence):
    #body = requests.get("http://localhost:8000/embedding/",params={'sentence': sentence})
    #return body.json()["sentence_embedding"]
     # Load pre-trained model tokenizer (vocabulary)    
    # Load pre-trained model (weights)
    print(sentence)
    model = BertModel.from_pretrained('bert-base-uncased',
                                    output_hidden_states = True, # Whether the model returns all hidden-states.
                                    )
    sentence_embedding = generate_sentence_embeddings(model,sentence)
    #print(sentence_embedding)
    sentence_embedding = {"sentence_embedding":sentence_embedding}
    #print(sentence_embedding['sentence_embedding'].shape)
    return sentence_embedding['sentence_embedding']

def clean(sentences):
    sentences= [re.sub("\\n","",i) for i in sentences.values()]
    return sentences


def gen_summary(sentences,n_clusters):
    start = time.time()
    # sentences = sentences.split(".")
    # sentences = [token.strip() for token in sentences if token!='']
    i = 0
    #rem = len(sentences)%4
    #vectors = []
    sentence_embed=req(sentences.values())
    '''
    if rem!=0:
        with Pool(rem) as p:
            vectors.extend(p.map(req,sentences[0:rem]))
    for i in range(rem,len(sentences),4):
        with Pool(4) as p:
            vectors.extend(p.map(req, sentences[i:i+4]))
    '''
    vectors = np.array(sentence_embed)
    print(vectors.shape)
    end = time.time()
    print(end-start)    
    print(n_clusters)
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

"""
    start = time.time()
    with open("data.txt","r") as f:
        s1 = f.read()
        s1 = clean(s1)
        sentences = s1.split(".")
        sentences = [token for token in sentences if token!='']
        i = 0
        rem = len(sentences)%8
        vectors = []
        if rem!=0:
            with Pool(rem) as p:
               vectors.extend(p.map(req,sentences[0:rem]))
        for i in range(rem,len(sentences),8):
            with Pool(8) as p:
               vectors.extend(p.map(req, sentences[i:i+8]))
        vectors = np.array(vectors)
        print(vectors.shape)
        end = time.time()
        print(end-start)
        n_clusters = int(np.ceil(len(vectors)/4))
        kmeans = KMeans(n_clusters=n_clusters, random_state=0)
        kmeans = kmeans.fit(vectors)
        avg = []
        closest = []
        for j in range(n_clusters):
            idx = np.where(kmeans.labels_ == j)[0]
            avg.append(np.mean(idx))
        closest, _ = pairwise_distances_argmin_min(kmeans.cluster_centers_,vectors)
        ordering = sorted(range(n_clusters), key=lambda k: avg[k])
        summary = '.'.join([sentences[closest[idx]] for idx in ordering])
        print('Clustering Finished')
        print(summary)

"""

