from grid.get_grid import get_grid


class Graph:
    def __init__(self, adjacency_list):
        self.adjacency_list = adjacency_list

    def get_neighbors(self, v):
        return self.adjacency_list[v]


def create_graph():
    """ Creates graph from game grid """

    adjacency_list = get_adjacency_list()
    return Graph(adjacency_list)


def get_adjacency_list():
    """ Returns list of node neighbours """

    adjacency_list = {}
    grid = get_grid()
    rows, columns = grid.shape

    for i in range(rows):
        for j in range(columns):
            if grid[i, j] == 0:     # if move not available just continue
                continue

            node_name = get_node_name(i, j)
            adjacency_list[node_name] = []

            # get all directions in which user can move and initialize its cost to 1

            if grid[i-1, j]:    # i is never 0 so i-1 is safe operation
                adjacency_list[node_name].append((get_node_name(i-1, j), 1))

            if j > 0:
                if grid[i, j-1]:
                    adjacency_list[node_name].append((get_node_name(i, j-1), 1))

            if grid[i+1, j]:    # i is never row-1 so i+1 is safe operation
                adjacency_list[node_name].append((get_node_name(i+1, j), 1))

            if j < columns-1:
                if grid[i, j+1]:
                    adjacency_list[node_name].append((get_node_name(i, j+1), 1))

    return adjacency_list


def get_node_name(i, j):
    return 'n' + str(i) + '_' + str(j)
