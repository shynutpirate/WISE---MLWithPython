from pandas import DataFrame
import pandas as pd
df1 = pd.read_csv("/Users/shravanivadlamudi/Downloads/youtube-new/CAvideos.csv",usecols = ['title','views'])
test = df1.sort_values(['views'], ascending = ['False'])
print (test[:10])

