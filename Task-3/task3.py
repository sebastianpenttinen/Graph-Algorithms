from collections import defaultdict
import pandas as pd
from tkinter.filedialog import askopenfilename

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
    filename = askopenfilename()
    #filename = "benchmark3.csv"
    return filename


def readFile(filename):
    data = pd.read_csv(filename, sep="\t")
    return data


def makeGraph(graph, data):
    for _, row in data.iterrows():
        graph.addNode(row["Vertex1"])
        graph.addNode(row["Vertex2"])
        graph.addEdge(row["Vertex1"], row["Vertex2"], row["weight"], True)


def makeGraphFromNodes(graph, nodes):
    # Not very great but it works......
    t = Graph()
    for i in nodes:
        t.addNode(i)
        for key, value in graph.edges.items():
            for j in value:
                t.addEdge(key, j, graph.weights.get((key, j)), True)
    return t


def lookupId(data, edges):
    # take the edges and look them up in the original data
    ids = []
    for i in edges[0]:
        edgeID = data.loc[(data["Vertex1"] == i[0]) & (data["Vertex2"] == i[1])]
        tmp = edgeID["id"].tolist()
        if len(tmp) == 0:
            edgeID = data.loc[(data["Vertex1"] == i[1]) & (data["Vertex2"] == i[0])]
            tmp = edgeID["id"].tolist()
        ids.append(tmp[0])

    return ids


def writeTofile(tree, data):
    f = open("MinimumSpanningTree.txt", "w")
    for i in tree:
        tmp = lookupId(data, prim(i))
        for j in tmp:
            f.write(j + ",")
    f.close()


def prim(graph):
    minimumSpanningTree = set()
    visitedNodes = set()
    totalWeight = 0
    # select a vertex to begin with, in this case the first in the node list
    if len(graph.nodes) != 0:
        visitedNodes.add(graph.nodes[0])
    while len(visitedNodes) != len(graph.nodes):
        crossRoad = set()
        for i in visitedNodes:
            for j in graph.nodes:
                if j not in visitedNodes and graph.weights.get((i, j)) != 0:
                    crossRoad.add((i, j))

        # find the edge with the smallest weight in crossRoad
        CrossRoadweights = []
        edges = []
        for index in crossRoad:
            tmp = graph.weights.get(index)
            if tmp is not None:
                CrossRoadweights.append(tmp)
                edges.append(index)

        minimumSpanningTree.add(edges[CrossRoadweights.index(min(CrossRoadweights))])
        visitedNodes.add(edges[CrossRoadweights.index(min(CrossRoadweights))][1])
        totalWeight += min(CrossRoadweights)
    print("Total weight of the minimal spanning tree: " + str(totalWeight))
    return minimumSpanningTree, totalWeight


def connectedComponents(graph):
    result = []
    nodes = set(graph.nodes)
    while nodes:
        n = nodes.pop()
        group = {n}
        queue = [n]

        while queue:
            n = queue.pop(0)
            edges = set(graph.edges.get(n))
            edges.difference_update(group)
            nodes.difference_update(edges)
            group.update(edges)
            queue.extend(edges)
        result.append(group)
    return result


def main():
    filename = getFileName()
    data = readFile(filename)
    g = Graph()
    makeGraph(g, data)
    con = connectedComponents(g)

    graphs = []
    for i in con:
        graphs.append(makeGraphFromNodes(g, i))
    writeTofile(graphs, data)


if __name__ == "__main__":
    main()
