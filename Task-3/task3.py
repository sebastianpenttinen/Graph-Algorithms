from collections import defaultdict
import pandas as pd


class Graph:
    def __init__(self):
        self.nodes = []
        self.edges = defaultdict(list)
        self.weights = {}

    def addEdge(self, startNode, endNode, weight, undirected):
        self.edges[startNode].append(endNode)
        if undirected:
            self.edges[endNode].append(startNode)
        self.weights[(startNode, endNode)] = weight
        self.weights[(endNode, startNode)] = weight

    def addNode(self, node):
        if node not in self.nodes:
            self.nodes.append(node)


def getFileName():
    # filename = askopenfilename()
    filename = "benchmark3.csv"
    return filename


def readFile(filename):
    data = pd.read_csv(filename, sep="\t")
    return data


def makeGraph(graph, data, graphType):
    for _, row in data.iterrows():
        if graphType == "u":
            graph.addNode(row["Vertex1"])
            graph.addNode(row["Vertex2"])
            graph.addEdge(row["Vertex1"], row["Vertex2"], row["weight"], True)
        else:
            graph.addEdge(row["Vertex1"], row["Vertex2"], row["weight"], False)


def lookupId(data, edges):
    ids = []
    for i in edges[0]:
        edgeID = data.loc[(data["Vertex1"] == i[0]) & (data["Vertex2"] == i[1])]
        tmp = edgeID["id"].tolist()
        if len(tmp) != 0:
            ids.append(tmp[0])
    return ids


def writeTofile(tree):
    f = open("MinimumSpanningTree.txt", "w")
    for i in tree:
        f.write(i + ",")
    f.close()


def prim(graph):

    minimumSpanningTree = set()
    visitedNodes = set()
    totalWeight = 0
    # select a vertex to begin with
    if len(graph.nodes) != 0:
        visitedNodes.add(graph.nodes[0])
    while len(visitedNodes) != len(graph.nodes):
        crossRoad = set()
        for i in visitedNodes:
            for j in graph.nodes:
                if j not in visitedNodes and graph.weights.get((i, j)) != 0:
                    crossRoad.add((i, j))

        # find the edge with the smallest weight in crossRoad
        # This can be improved
        weight = 1000000000
        minEdge = ("", "")
        for index in crossRoad:
            tmp = graph.weights.get(index)
            if tmp is not None:
                if tmp < weight:
                    weight = tmp
                    minEdge = index

        minimumSpanningTree.add(minEdge)

        visitedNodes.add(minEdge[1])
        totalWeight += weight

    return minimumSpanningTree, totalWeight


def main():
    filename = getFileName()
    data = readFile(filename)
    g = Graph()

    makeGraph(g, data, "u")
    writeTofile(lookupId(data, prim(g)))


if __name__ == "__main__":
    main()
