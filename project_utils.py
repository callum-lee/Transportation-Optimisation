import networkx as nx
from matplotlib import pyplot as plt

def read_network(filename):
    """ Reads in a file to a netowrkx.Graph object

    Parameters
    ----------
    filename : str
        Path to the file to read. File should be in graphml format

    Returns
    -------
    network : networkx.Graph
        representation of the file as a graph/network

    """
    network = nx.read_graphml(filename)
    # relabel all integer nodes if possible
    def relabeller(x):
        try:
            return int(x)
        except ValueError:
            return x
    nx.relabel_nodes(network, relabeller, copy=False)
    return network

def get_rest_homes(filename):
    """ Reads in the list of rest home names

    Parameters
    ----------
    filename : str
        Path to the file to read

    Returns
    -------
    rest_homes : list of strings
        list of all rest homes
    """

    rest_homes = []
    with open(filename, 'r') as fp:
        for line in fp:
            rest_homes.append(line.strip())
    return rest_homes

def plot_path(network, path, save=None):
    """ Plots a given path of the Auckland network

    Parameters
    ----------
    network : networkx.Graph
        The graph that contains the node and edge information
    path : list
        A list of node names
    save: str or None
        If a string is provided, then saves the figure to the path given by the string
        If None, then displays the figure to the screen
    """
    lats = [network.nodes[p]['lat'] for p in path]
    lngs = [network.nodes[p]['lng'] for p in path]
    plt.figure(figsize=(8,6))
    ext = [174.48866, 175.001869, -37.09336, -36.69258]
    plt.imshow(plt.imread("akl_zoom.png"), extent=ext)
    plt.plot(lngs, lats, 'r.-')
    if save:
        plt.savefig(save, dpi=300)
    else:
        plt.show()
