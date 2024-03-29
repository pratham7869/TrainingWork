import numpy as np
import pandas as pd

dict1 = {
    "name": ['pratham','anupam','aditya'],
    "marks": [100,60,50],
    "attendence": [100,99,50],
    "city": ['indore','ujjain','sonkach']
}

df=pd.DataFrame(dict1)

print(df)
print("")
df.to_csv('marks.csv',index=False)    # here index = false for not getting indexes in csv file

print(df.head(2))
print("")
print(df.tail(2))
print("")

print(df.describe())
print("")


df2=pd.read_csv('C:\greek_gods_v2.csv')

print(df2)
print("")
print(df2.head(2))
print("")
print(df2.tail(2))
print("")








