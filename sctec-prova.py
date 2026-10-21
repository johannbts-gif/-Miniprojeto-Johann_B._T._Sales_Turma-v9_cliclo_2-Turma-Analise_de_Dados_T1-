import pandas as pd
df = pd.read_csv("Base Varejo.csv", sep=";") 
pd.set_option("display.max_rows", 150)
df = df.rename(columns={
    "CO_ID": "codigo_de_compra",
    "CL_ID": "codigo_de_cliente",
    "CL_GENERO": "genero",
    "CL_EC": "estado_civil",
    "CL_FHL": "Dependentes",
    "CL_SEG": "segmento",
    "PR_CAT": "categoria",
    "PR_NOME": "nome_do_produto",
    "PR_ID": "codigo_do_produto"
})
consumo_por_cliente = df["codigo_de_cliente"].value_counts()
  
print(df.head())
print(df["genero"].value_counts())
print(df['genero'].value_counts(normalize=True) * 100)
print(df["categoria"].value_counts())
#print(df.groupby("categoria")["nome_do_produto"].value_counts())
#print(consumo_por_cliente.head(10))
