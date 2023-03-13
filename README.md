
# densest-subgraph-discovery
We explore different algorithms to find the densest sub-graph on various data-sets and compare the results.

## Set-up:
### Ubuntu/MacOS
#### Creating the environment

    python3 -m venv densest-subgraph
    source densest-subgraph/bin/activate

#### Installations

    python3 -m pip install networkx==1.9.1 matplotlib==2.2.3
    python3 -m pip install PyMaxflow scipy

#### Shut-down environment

    deactivate

### Windows:
#### Creating the environment

    python3 -m venv densest-subgraph
    source densest-subgraph\Scripts\activate

#### Installations

    python3 -m pip install networkx==1.9.1 matplotlib==2.2.3
    python3 -m pip install PyMaxflow scipy

#### Shut-down

    deactivate

## Steps to run the code:

### Alpha Quasi Clique algorithm
    
    Copy the code to IDE/Jupyter Notebook
    Add any undirected graph to the directory
    Change the graph path in code to the custom added graph path 
    Run the code to see the result

### Goldberg algorithm

    Create two folders content/ , content/outputs/
    Upload the matrix market graph in the directory content/ and load it in adj_matrix 
    Run the code to see the result

### Greedy Plus algorithm

    Load the above program on an IDE
    Call the function greedyPlus with the desired parameter T
    Run the code to see the result

### K Clique algorithm
    Call the main function and add the first name of the graph as first argument
    Run the code to see the result



## Results/Models:
Results and Plots given in the paper