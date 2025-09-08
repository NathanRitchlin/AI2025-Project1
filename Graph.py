from collections import defaultdict


class Graph:
    def __init__(self):
        self.graph = defaultdict(list)

    def addEdge(self,u,v):
        self.graph[u].append(v)
        # A function used by DFS

    def removeNode(self, v):
        self.graph.pop(v)



    def DFSUtil(self, v, visited, puzzle):

        # Mark the current node as visited
        # and print it
        visited.add(v)
        if(v!= 'start'):
            print("set value", v[0].value, "domain value", v[1], "position value", v[0].position, end=' ')
            v[0].value = v[1]


        # Recur for all the vertices
        # adjacent to this vertex

        for neighbour in self.graph[v]:
            if (neighbour not in visited):
                self.DFSUtil(neighbour, visited, puzzle)

        # The function to do DFS traversal. It uses
        # recursive DFSUtil()

    def DFS(self, v, puzzle):

        # Create a set to store visited vertices
        visited = set()

        # Call the recursive helper function
        # to print DFS traversal
        self.DFSUtil(v, visited, puzzle)


if __name__ == "__main__":
    g = Graph()
    g.addEdge(0, 1)
    g.addEdge(0,2)
    g.addEdge(2,3)
    g.addEdge(2,7)
    g.addEdge(3,5)

    print("Following is Depth First Traversal (starting from vertex 2)")

    # Function call
    g.DFS(0)

    g = Graph()
    for d1 in puzzle[0][0].domain:
        g.addEdge("start", (puzzle[0][0], d1))
    # constructing graph of all possible numbers for the sudoku puzzle
    for i in range(81):
        row = i // 9
        col = i % 9
        tile = puzzle[row][col]
        if (i != 80):
            row = (i + 1) // 9
            col = (i + 1) % 9
            nextTile = puzzle[row][col]
            for d1 in tile.domain:
                for d2 in nextTile.domain:
                    g.addEdge((tile, d1), (nextTile, d2))
                    # storing starting vert
        else:
            print('done')

    g.DFS("start", puzzle)