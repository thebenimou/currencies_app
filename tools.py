import pandas as pd
import requests


url = "https://api.exchangeratesapi.io/history?start_at=1999-01-01&end_at=2020-12-02&base=USD"
resp = requests.get(url)
dico = resp.json()
df_0 = pd.DataFrame.from_records(dico['rates']).transpose()
df_0['date'] = df_0.index
df_0['date'] = pd.to_datetime(df_0['date'])
df_0 = df_0.melt(id_vars=df_0.columns[-1])
df_0.rename(columns={"variable": "currency"}, inplace=True)
df_0['year'] = df_0['date'].apply(lambda x: x.year)

transco = pd.read_csv("transco.csv", sep=";")
transco.index = transco["abbr"]
transco_dic = transco.to_dict()['label']

# on filtre que là où la transco est dispo
df = df_0[df_0.currency.isin(list(transco_dic.keys()))]
