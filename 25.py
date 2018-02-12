import matplotlib.pyplot as plt
import pandas as pd

def readColumn(x):
    df = pd.read_csv('C:/Users/ShravaniVadlamudi/Downloads/testset.csv', usecols = [x])
    return df[:5]
def displayGraph(X,Y,color):
    X = readColumn(X)
    Y = readColumn(Y)
    plt.plot(X,Y,color)
    plt.show()
displayGraph(' _hum', ' _tempm', 'green')