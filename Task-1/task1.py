import numpy as np
import pandas as pd
from tkinter.filedialog import askopenfilename

def Matrix(edges):
    # varaibles named according to what the value in the dictionaries are
    nodes = sorted(edges.keys()) # Sort the nodes according to index then node as value
    index = dict(zip(nodes, range(len(nodes)))) # here the node is the value and the index is the key 
    matrix = np.zeros(shape=(len(edges),len(edges))) # make the n x n matrix
    for i in range(len(nodes)): # go row by row
        for j in range(i, len(edges)): # column by column
             # Check if there is an edge by looking it up in the dictionaries
             # First it checks the node value to find the node in the edges and then looks up that nodes index
             # Example: looks up node at index 0 values is: 'n0'. Then uses 'n0' as the key to find if 'n0' has an edge to an node.
             # If there is an edge it looks up the index of that edge from the index dict by using the found node as the key.
             # In this case 'n0' has an edge to 'n33' and 'n33' has an index of 16. As a result a 1 is placed on row 0 column 16.
            if edges[nodes[i]] in index:
                j = index[edges[nodes[i]]] # put one in column if there is an edge
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