import networkx as nx
import numpy as np
from project_utils import *
from matplotlib import pyplot as plt


def closest_node(network, startNode, destinations):
    """ Reads in the starting node of the network and returns the closest node by distance

    Parameters
    ----------
    network : str
        Name of network
    
    startNode : str
        Name of starting node

    destinations : list
        List of possible destinations from start node

    Returns
    -------
    closestNode : str
        Name of closest node
    """

    # Initialise the first distance 
    shortest_dist = float('inf') 

    # Loop through the list of destinations
    for node in destinations:
        dist = nx.shortest_path_length(auckland, startNode, node, weight = 'weight') # Calculate the distance between node and destination node

        # Check if its the shortest distance
        if dist < shortest_dist:
            closestNode = node # Set the closest node
            shortest_dist = dist # Set the new shortest node
    
    # Return the closest node by distance
    return closestNode

     
def nearest_neighbour(network, startNode, destinations):
    """ Generates a path from the starting node to its respective destinations and returns a path containing
        the list of nodes it travels to and its corresponding path length.

    Parameters
    ----------
    network : str
        Name of network

    startNode : str
        Name of starting node

    destinations : list
        List of possible destinations from start node


    Returns
    -------
    path : list
        List containing the nodes travelled through

    pathDist: float
        Total distance of the path travelled
    """

    
    path = [] # Initialise the list of nodes
    pathDist = float(0) # Initialise the distance
    
    path.append(startNode) # Append the first node

    # Loop through all destinations until empty
    while len(destinations) != 0:
        closestNode = closest_node(network, startNode, destinations) # Find the closest node of current node
        destinations.remove(closestNode) # Remove the closest node from the possible destinations
        path.append(closestNode) # Append the closest node to the path
        pathDist = pathDist + nx.shortest_path_length(auckland, startNode, closestNode, weight = 'weight') # Add the distance 
        startNode = closestNode # Set the current node as the closest one 

    # Add the final destination to the path 
    path.append('Auckland Airport') # append the last node
    pathDist = pathDist + nx.shortest_path_length(auckland, closestNode, 'Auckland Airport', weight = 'weight') # Add the distance 

    # Return the path and its distance
    return path, pathDist



def longitude_homes(network, rest_homes, longitude):
    """ Generates two lists of homes with one consisting the names of rest homes left of longitude and one 
        to the right of the longitude 

    Parameters
    ----------
    network : str
        Name of network

    resthomes : list
        List of rest homes

    longitude : float
        Longitude to split homes by

    Returns
    -------
    west_homes : list
        List containing the nodes west of the longitude

    east_homes: list
        List containing the nodes east of the longitude
    """

    # Initialise the two seperate lists
    west_homes = []
    east_homes = []

    # Loop through all the rest homes
    for home in rest_homes:

        # Check if the longitude is greater than the given one
        if network.nodes[home]['lng'] > longitude: 
            east_homes.append(home) # append to the east list

        else: 
            west_homes.append(home) # append to the west list

    # return both lists
    return west_homes, east_homes



def latitude_homes(network, west_homes, east_homes, west_latitude, east_latitude):
    """ Generates four lists of homes with each consisting a quadrant of the homes in the NW,NE,SW,SE directions

    Parameters
    ----------
    network : str
        Name of network

    west_homes : list
        List of homes west of a longitude

    east_homes : list
        List of homes east of a longitude
    
    west_latitude : float
        latitude to split west homes by
    
    east_latitude : float
        latitude to split east homes by

    Returns
    -------
    NW_homes : list
        List containing the nodes in the north west quadrant

    NE_homes : list
        List containing the nodes in the north east quadrant

    SW_homes : list
        List containing the nodes in the south west quadrant

    SE_homes : list
        List containing the nodes in the south east quadrant
    """

    # Initialise the four paths
    NW_homes = []
    NE_homes = []
    SW_homes = []
    SE_homes = []

    # Loop through the west list
    for home in west_homes:

        # Check if latitude is greater than the given one
        if network.nodes[home]['lat'] > west_latitude:
            NW_homes.append(home) # Append to north west list

        else: 
            SW_homes.append(home) # Append to south west list
    
    # Loop through the east list
    for home in east_homes:

        # Check if the latitude is greater than the given one
        if network.nodes[home]['lat'] > east_latitude: 
            NE_homes.append(home) # Append to the north east list

        else: 
            SE_homes.append(home) # Append to the north west list


    # Return the four paths
    return NW_homes, NE_homes, SW_homes, SE_homes



