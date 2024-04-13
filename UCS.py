import heapq

class Graph:
    def __init__(self):
        self.graph = {}

    def addNode(self, start, end, cost):
        if start not in self.graph:
            self.graph[start] = []
        self.graph[start].append((end, cost))

def ucs(graph, start, goal):
    priorityq = [(0, start)]  # (cost, node)
    visited = set()
    costs = {start: 0}  # Dictionary to store the cost to reach each node
    while priorityq:
        cost, node = heapq.heappop(priorityq)
        if node in visited:
            continue
        visited.add(node)
        if node == goal:
            return costs  # Return the costs dictionary
        if node in graph.graph:
            for neighbor, edge_cost in graph.graph[node]:
                if neighbor not in visited:
                    new_cost = cost + edge_cost
                    if neighbor not in costs or new_cost < costs[neighbor]:
                        costs[neighbor] = new_cost
                        heapq.heappush(priorityq, (new_cost, neighbor))
    return None

class UCS:
    def __init__(self):
        pass