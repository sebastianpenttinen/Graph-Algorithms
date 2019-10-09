import pandas as pd
from collections import defaultdict
from tkinter.filedialog import askopenfilename

class Graph:
    def __init__(self):
        self.nodes = []
        self.edges = defaultdict(list)
        self.weights = {}

    def addEdge(self, startNode, endNode, undirected):
        self.edges[startNode].append(endNode)
        if undirected:
            self.edges[endNode].append(startNode)

    def addNode(self, node):
        if node not in self.nodes:
            self.nodes.append(node)

def getFileName():
    #filename = askopenfilename()
    filename = "benchmark4.csv"
    return filename

def readFile(filename):
    data = pd.read_csv(filename, sep="\t")
    return data


def makeGraph(graph, data):
    for _, row in data.iterrows():
        graph.addNode(row["Vertex1"])
        graph.addNode(row["Vertex2"])
        graph.addEdge(row["Vertex1"], row["Vertex2"], True)
        

def nodeColoring(graph):
    sortedNodes = sorted(graph.edges.items(), key=lambda i: len(i[1]), reverse=True)
    
    nodeColors = {}

    for node in sortedNodes:
        freeColors = [True] * len(sortedNodes)
        for adjacentNode in graph.edges.get(node[0]):
            if adjacentNode in nodeColors:
                color = nodeColors[adjacentNode]
                freeColors[color] = False
        for color, available in enumerate(freeColors):
            if available:
                nodeColors[node[0]] = color
                break

    return nodeColors


def main():
    filename = getFileName()
    data = readFile(filename)
    g = Graph()
    makeGraph(g, data)
    color = nodeColoring(g)
    print (color)

if __name__ == "__main__":
    main()