import pandas as pd

# Ler o arquivo JSON
df = pd.read_json('data/sales_records.json')

# Salvar o DataFrame em um arquivo CSV
df.to_csv('data/sales_records.csv', index=False)
