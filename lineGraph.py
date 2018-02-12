import matplotlib.pyplot as plt
import pandas as pd

def readFile(x):
    df = pd.read_csv('/Users/shravanivadlamudi/Downloads/testset.csv', usecols = [x])
    return df[:5]
x = readFile('datetime_utc')
y = readFile(' _tempm')
plt.plot(x,y)
plt.show()
