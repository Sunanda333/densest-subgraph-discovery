import networkx as nx

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

def triangle_density(G): 
    """
    Returns the triangle density of the graph triangle density = |T(S)|/(|S|*(|S|-1)*(|S|-2))/6
    """
    t = nx.triangles(G)
    return (sum(t.values())/3.0)/((G.number_of_nodes()*(G.number_of_nodes()- 1)*(G.number_of_nodes()-2))/6.0)

def get_triangles(G): 
    """
    Lists all the triangles of the graph """
    triangles = {}
    edges = {}
    for edge in G.edges(): 
        if edge[0] < edge[1]:
            edges[(edge[0], edge[1])] = [] 
        else:
            edges[(edge[1], edge[0])] = [] 
    ind = 0
    done = set() 

    for n in G:
        done.add(n) 
        nbrdone = set()
        nbrs = set(G[n]) 
        for nbr in nbrs:
            if nbr in done:
                continue
            nbrdone.add(nbr)
            for both in nbrs.intersection(G[nbr]):
                if both in done or both in nbrdone:
                    continue
                triangles[ind] = sorted((n, nbr, both)) 

                if n > nbr:
                    edges[(nbr, n)].append(ind) 
                else:
                    edges[(n, nbr)].append(ind) 
                
                if n > both:
                    edges[(both, n)].append(ind) 
                else:
                    edges[(n, both)].append(ind) 
                    
                if both > nbr:
                    edges[(nbr, both)].append(ind) 
                else:
                    edges[(both, nbr)].append(ind) 
                ind += 1
    return triangles, edges    

def generate_triangle_neighbors(triangles, edges): 
    """
    For each triangle returns the triangles with which it shares a common edge
    """
    neighbors = {}
    for triangle in triangles.keys(): 
        neighbors[triangle] = {} 
        neighbors[triangle][(triangles[triangle][0],
    triangles[triangle][1])] = len(edges[(triangles[triangle][0], triangles[triangle][1])]) - 1 
    neighbors[triangle][(triangles[triangle][0], 
    triangles[triangle][2])] = len(edges[(triangles[triangle][0], triangles[triangle][2])]) - 1 
    neighbors[triangle][(triangles[triangle][1],
    triangles[triangle][2])] = len(edges[(triangles[triangle][1], triangles[triangle][2])]) - 1
    return neighbors

