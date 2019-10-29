import pandas as pd
from collections import defaultdict
from tkinter.filedialog import askopenfilename
import csv

class Node:
    def __init__(self, label, source=False, sink=False):
        self.label = label
        self.source = source
        self.sink = sink

class Edge:
    def __init__(self, start, end, capacity, edgeId):
        self.start = start
        self.end = end
        self.capacity = capacity
        self.edgeId = edgeId
        self.flow = 0
        self.returnEdge = None

class Graph:
    def __init__(self):
        self.nodes = []
        self.edges = defaultdict(list)
        
    def getNode(self, name):
        for node in self.nodes:
            if name == node.label:
                return node

    def addEdge(self, start, end, capacity, edgeId):
        newEdge = Edge(start, end, capacity, edgeId)
        returnEdge = Edge(end, start, 0, "")
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
        source = self.getNode('source')
        sink = self.getNode('sink')
        
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
        graph.addEdge(row["Vertex1"], row["Vertex2"], row["capacity"], row["id"])


def writeToCSV(graph, maxFlow):
    with open("Flow.csv", mode="w") as csvFile:
        fieldnames = ["edge_id", "flow_value"]
        writer = csv.DictWriter(csvFile, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        for _, value in graph.edges.items():
            for i in value:
                if i.edgeId == "":
                    continue
                else:
                    writer.writerow({"edge_id": i.edgeId, "flow_value": i.flow})
        writer.writerow({"edge_id": "Max-flow value", "flow_value": maxFlow})

def main():
    filename = getFileName()
    data = readFile(filename)
    g = Graph()
    makeGraph(g, data)
    maxFlow = g.calculateMaxFlow()
    writeToCSV(g, maxFlow)
if __name__ == "__main__":
    main()