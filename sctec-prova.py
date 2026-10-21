import pandas as pd

df = pd.read_csv("Base Varejo.csv", sep=";")
df = df.rename(columns={
    "CO_ID": "codigo_de_compra",
    "CL_ID": "codigo_de_cliente",
    "CL_GENERO": "genero",
    "CL_EC": "estado_civil",
    "CL_FHL": "dependentes",
    "CL_SEG": "segmento",
    "PR_CAT": "categoria",
    "PR_NOME": "nome_do_produto",
    "PR_ID": "codigo_do_produto"
})
print(df.head())
