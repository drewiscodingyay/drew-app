import pandas as pd
data=pd.read_csv('utils\CrimesOnWomenData - Copy.csv', sep =";")
print("HEAD:")
print(data.head())
print("TAIL:")
print(data.tail())