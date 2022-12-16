#!/usr/bin/env python
# coding: utf-8

# # Imports

# In[1]:


import pandas as pd 
import matplotlib.pyplot as plt
import networkit as nk
import tqdm
import numpy as np
import glob
import time
import json

from sklearn.metrics import ndcg_score
from sklearn.preprocessing import MinMaxScaler
from scipy.stats import kendalltau, spearmanr


# # Load data

# In[2]:


HepPh_df = pd.read_csv("../data/HepPh/ca-HepPh.txt", sep="\t", on_bad_lines="skip", header=None, names=["source", "target"])[4:]

HepPh_df["source"] = HepPh_df["source"].astype(int)
HepPh_df["target"] = HepPh_df["target"].astype(int)

HepPh_df.head()


# # Generate networkit graph

# In[3]:


g = nk.Graph(directed=False)

for row in HepPh_df[["source", "target"]].to_records(index=False).tolist():
    g.addEdge(row[0], row[1], addMissing=True)

g.removeSelfLoops()


# # Network metrics

# In[4]:


results = {
            "dataset": "HepPh",
            "directed": False,
            "nodes": len(set(HepPh_df["source"].to_list() + HepPh_df["target"].to_list())),
            "edges": int(g.numberOfEdges()/2)
        }

# Density
results["density"] = nk.graphtools.density(g)
print(f"Density: ", results["density"])

# Average clustering coefficient
results["average_clustering_coefficient"] = nk.globals.ClusteringCoefficient().avgLocal(g, 10**6) 
print(f"Average clustering coefficient: ", results["average_clustering_coefficient"])

# Diameter
diameter = nk.distance.Diameter(g, algo=nk.distance.DiameterAlgo.Exact, nSamples=10**5)
diameter.run()
results["diameter"] = diameter.getDiameter() 
print(f"Diameter: ", results["diameter"])


# # Centrality measures

# In[5]:


def get_degree_centrality(g):
    start_time = time.process_time()
    
    degree = nk.centrality.DegreeCentrality(g)
    degree.run()
    
    end_time = time.process_time()
    
    return degree, (end_time - start_time)

def get_closeness_centrality(g):
    start_time = time.process_time()
    
    closeness = nk.centrality.Closeness(g, True, nk.centrality.ClosenessVariant.Generalized)
    closeness.run()
    
    end_time = time.process_time()
    
    return closeness, (end_time - start_time)

def get_topk_closeness_centrality(g, first_heu=False, second_heu=False, k=5):
    start_time = time.process_time()

    topk_closeness = nk.centrality.TopCloseness(g, k=k, first_heu=first_heu, sec_heu=second_heu)
    topk_closeness.run()
    
    end_time = time.process_time()

    return topk_closeness, (end_time - start_time)

centrality = {}
results["time_elapsed"] = {}

# Degree centrality
centrality["degree"], results["time_elapsed"]["degree"] = get_degree_centrality(g)

# Closeness centrality
centrality["closeness"], results["time_elapsed"]["closeness"] = get_closeness_centrality(g)

# Topk closeness centrality
ks = [5, 10, 50, 100, int(results["nodes"]/2)]

centrality["topkcloseness_0"] = {}
centrality["topkcloseness_1"] = {}
results["time_elapsed"]["topkcloseness_0"] = {}
results["time_elapsed"]["topkcloseness_1"] = {}

for k in ks:
    centrality["topkcloseness_0"][k], results["time_elapsed"]["topkcloseness_0"][k] = get_topk_closeness_centrality(g, False, False, k)
    centrality["topkcloseness_1"][k], results["time_elapsed"]["topkcloseness_1"][k] = get_topk_closeness_centrality(g, False, True, k)


# In[6]:


print(results)


# # Experiments

# ## Preprocess

# In[7]:


normalised_scores = {}
nodes = {}

# Degree centrality
scaler = MinMaxScaler()
normalised_scores["degree"] = scaler.fit_transform(np.array([row[1] for row in centrality["degree"].ranking()]).reshape(-1, 1)).flatten()
nodes["degree"] = [row[0] for row in centrality["degree"].ranking()]

# Closeness centrality
scaler = MinMaxScaler()
normalised_scores["closeness"] = scaler.fit_transform(np.array([row[1] for row in centrality["closeness"].ranking()]).reshape(-1, 1)).flatten()
nodes["closeness"] = [row[0] for row in centrality["closeness"].ranking()]

# Topk closeness centrality
normalised_scores["topkcloseness_0"], normalised_scores["topkcloseness_1"] = {}, {}
nodes["topkcloseness_0"], nodes["topkcloseness_1"] = {}, {}

