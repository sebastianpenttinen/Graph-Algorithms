import pandas as pd
from collections import defaultdict
from tkinter.filedialog import askopenfilename
import csv


class Edge:
    def __init__(self, start, end, capacity, edgeId):
        self.start = start
        self.end = end
        self.capacity = capacity
        self.edgeId = edgeId
        self.flow = 0
        self.backEdge = None


class Graph:
    def __init__(self):
        self.nodes = []
        self.edges = defaultdict(list)

    def addEdge(self, start, end, capacity, edgeId):
        edgeToAdd = Edge(start, end, capacity, edgeId)
        backEdge = Edge(end, start, 0, "")
        edgeToAdd.backEdge = backEdge
        backEdge.backEdge = edgeToAdd
        node = self.getNode(start)
        self.edges[node].append(edgeToAdd)
        backNode = self.getNode(end)
        self.edges[backNode].append(backEdge)

    def addNode(self, node):
        if node not in self.nodes:
            self.nodes.append(node)
            self.edges[node] = []

    def getNode(self, name):
        for node in self.nodes:
            if name == node:
                return node


def findPath(graph, start, end, path):
    if start == end:
        return path
<<<<<<< HEAD

    for edge in graph.edges[start]:
        flowLeft = edge.capacity - edge.flow
        if flowLeft > 0 and not (edge, flowLeft) in path:
            result = findPath(graph, edge.end, end, path + [(edge, flowLeft)])
=======
    for edge in graph.edges[start]:
        residualCapacity = edge.capacity - edge.flow
        if residualCapacity > 0 and not (edge, residualCapacity) in path:
            result = findPath(graph, edge.end, end, path + [(edge, residualCapacity)])
>>>>>>> 2cf7836dfef6bbc47ebe725d2c536f97e4a64a9a
            if result != None:
                return result


<<<<<<< HEAD
def maxFlow(graph):
=======
def calculateMaxFlow(graph):
>>>>>>> 2cf7836dfef6bbc47ebe725d2c536f97e4a64a9a
    source = graph.getNode("source")
    sink = graph.getNode("sink")

    path = findPath(graph, source, sink, [])

    while path != None:
        flow = min(edge[1] for edge in path)
        for edge, _ in path:
            edge.flow += flow
            edge.backEdge.flow -= flow
        path = findPath(graph, source, sink, [])
    return sum(edge.flow for edge in graph.edges[source])


def getFileName():
    # filename = askopenfilename()
    filename = "benchmark6.csv"
    return filename


def readFile(filename):
    data = pd.read_csv(filename, sep="\t")
    return data


def makeGraph(graph, data):

    for _, row in data.iterrows():
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
    mf = maxFlow(g)
    writeToCSV(g, mf)


if __name__ == "__main__":
    main()
