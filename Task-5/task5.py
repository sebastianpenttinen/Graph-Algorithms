from collections import defaultdict
import pandas as pd

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
    filename = "benchmark5.csv"
    return filename


def readFile(filename):
    data = pd.read_csv(filename, sep="\t")
    return data


def makeGraph(graph, data):
    for _, row in data.iterrows():
        graph.addNode(row["Vertex1"])
        graph.addNode(row["Vertex2"])
        graph.addEdge(row["Vertex1"], row["Vertex2"], True)

def augmentingPath(graph):
    return augmentingPath

def maximumCardinality(graph):
    agPath = augmentingPath(graph)
    

def main():
    filename = getFileName()
    data = readFile(filename)
    g = Graph()
    makeGraph(g, data)
if __name__ == "__main__":
    main()