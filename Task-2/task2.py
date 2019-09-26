from tkinter.filedialog import askopenfilename
import pandas as pd

from collections import defaultdict


class Graph:
    # Simple intuitive way of representing a graph
    def __init__(self):
        self.edges = defaultdict(list)
        self.weights = {}

    def addEdge(self, startNode, endNode, weight, undirected):
        self.edges[startNode].append(endNode)
        if undirected:
            self.edges[endNode].append(startNode)  # undirected
        self.weights[(startNode, endNode)] = weight
        self.weights[(endNode, startNode)] = weight


def getInput():
    wrongInput = True
    while wrongInput:
        userInput = input("Do you want to continue with a new set of nodes? y/n\n")
        if userInput.lower() == "y" or userInput.lower() == "n":
            wrongInput = False

    return userInput.lower()


def getFileName():
    filename = askopenfilename()
    #filename = "edges_1_27307.csv"
    return filename


def readFile(filename):
    data = pd.read_csv(filename, sep="\t")
    return data


def makeNodeList(data):
    nodes = dict(zip(data["Vertex1"], data["Vertex2"]))
    nodesSorted = sorted(nodes.keys())
    return nodesSorted


def printOutput(g, nodeOne, nodeTwo, minOrMax):
    result = dijsktra(g, nodeOne, nodeTwo, minOrMax)

    if isinstance(result, str):
        print(result)

    else:
        print(result[0])
        print(result[1])


def getGraphType():
    wrongInput = True
    while wrongInput:
        userInput = input(
            'If the graph is directed enter "d" if undirected enter "u"\n'
        )
        if userInput.lower() == "d" or userInput.lower() == "u":
            wrongInput = False

    return userInput.lower()


def dijsktra(graph, startNode, endNode, isMinimum):
    shortestPaths = {startNode: (None, 0)}
    currentNode = startNode
    visitedNodes = set()  # to avoid loops

    while currentNode != endNode:
        visitedNodes.add(currentNode)
        destinations = graph.edges[currentNode]
        weightToCurrentNode = shortestPaths[currentNode][1]

        for nextNode in destinations:
            weight = graph.weights[(currentNode, nextNode)] + weightToCurrentNode

            if weight < 0 and isMinimum:
                return (
                    "There is a negtive weight in the graph"
                )  # Will not loop but can't garantee the minmum withted path

            if nextNode not in shortestPaths:
                shortestPaths[nextNode] = (currentNode, weight)
            else:
                currentShortestWeight = shortestPaths[nextNode][1]
                if currentShortestWeight > weight:
                    shortestPaths[nextNode] = (currentNode, weight)

        nextDestinations = {
            node: shortestPaths[node]
            for node in shortestPaths
            if node not in visitedNodes
        }
        if not nextDestinations:
            return "There is no path between the selected nodes"
        if isMinimum:
            currentNode = min(nextDestinations, key=lambda k: nextDestinations[k][1])
        else:
            currentNode = max(nextDestinations, key=lambda k: nextDestinations[k][1])

    path = []
    weight = []
    while currentNode is not None:
        path.append(currentNode)
        weight.append(shortestPaths[currentNode][1])
        nextNode = shortestPaths[currentNode][0]
        currentNode = nextNode

    path = path[::-1]
    weight = weight[::-1]
    return path, weight


def main():
    graphType = getGraphType()
    filename = getFileName()
    data = readFile(filename)
    g = Graph()

    for _, row in data.iterrows():
        if graphType == "u":
            g.addEdge(row["Vertex1"], row["Vertex2"], row["weight"], True)
        else:
            g.addEdge(row["Vertex1"], row["Vertex2"], row["weight"], False)

    print("Lookup minimum and maximum weighted paths\n")
    print("Choose from the following nodes\n")

    print(makeNodeList(data))
    print()

    nodeOne = input("Enter the first node\n")
    nodeTwo = input("Enter the second node\n")

    print("Minimum weighted path\n")

    printOutput(g, nodeOne, nodeTwo, True)

    print("Maximum weighted path\n")
    printOutput(g, nodeOne, nodeTwo, False)

    answer = getInput()
    if answer == "y":
        main()


if __name__ == "__main__":
    main()
