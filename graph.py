from grid.get_grid import get_grid
import numpy as np


def create_graph():
    adjacency_list = get_adjacency_list()
    return Graph(adjacency_list)


# list of node neighbours
def get_adjacency_list():
    adjacency_list = {}
    grid = np.array(get_grid())
    rows, columns = grid.shape

    for i in range(rows):
        for j in range(rows):
            if not grid[i, j]:
                continue

            node_name = get_node_name(i, j)
            adjacency_list[node_name] = []

            # get all directions in which user can move and initialize its cost to 1
            if grid[i-1, j]:
                adjacency_list[node_name].append((get_node_name(i-1, j), 1))
            if grid[i, j-1]:
                adjacency_list[node_name].append((get_node_name(i, j-1), 1))
            if grid[i+1, j]:
                adjacency_list[node_name].append((get_node_name(i+1, j), 1))
            if grid[i, j+1]:
                adjacency_list[node_name].append((get_node_name(i, j+1), 1))

    return adjacency_list


def get_node_name(i, j):
    return 'n' + str(i) + '_' + str(j)


class Graph:
    def __init__(self, adjacency_list):
        self.adjacency_list = adjacency_list

    def __str__(self):
        return str(self.adjacency_list)

    def get_neighbors(self, v):
        return self.adjacency_list[v]
