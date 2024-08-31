import pandas as pd
import json

# Lee el archivo csv
df = pd.read_csv('nomys_initial.csv')

# Guarda el DataFrame como JSON
df.to_json('nomys.json', orient='records')

with open('nomys.json', 'r') as file:
    nomys = json.load(file)

for i in range(100):
    nomy = nomys[i]
    print(nomy)
    break