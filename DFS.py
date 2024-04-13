from collections import defaultdict

class Graph:
    def __init__(self):
        self.graph = defaultdict(list)

    def addEdge(self, u, v):
        self.graph[u].append(v)

    def DFSUtil(self, v, visited, path):
        visited.add(v)
        path.append(v)
        for neighbour in self.graph[v]:
            if neighbour not in visited:
                self.DFSUtil(neighbour, visited, path)

    def DFS(self, v, visited, path):
        visited = set()
        self.DFSUtil(v, visited, path)

class DFS:
    def __init__(self):
        pass


