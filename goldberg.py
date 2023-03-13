pip install PyMaxflow
pip install scipy
pip install networkx==1.9.1
pip install matplotlib==2.2.3

import maxflow
import time
import scipy
from scipy import io
import networkx as nx
import matplotlib.pyplot as plt

def graphPlot(graph, subg, fileName): 
    values = []
    sizes = []
    G = nx.Graph(graph) 
    for node in G.nodes():
        if node in subg: 
            values.append('red') 
            sizes.append(50)
        else: 
            values.append('blue') 
            sizes.append(50)
        plt.figure(1,figsize=(15,15))
        nx.draw_networkx(G, node_color=values, node_size = sizes, with_labels=False, font_color='white', font_weight=600)
        # nx.draw_networkx(G, node_color=values, with_labels=False, font_color='white', font_weight=600)
        plt.axis('off') 
        plt.savefig('content/outputs/'+fileName+'.png')

def Find_Density(graph, adj_matrix):
    ''' Finds the density of the given graph nodes.''' 
    # print(type(graph), type(adj_matrix))
    # graph = [x - 1 for x in graph]
    subgraph = adj_matrix[graph]
    subgraph = subgraph.transpose()[graph]
    # print(subgraph.shape)
    n_edges = subgraph.getnnz()/2
    n_nodes = len(graph)
    density_score = n_edges/n_nodes
    density = 2*n_edges / (n_nodes * (n_nodes-1)) 
    print("subgraph: nodes, edges, density, density score:",n_nodes, n_edges, density, density_score) 
    return density, density_score

def Find_Densest_Subgraph(number_of_nodes,number_of_edges, adj_matrix): 
    ''' This function performs the binary search of the density of subgraph and finds the densest subgraph.'''
    min_degree = 0
    max_degree = number_of_edges
    subgraph = []
    difference = 1.0/(number_of_nodes*(number_of_nodes - 1)) 
    # print("Diff: ",difference)
    print("Computing Densest Subgraph...") 
    while(max_degree - min_degree >= difference):
        least_density = (max_degree + min_degree)/2.0
        source_segment = make_graph(number_of_nodes, number_of_edges, adj_matrix, least_density)
        if(source_segment == []): 
            max_degree = least_density
        else:
            min_degree = least_density
            subgraph = source_segment
        #print(subgraph)
        # print("min, max: ", min_degree, max_degree)
        return subgraph
        
counter=0;
def make_graph(number_of_nodes, number_of_edges, adj_matrix, least_density):
    ''' Constructs the network as per the specifications given by Goldberg'''
    print("Runing iteration ", ++counter)
    graph = maxflow.Graph[float](number_of_nodes, number_of_edges) 
    nodes = graph.add_nodes(number_of_nodes)
    #print(nodes)
    degrees = {}
    #print(degrees)
    # print(adj_matrix.shape, adj_matrix.getnnz()) #nodes, edges
    for i in range(number_of_nodes):
        for j in range(i+1,number_of_nodes):
            if adj_matrix[i,j]>0:
                graph.add_edge(nodes[i], nodes[j], 1,1) 
                if str(i) in degrees:
                    degrees[str(i)] += 1 
                else:
                    degrees[str(i)] = 1 

                if str(j) in degrees:
                    degrees[str(j)] += 1 
                else:
                    degrees[str(j)] = 1 

    for i in range(number_of_nodes): 
        if str(i) not in degrees:
            degrees[str(i)] = 0 
            graph.add_tedge(nodes[i], number_of_edges, number_of_edges + 2*least_density - degrees[str(i)])
            #print("s -- ",number_of_edges,"-->", nodes[i], "--",number_of_edges + 2*least_density - degrees[str(i)], "--> t")

    '''Computes the max-flow in the graph'''
    graph.maxflow()
    '''The following section of code finds which node belongs to which cutset.'''
    source_segment = [] 
    for i in nodes:
        #print(nodes[i] ,"--->", graph.get_segment(nodes[i]))
        if(graph.get_segment(nodes[i]) == 0): 
            source_segment.append(nodes[i])
            #print degrees
    return source_segment

adj_matrix = scipy.io.mmread("content/karate.mtx").tocsr()
# adj_matrix = scipy.io.mmread("content/delaunay_n10.mtx").tocsr() # adj_matrix = scipy.io.mmread("content/data.mtx").tocsr()
# adj_matrix = scipy.io.mmread("content/uk.mtx").tocsr()
# print(adj_matrix)
number_of_nodes = adj_matrix.shape[0] #nodes
number_of_edges = adj_matrix.getnnz()/2 #edges
print('#Nodes: ', number_of_nodes, '#Edges: ', number_of_edges)
start_time = time.process_time()
densest_subgraph = Find_Densest_Subgraph(number_of_nodes, number_of_edges, adj_matrix)
end_time = time.process_time()
(density, density_score) = Find_Density(densest_subgraph, adj_matrix) 
print('Densest Subgraph:', densest_subgraph)
print('Density: ', density)
print('Densest Subgraph Objective Score: ', density_score) 
print('Time taken: ', end_time- start_time)
graphPlot(adj_matrix, densest_subgraph, 'uk')