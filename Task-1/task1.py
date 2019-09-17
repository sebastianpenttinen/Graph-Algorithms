import numpy as np
import pandas as pd
from tkinter.filedialog import askopenfilename

def Matrix(edges):
    keyNodes = sorted(edges.keys()) # Sort the nodes rows?
    valueNodes = dict(zip(keyNodes, range(len(keyNodes)))) #columns? # make them the same shape
    matrix = np.zeros(shape=(len(edges),len(edges)))
    for i in range(len(keyNodes)):
        for j in range(i, len(edges)):
            if edges[keyNodes[i]] in valueNodes: # Check if there is an edge
                j = valueNodes[edges[keyNodes[i]]]
                matrix[i,j] = 1
    return matrix

def getInput():
    wrongInput = True
    while(wrongInput):
        userInput = input(
            'If the graph is directed enter "d" if undirected enter "u"\n')
        if (userInput == 'd' or userInput == 'u'):
            wrongInput = False

    return userInput


def readFile():
    #filename = askopenfilename()
    filename = 'edges_1_27307.csv'
    data = pd.read_csv(filename,sep='\t', header=None, skiprows=1) # read the tab separated file and remove the header
    edges = data.iloc[:,0:2]
    return edges


def main():
    #userInput = getInput()
    edges = readFile()
    edgeDict = dict(zip(edges[0], edges[1]))
    matrix = Matrix(edgeDict)
    np.savetxt("adjacencyMatrix.txt", np.around(matrix, decimals=0),fmt='%.0f',delimiter='\t')

if __name__ == "__main__":
    main()