def path_nodes(network, path):
    """ Generates a path with the interlinking nodes between it

    Parameters
    ----------
    network : str
        Name of network

    path : list
        List of homes in the path


    Returns
    -------
    path_nodes : list
        List containing all the nodes for the path

    """
    
    # Initialise a list of all the path nodes
    path_nodes = [] 

    # Search through each pair of nodes
    for rest_home_1, rest_home_2 in zip(path[:-1], path[1:]):
        path_with_nodes = nx.shortest_path(auckland, rest_home_1, rest_home_2, weight='weight') # Find the shortest path 
        path_nodes.extend(path_with_nodes[:-1]) # Extend the list

    # return the final path 
    return path_nodes




# Read in both the network of homes and the list of rest_homes
auckland = read_network('network.graphml')
rest_homes = get_rest_homes('rest_homes.txt')

# Set up a list of the rest_homes latitudes and longitudes
longitude = []
west_latitude = []
east_latitude = []

# loop through each rest home
for home in rest_homes:
    lng = auckland.nodes[home]['lng'] # Find the longitude
    longitude.append(lng) # append to the list

mid_lng = np.median(longitude) # Find the midpoint longitude

# Extract the west and east sections 
west_homes, east_homes = longitude_homes(auckland, rest_homes, mid_lng)

# Loop through each west home
for home in west_homes:
    lat = auckland.nodes[home]['lat'] # Find the latitude
    west_latitude.append(lat) # Append to the list

west_mid_lat = np.mean(west_latitude) # Find the midpoint latitude

# Loop through each east home
for home in east_homes:
    lat = auckland.nodes[home]['lat'] # Find the latitude
    east_latitude.append(lat) # Append to the list

east_mid_lat = np.mean(east_latitude) # Find the midpoint latitude

# Find the 4 quadrants
NW_homes, NE_homes, SW_homes, SE_homes = latitude_homes(auckland, west_homes, east_homes, west_mid_lat, east_mid_lat)



# Find the North West Path
NW_path, NW_pathDist = nearest_neighbour(auckland,'Auckland Airport', NW_homes) # Use algorithm
NW_path_nodes = path_nodes(auckland, NW_path) # Find the total path
print("Path 1 Distance is: {:6.3f}".format(NW_pathDist)) # Print the distnace
plot_path(auckland, NW_path_nodes, save='path_1.png') # Save it to a figure

# Write the North West path to a file
with open("path_1.txt", 'w') as output:
    for row in NW_path:
        output.write(str(row) + '\n')


# Find the North East Path
NE_path, NE_pathDist = nearest_neighbour(auckland,'Auckland Airport', NE_homes) # Use algorithm
NE_path_nodes = path_nodes(auckland, NE_path) # Find the total path
print("Path 2 Distance is: {:6.3f}".format(NE_pathDist)) # Print the distnace
plot_path(auckland, NE_path_nodes, save='path_2.png') # Save it to a figure

# Write the North East path to a file
with open("path_2.txt", 'w') as output:
    for row in NE_path:
        output.write(str(row) + '\n')


# Find the South West Path
SW_path, SW_pathDist = nearest_neighbour(auckland,'Auckland Airport', SW_homes) # Use algorithm
SW_path_nodes = path_nodes(auckland, SW_path) # Find the total path
print("Path 3 Distance is: {:6.3f}".format(SW_pathDist)) # Print the distnace
plot_path(auckland, SW_path_nodes, save='path_3.png') # Save it to a figure

# Write the South West path to a file
with open("path_3.txt", 'w') as output:
    for row in SW_path:
        output.write(str(row) + '\n')


# Find the South East Path
SE_path, SE_pathDist = nearest_neighbour(auckland,'Auckland Airport', SE_homes) # Use algorithm
SE_path_nodes = path_nodes(auckland, SE_path) # Find the total path
print("Path 4 Distance is: {:6.3f}".format(SE_pathDist)) # Print the distnace
plot_path(auckland, SE_path_nodes, save='path_4.png') # Save it to a figure

# Write the South Eest path to a file
with open("path_4.txt", 'w') as output:
    for row in SE_path:
        output.write(str(row) + '\n')