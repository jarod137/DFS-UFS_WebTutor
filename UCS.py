# Jared Kaiser & Bryce Bales AI Project
# DFS & UCS WebTutor
# This file runs UCS on a specific graph
# Sources: https://www.geeksforgeeks.org/heap-queue-or-heapq-in-python/ , https://www.geeksforgeeks.org/uniform-cost-search-dijkstra-for-large-graphs/?ref=header_search,
# More Sources: https://www.tutorialspoint.com/python_data_structure/python_graphs.htm , https://www.geeksforgeeks.org/priority-queue-in-python/, 

import heapq

class Graph: #making the tree to put the nodes on using python graph class
    def __init__(thisone):
        thisone.graph = {}
        
    def addNode(thisone, start, end, cost):
        if start not in thisone.graph:
            thisone.graph[start] = []
        thisone.graph[start].append((end,cost))
        
def ucs(graph, start, goal):
    #need to use priority queue for UCS
    priorityq = [(0, start)] #(cost,node)
    visited = set()
    
    while priorityq:
        cost, node = heapq.heappop(priorityq)
        
        if node in visited:
            continue
        
        print(f"to go to node {node} it will cost {cost}")
        visited.add(node)
        
        if node == goal:
            print("goal state found")
            return
        
        if node in graph.graph:
            for neighbor, edge_cost in graph.graph[node]:
                if neighbor not in visited:
                    heapq.heappush(priorityq, (cost + edge_cost, neighbor))
                    
tree = Graph() #initializing and adding the nodes to the tree
tree.addNode(1,2,1)
tree.addNode(1,9,5)
tree.addNode(1,10,3)
tree.addNode(2,3,2)
tree.addNode(2,4,4)
tree.addNode(4,5,1)
tree.addNode(4,6,2)
tree.addNode(4,7,3)
tree.addNode(5,8,2)

ucs(tree, 1, 8) #runs ucs on our tree from nodes 1 to 8. wants to find 8