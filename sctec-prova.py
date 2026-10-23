import pandas as pd
import numpy as np
from rich.console import Console
from rich.panel import Panel

df = pd.read_csv("Base Varejo.csv", sep=";") 
pd.set_option("display.max_rows", 150)
console = Console()

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
df.replace(["#N/D", "N/D", "", " "], np.nan, inplace=True)
consumo_por_cliente = df["codigo_de_cliente"].value_counts()

def remover_duplicados(df):
    return df.drop_duplicates()

def remover_linhas_nulas(df, colunas=None):
    return df.dropna(subset=colunas)

df = remover_duplicados(df)
df = remover_linhas_nulas(df)

def mostrar_d_genero(df):
    genero_numero = df["genero"].value_counts()
    genero_percentual = df["genero"].value_counts(normalize=True) * 100
    texto = (
        f"[bold]genero_numero:[/] ({genero_numero})    "
        f"[bold]genero_percentual:[/] ({genero_percentual})%"
    )
    console.print(Panel(texto, title="dados genero", expand=False))
def mostrar_d_categorias(df):
    categorias_numero = df["categoria"].value_counts()
    categorias_percentual = df["categoria"].value_counts(normalize=True) * 100
    categorias_produto = df.groupby("categoria")["nome_do_produto"].value_counts(normalize=True) * 100
    percentual_total = df["nome_do_produto"].value_counts(normalize=True) * 100
    texto = (
        f"[bold]categorias_numero:[/] ({categorias_numero})    "
        f"[bold]categorias_percentual:[/] ({categorias_percentual})%"
        f"[bold]categorias_produto:[/] ({categorias_produto})%"
        f"[bold]percentual_total:[/] ({percentual_total})%"
    )
    console.print(Panel(texto, title="dados categorias", expand=False))

def categoria(df):
    dependentes= df["dependentes"].value_counts()
    dependentes_consumo=df.groupby("dependentes")["categoria"].value_counts()
    texto = (
        f"[bold]dependentes:[/] ({dependentes})    "
        f"[bold]dependentes_consumo:[/] ({dependentes_consumo})%"
    )
    console.print(Panel(texto, title="dados categorias", expand=False))

mostrar_d_genero(df)
mostrar_d_categorias(df)
categoria(df)