for k in ks:
    scaler = MinMaxScaler()
    normalised_scores["topkcloseness_0"][k] = scaler.fit_transform(np.array(centrality["topkcloseness_0"][k].topkScoresList()).reshape(-1, 1)).flatten()
    nodes["topkcloseness_0"][k] = centrality["topkcloseness_0"][k].topkNodesList()

    scaler = MinMaxScaler()
    normalised_scores["topkcloseness_1"][k] = scaler.fit_transform(np.array(centrality["topkcloseness_1"][k].topkScoresList()).reshape(-1, 1)).flatten()
    nodes["topkcloseness_1"][k] = centrality["topkcloseness_1"][k].topkNodesList()


# ## LabelBinarizer function

# In[8]:


def get_label_binarized(labels, node_count, k):
    b = np.full((k, node_count), 0, dtype="byte")
    b[np.arange(k), labels] = 1
    
    return b


# ## NDCG degree to (top-k) closeness

# In[13]:


ndcg_scores = {}

for k in ks[:-1]:
    ndcg_scores[k] = {}
    
    for centrality_measure in ["closeness", "topkcloseness_0", "topkcloseness_1"]:
        
        y_true = get_label_binarized(nodes["degree"][:k], g.numberOfNodes(), k)
        sample_weight = normalised_scores["degree"][:k]
        
        if "topk" in centrality_measure:
            y_score = get_label_binarized(nodes[centrality_measure][k], g.numberOfNodes(), k)
            
        else:
            y_score = get_label_binarized(nodes[centrality_measure][:k], g.numberOfNodes(), k)

        ndcg_scores[k][centrality_measure] = ndcg_score(y_true, y_score, sample_weight=sample_weight)
    
results["ndcg_degree"] = ndcg_scores

print(pd.DataFrame(ndcg_scores).T)


# ## NDCG closeness to (top-k) closeness

# In[15]:


ndcg_scores = {}

for k in ks[:-1]:
    ndcg_scores[k] = {}
    
    y_score = get_label_binarized(nodes["closeness"][:k], g.numberOfNodes(), k)
    sample_weight = normalised_scores["closeness"][:k]
    
    for centrality_measure in ["topkcloseness_0", "topkcloseness_1"]:
        y_true = get_label_binarized(nodes[centrality_measure][k], g.numberOfNodes(), k)
            
        ndcg_scores[k][centrality_measure] = ndcg_score(y_true, y_score, sample_weight=sample_weight)
    
results["ndcg_closeness"] = ndcg_scores

print(pd.DataFrame(ndcg_scores).T)


# ## Spearman rank correlation

# In[10]:


spearmanr_corr = {}

for k in ks:
    spearmanr_corr[k] = {}
    
    y_true = pd.DataFrame({"nodes": nodes["degree"][:k], "ranking_x": normalised_scores["degree"][:k]})

    for centrality_measure in ["closeness", "topkcloseness_0", "topkcloseness_1"]:
        
        if "topk" in centrality_measure:
            y_score = pd.DataFrame({"nodes": nodes[centrality_measure][k], "ranking_y": normalised_scores[centrality_measure][k]})
            
        else:
            y_score = pd.DataFrame({"nodes": nodes[centrality_measure][:k], "ranking_y": normalised_scores[centrality_measure][:k]})

        y_df = y_true.merge(y_score, how="outer", on="nodes").fillna(0)

        corr, _ = spearmanr(y_df["ranking_x"], y_df["ranking_y"])
        spearmanr_corr[k][centrality_measure] = corr
    
results["spearmanr"] = spearmanr_corr

print(pd.DataFrame(spearmanr_corr).T)


# ## Kendalltau rank correlation

# In[11]:


kendalltau_corr = {}

for k in ks:
    kendalltau_corr[k] = {}
    
    y_true = pd.DataFrame({"nodes": nodes["degree"][:k], "ranking_x": normalised_scores["degree"][:k]})

    for centrality_measure in ["closeness", "topkcloseness_0", "topkcloseness_1"]:
        
        if "topk" in centrality_measure:
            y_score = pd.DataFrame({"nodes": nodes[centrality_measure][k], "ranking_y": normalised_scores[centrality_measure][k]})
            
        else:
            y_score = pd.DataFrame({"nodes": nodes[centrality_measure][:k], "ranking_y": normalised_scores[centrality_measure][:k]})

        y_df = y_true.merge(y_score, how="outer", on="nodes").fillna(0)

        corr, _ = kendalltau(y_df["ranking_x"], y_df["ranking_y"])
        kendalltau_corr[k][centrality_measure] = 0 if np.isnan(corr) else corr
    
results["kendalltau"] = kendalltau_corr

print(pd.DataFrame(kendalltau_corr).T)


# # Store results

# In[16]:


with open(f"../results/{results['dataset']}_{results['directed']}.json", 'w') as outfile:
    json.dump(results, outfile)


# In[ ]:




