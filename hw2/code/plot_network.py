import networkx as nx
from numpy.random import seed
from numpy import arange, array
from matplotlib import pyplot as plt

def plot_network(A, voltages):
    ''' 
    Plot graph associated with adjacency matrix A
    
    input
    -----
    A              : numpy array, adjacency matrix
                     each row of A should have only two nonzero entries
                     A[i,j] = -1 is the edge start 
                     A[i,j] = 1 is the edge end 
                     Interface for f:  f(x) returns f(x), Jacobian of f(x)
    voltages       : numpy array, size of A.shape[1], the number of columns 
                     voltages[k] holds the voltage at node k

    output
    ------
    plots network to screen

    '''
    seed(1)

    if (voltages.shape[0] != A.shape[1]) or (len(voltages.shape) != 1):
        raise ValueError("length of voltages must be equal to number of nodes in A")

    fig, ax = plt.subplots()
    
    # Draw graph based on A
    G = nx.DiGraph()

    # Add nodes, be careful to add nodes in numerical order, so that the 
    # ordering of adding nodes matches the index ordering in voltages
    G.add_nodes_from([str(k) for k in arange(A.shape[1])])
    labels = {}
    for i in range(A.shape[1]):
        labels[str(i)] = str(i) #+ "\nv=%1.3f"%voltages[i]

    # Draw edges
    edge_labels = {}
    for i in range(A.shape[0]):
        node1 = (A[i,:] == -1).nonzero()[0]
        node2 = (A[i,:] == 1).nonzero()[0]
        if (node1.shape[0] != 1) or (node2.shape[0] != 1) :
            raise ValueError("adjacency matrix not correct")
        
        key = (str(node1[0]), str(node2[0]))
        #edge_labels[key] = str(i)
        edge_labels[key] = "$%1.2f$"%(voltages[node2] - voltages[node1])
        G.add_edges_from([key])
    
    # choose node positions
    if A.shape == (8,6):
        # Positions for A1 graph
        pos = {'0': array([ 0.820, -0.636]), 
               '1': array([ 0.265,  0.405]), 
               '2': array([-0.242,  1.3   ]), 
               '3': array([-0.750, -0.622]), 
               '4': array([ 0.051, -0.122]), 
               '5': array([-0.750,  0.405])}
    elif A.shape == (10,7):
        # Positions for A2 graph
        pos = {'0': array([ 0.820, -0.636]), 
               '1': array([ 0.265,  0.405]), 
               '2': array([-0.242,  1.3   ]), 
               '3': array([-0.750, -0.622]), 
               '4': array([ 0.051, -0.122]), 
               '5': array([-0.750,  0.405]),
               '6': array([ 1.250,   0.405])}
    else:
        pos = nx.fruchterman_reingold_layout(G)
    

    cmap = plt.cm.coolwarm
    nx.draw(G, pos, node_size=620, width=2, arrowstyle = '-|>', arrowsize = 12, ax=ax,
            node_color=voltages, cmap=cmap)
    nx.draw_networkx_labels(G, pos, font_weight='bold', ax=ax, labels=labels)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=12, label_pos=0.5, 
                                 font_color='r', ax=ax)
    
    vminmax = max(abs(voltages))
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=-vminmax, vmax=vminmax))
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=ax)
    
    plt.title("Electrical Network\nNode Color Indicates Voltage: Red is positive, Blue is negative")
    plt.axis('equal')
    plt.savefig('network_solution.png', dpi=500, format='png', bbox_inches='tight', pad_inches=0.0,)
    #plt.show()   


