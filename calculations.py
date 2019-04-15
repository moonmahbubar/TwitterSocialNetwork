#Mahbubar Moon 
#Assignment 2
#Calculations
import networkx as nx 
import matplotlib.pyplot as plt

#Main.
if __name__== "__main__":
    #Open adjacency list created by homework2.py
    fh=open("out.adjlist", 'rb')

    #Import graph.
    graph=nx.read_adjlist(fh)

    #Calculate diameter.
    diameter = nx.algorithms.distance_measures.diameter(graph)

    #Calculate average distance.
    average_distance = nx.algorithms.shortest_paths.generic.average_shortest_path_length(graph)

    #Number of nodes.
    num_nodes = graph.number_of_nodes()

    #Number of edges.
    num_edges = graph.number_of_edges()

    #Save number of nodes and edges, diameter and average distance to calculations.txt
    f= open("calculations.txt","w+")
    f.write("Number of nodes: " + str(num_nodes) + "\n")
    f.write("Number of edges: " + str(num_edges) + "\n")
    f.write("Diameter: " + str(diameter) + "\n")
    f.write("Average distance: " + str(average_distance) + "\n")
    f.close()

    #Draw graph.
    nx.draw(graph)
    plt.show()