pip install networkx==1.9.1 
pip install matplotlib==2.2.3

import networkx as nx
import sys
from scipy.io import mmread
#from evaluation_metrics import (density,degree_density,triangle_density) import matplotlib.pyplot as plt
import time

def densestSubgraphObjectiveScore(G): 
    """
    Returns the densest subgraph objective score of the graph density = |E(S)|/|S|
    """
    return G.number_of_edges()/G.number_of_nodes()

def density(G): 
    """
    Returns the density of the graph density = 2*|E(S)|/(|S|*(|S|-1))
    """
    return 2*G.number_of_edges()/float(G.number_of_nodes()*(G.number_of_nodes()- 1))

def degree_density(G): 
    """
    Returns the degree density of the graph degree density = 2*|E(S)|/|S|
    """
    return 2*G.number_of_edges()/float(G.number_of_nodes())

def edge_surplus(G, alpha): 
    """
    Returns the edge surplus of the graph
    edge surplus = |E(S)| - alpha*(|S|*(|S|-1))/2
    """
    return G.number_of_edges() - alpha * ((G.number_of_nodes() * (G.number_of_nodes() - 1))/2.0)

def graphPlot(graph, sub_graph):
    G = nx.Graph(graph)
    subg = G.subgraph(sub_graph) 
    values=[]
    sizes = []
    for node in G.nodes():
        if node in subg: 
            values.append('red') 
            sizes.append(50)
        else: 
            values.append('blue') 
            sizes.append(50)
    plt.figure(1,figsize=(15,15))
    nx.draw_networkx(G, node_color=values, node_size=sizes, with_labels=False, font_color='white', font_weight=600)
    plt.axis('off') 
    plt.savefig('/content/plt.png')

def greedy_quasi_cliques(G, alpha): 
    """
    Returns the subgraph with optimal edge surplus 
    """
    neighbors=G.neighbors
    degrees=G.degree()
    sum_degrees = sum(degrees.values())
    # num_nodes = G.number_of_nodes() 
    nodes=sorted(degrees,key=degrees.get)
    #sum_degrees = 0
    #for k, v in degrees:
    # sum_degrees+=v
    num_nodes = G.number_of_nodes()
    #nodes = sorted(G.degree, key=lambda x: x[1], reverse=True) 
    bin_boundaries=[0]
    curr_degree=0
    for i,v in enumerate(nodes):
        if degrees[v]>curr_degree: 
            print(i,"and",degrees[v]-curr_degree) 
            bin_boundaries.extend([i]*(degrees[v]-curr_degree)) 
            curr_degree=degrees[v]
    node_pos = dict((v,pos) for pos,v in enumerate(nodes)) 
    nbrs=dict((v,set(neighbors(v))) for v in G)
    print(bin_boundaries)
    max_edge_surplus = sum_degrees/2.0 - alpha * ((num_nodes * (num_nodes- 1))/2.0) 
    ind = 0
    for v in nodes: 
        num_nodes -= 1
        while degrees[v] > 0:
            pos=node_pos[v]
            bin_start=bin_boundaries[degrees[v]]
            node_pos[v]=bin_start
            node_pos[nodes[bin_start]]=pos 
            nodes[bin_start],nodes[pos]=nodes[pos],nodes[bin_start] 
            bin_boundaries[degrees[v]] = bin_boundaries[degrees[v]] + 1 
            degrees[v]-=1
        for u in nbrs[v]:
            nbrs[u].remove(v)
            pos=node_pos[u]
            bin_start=bin_boundaries[degrees[u]] 
            node_pos[u]=bin_start
            node_pos[nodes[bin_start]]=pos 
            nodes[bin_start],nodes[pos]=nodes[pos],nodes[bin_start] 
            bin_boundaries[degrees[u]]+=1
            degrees[u]-=1 
            sum_degrees -= 2

        if num_nodes > 0:
            current_edge_surplus = sum_degrees/2.0 - alpha * ((num_nodes *(num_nodes - 1))/2.0)
            if current_edge_surplus > max_edge_surplus:
                max_edge_surplus = current_edge_surplus 
                ind = G.number_of_nodes()-num_nodes

    optimal_nodes = nodes[ind:] 
    return G.subgraph(optimal_nodes)

def main(): 
    """
    # # #
    Main method
    """
    adj = mmread("delaunay_n10.mtx")
    adj = np.asmatrix(adj)
    adj = nx.convert_matrix.from_numpy_matrix(adj) 
    G = nx.from_numpy_matrix(adj)
    G = nx.Graph(adj)
    print ("Number of nodes:", G.number_of_nodes()) 
    print ("Number of edges:", G.number_of_edges()) 
    
    start_time = time.process_time()
    subg = greedy_quasi_cliques(G, 0.80)
    end_time = time.process_time()
    #print ("Degree Density: " + str(degree_density(subg)))

    print ("Graph Density: " + str(density(subg)))
    print ("Densest subgraph objective: " + str(densestSubgraphObjectiveScore(subg)))
    print ("# Nodes: " + str(subg.number_of_nodes())) 
    print ("Number of nodes:", subg.number_of_nodes()) 
    print ("Number of edges:", subg.number_of_edges()) 
    print ("Time taken", end_time - start_time) 
    graphPlot(G, subg)
    
if __name__ == "__main__": 
    main()