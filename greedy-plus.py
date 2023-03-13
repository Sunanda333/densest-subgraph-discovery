pip install networkx==1.9.1 
pip install matplotlib==2.2.3 

import time
import numpy as np
import copy
import networkx as nx
import matplotlib.pyplot as plt from scipy.io
import mmread

def maxDensity(dic): 
    score=0
    density=0 
    if(len(dic)<=1):
        return score, density 
    a=0
    for i in dic.keys(): 
        a+=len(dic[i])
        score=a/(2.0*len(dic)) 
        density=a/(len(dic)*(len(dic)-1)) 
        return score, density

def remove(node,dic,deg):
    for i in dic[node]:
        (dic[i]).remove(node) 
        deg[i]=deg[i]-1

    del dic[node]
    del deg[node]

def calculate(): 
    dicPerm={} 
    degPerm={}
    for i in range(len(cols)):
        if cols[i] not in dicPerm.keys():
            dicPerm[cols[i]]=[]
            degPerm[cols[i]]=0 
        dicPerm[cols[i]].append(rows[i]) 
        degPerm[cols[i]]+=1
    return dicPerm,degPerm

def graphPlot(G, subg): 
    values = []
    sizes = []
    for node in G.nodes():
        if node in subg: 
            values.append('red')
            sizes.append(50) 
        else:
            values.append('blue')
            sizes.append(50)

    plt.figure(1,figsize=(15,15))
    nx.draw_networkx(G, node_color=values, node_size = sizes, with_labels=False, font_color='white', font_weight=600) 
    nx.draw_networkx(G, node_color=values, with_labels=False, font_color='white', font_weight=600) 
    plt.axis('off')
    plt.savefig('/content/plt.png')

# A = mmread("karate.mtx")
# A = mmread("data.mtx")
A = mmread("uk.mtx")
# A = mmread("delaunay_n10.mtx") 
rows, cols = A.nonzero()

def greedyPlus(T):
    start_time = time.process_time() 
    maxDensScore=0
    maxDens=0
    subgraph=[]
    load = [0] * A.shape[0] 
    dicPerm, degPerm = calculate() 
    for i in range(T):
        deg = copy.deepcopy(degPerm) 
        dic = copy.deepcopy(dicPerm) 
        while(len(deg)>0):
            minDeg=float('inf') 
            minNode = -1
            for j in deg.keys():
                if(deg[j]+load[j] < minDeg): 
                    minDeg = deg[j]+load[j] 
                    minNode = j
            load[minNode] = load[minNode]+deg[minNode] 
            remove(minNode,dic,deg)
            (score, density) = maxDensity(dic)
            
            if (score>maxDensScore):
                maxDensScore=score 
                maxDens=density
                subgraph = list(dic.keys())
    end_time = time.process_time()
    print("Time taken for the algorithm : ", end_time - start_time) 
    print("Subgraph has the following nodes : ", subgraph)
    print("Subgraph has the following number of nodes : ", len(subgraph))
    print("Maximum density score objective : ", maxDensScore) 
    print("Maximum density : ", maxDens)
    G = nx.Graph(A)
    subg = G.subgraph(subgraph)
    return graphPlot(G,subg)