def greedy_triangle_graph_density(G): 
    """
    Returns the subgraph created by the subgraph of the triangle-graph with optimal triangle-graph density """
    triangles, edges = get_triangles(G)
    nbrs = generate_triangle_neighbors(triangles, edges)
    num_nodes = len(triangles) 
    total_nodes = len(triangles) 
    min_degs = {}
    for k1 in nbrs.keys():
        s = []
        for k2 in nbrs[k1].keys():
            s.append(nbrs[k1][k2]) 
        min_degs[k1] = min(s)

    sum_degs = sum(min_degs.values())
    nodes = sorted(min_degs, key=min_degs.get) 
    bin_boundaries = [0]
    curr_deg = 0

    for i, v in enumerate(nodes):
        if min_degs[v] > curr_deg:
            bin_boundaries.extend([i] * (min_degs[v] - curr_deg)) 
            curr_deg = min_degs[v]

    node_pos = dict((v, pos) for pos, v in enumerate(nodes)) 
    max_degree_density = sum_degs / float(num_nodes)
    ind = 0

    for v in nodes: 
        num_nodes -= 1 
        sum_degs -= min_degs[v]
        while min_degs[v] > 0:
            pos = node_pos[v]
            bin_start = bin_boundaries[min_degs[v]]
            node_pos[v] = bin_start
            node_pos[nodes[bin_start]] = pos
            nodes[bin_start], nodes[pos] = nodes[pos], nodes[bin_start] bin_boundaries[min_degs[v]] += 1
            min_degs[v] -= 1
        edges[(triangles[v][0], triangles[v][1])].remove(v) 
        for u in edges[(triangles[v][0], triangles[v][1])]:
            nbrs[u][(triangles[v][0], triangles[v][1])] -= 1
            if len(edges[(triangles[v][0], triangles[v][1])]) - 1 < min_degs[u]:
                pos = node_pos[u]
                bin_start = bin_boundaries[min_degs[u]] 
                node_pos[u] = bin_start 
                node_pos[nodes[bin_start]] = pos
                nodes[bin_start], nodes[pos] = nodes[pos], nodes[bin_start] 
                bin_boundaries[min_degs[u]] += 1
                min_degs[u] -= 1
                sum_degs -= 1

        edges[(triangles[v][0], triangles[v][2])].remove(v) 
        for u in edges[(triangles[v][0], triangles[v][2])]:
            nbrs[u][(triangles[v][0], triangles[v][2])] -= 1
            if len(edges[(triangles[v][0], triangles[v][2])]) - 1 < min_degs[u]:
                pos = node_pos[u]
                bin_start = bin_boundaries[min_degs[u]]
                node_pos[u] = bin_start
                node_pos[nodes[bin_start]] = pos
                nodes[bin_start], nodes[pos] = nodes[pos], nodes[bin_start] 
                bin_boundaries[min_degs[u]] += 1
                min_degs[u] -= 1
                sum_degs -= 1

        edges[(triangles[v][1], triangles[v][2])].remove(v) 
        for u in edges[(triangles[v][1], triangles[v][2])]:
            nbrs[u][(triangles[v][1], triangles[v][2])] -= 1
            if len(edges[(triangles[v][1], triangles[v][2])]) - 1 < min_degs[u]:
                pos = node_pos[u]
                bin_start = bin_boundaries[min_degs[u]]
                node_pos[u] = bin_start
                node_pos[nodes[bin_start]] = pos
                nodes[bin_start], nodes[pos] = nodes[pos], nodes[bin_start] 
                bin_boundaries[min_degs[u]] += 1
                min_degs[u] -= 1
                sum_degs -= 1

        if num_nodes > 0:
            current_degree_density = sum_degs / float(num_nodes) 
            if current_degree_density > max_degree_density:
                max_degree_density = current_degree_density 
                ind = total_nodes - num_nodes

    optimal_nodes = nodes[ind:]
    nodes = set()
    for triangle in optimal_nodes: 
        nodes.add(triangles[triangle][0]) 
        nodes.add(triangles[triangle][1]) 
        nodes.add(triangles[triangle][2])

    subg = G.subgraph(nodes) 
    return subg

def main(): 
    """ Main method """
    filename = sys.argv[1]
    if filename.split('.')[1] == 'gml':
        G = read_gml('networks/' + filename) 
    elif filename.split('.')[1] == 'mtx':
        G = mmread(filename) 
    else:
        G = nx.read_edgelist('networks/' + filename, delimiter='\t', nodetype=int)
    
    if filename.split('.')[1] == 'mtx': 
        G = nx.Graph(G)
    else:
        G = G.to_undirected()
        
    for node in G.nodes_with_selfloops(): 
        G.remove_edge(node, node)

    G1 = nx.Graph()
    for edge in G.edges():
        u = edge[0] 
        v = edge[1] 
        if u == v:
            continue

        if not G1.has_edge(u, v):
            G1.add_edge(u, v, weight=1.0)

    G = G1
    print ("Number of nodes:", G.number_of_nodes())
    print ("Number of edges:", G.number_of_edges())
    subg = greedy_triangle_graph_density(G)
    print ("----Greedy Triangle-Graph Density----")
    print ("Degree Density: " + str(degree_density(subg)))
    print ("Density: " + str(density(subg)))
    print ("Triangle Density: " + str(triangle_density(subg))) 
    print ("# Nodes: " + str(subg.number_of_nodes()))