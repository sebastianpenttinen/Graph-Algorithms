import pandas as pd
from tkinter.filedialog import askopenfilename
import csv

class Node:
    def __init__(self, label, source=False, sink=False):
        self.label = label
        self.source = source
        self.sink = sink

class Edge:
    def __init__(self, start, end, capacity):
        self.start = start
        self.end = end
        self.capacity = capacity
        self.flow = 0
        self.returnEdge = None

class Graph:
    def __init__(self):
        self.nodes = []
        self.edges = {}
        
    def getNode(self, name):
        for node in self.nodes:
            if name == node.label:
                return node


    def findSource(self):
        for node in self.nodes:
            if node.source == True:
                return node

    def findSink(self):
        for node in self.nodes:
            if node.sink == True:
                return node


    def addEdge(self, start, end, capacity):
        newEdge = Edge(start, end, capacity)
        returnEdge = Edge(end, start, 0)
        newEdge.returnEdge = returnEdge
        returnEdge.returnEdge = newEdge
        vertex = self.getNode(start)
        self.edges[vertex.label].append(newEdge)
        returnNode = self.getNode(end)
        self.edges[returnNode.label].append(returnEdge)

    def addNode(self, node, source=False, sink=False):
        if node not in self.nodes:
            node = Node(node, source, sink)
            self.nodes.append(node)
            self.edges[node.label] = []

    def findPath(self, start, end, path):
        if start == end:
            return path
        for edge in self.edges[start]:
            residualCapacity = edge.capacity - edge.flow
            if residualCapacity > 0 and not (edge, residualCapacity) in path:
                result = self.findPath(edge.end, end, path + [(edge, residualCapacity)])
                if result != None:
                    return result

    def calculateMaxFlow(self):
        source = self.findSource()
        sink = self.findSink()
        
        path = self.findPath(source.label, sink.label, [])
        while path != None:
            flow = min(edge[1] for edge in path)
            for edge, _ in path:
                edge.flow += flow
                edge.returnEdge.flow -= flow
            path = self.findPath(source.label, sink.label, [])
        return sum(edge.flow for edge in self.edges[source.label])

def getFileName():
    #filename = askopenfilename()
    filename = "benchmark6.csv"
    return filename


def readFile(filename):
    data = pd.read_csv(filename, sep="\t")
    return data


def makeGraph(graph, data):
    for _, row in data.iterrows():

        if row["Vertex1"] == 'source':
            graph.addNode(row["Vertex1"], True, False)

        elif row["Vertex2"] == 'sink':
            graph.addNode(row["Vertex2"], False, True)

        else:
            graph.addNode(row["Vertex1"])
            graph.addNode(row["Vertex2"])

    for _, row in data.iterrows():
        graph.addEdge(row["Vertex1"], row["Vertex2"], row["capacity"])


def writeToCSV(coloredGraph):
    with open("Flow.csv", mode="w") as csvFile:
        fieldnames = ["edge_id", "flow_value"]
        writer = csv.DictWriter(csvFile, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        for key, value in coloredGraph.items():
            writer.writerow({"edge_id": key, "flow_value": value})

def main():
    filename = getFileName()
    data = readFile(filename)
    g = Graph()
    makeGraph(g, data)
    print(g.calculateMaxFlow())

if __name__ == "__main__":
    main()