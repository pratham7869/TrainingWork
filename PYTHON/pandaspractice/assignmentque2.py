import pandas as pd


 # question 2...
dfgod = pd.read_csv("gods.csv")
print(dfgod)
dfgoddess = pd.read_csv("goddess.csv")
print(dfgoddess)
print(dfgod.merge(dfgoddess, how='left', on='domain'))


