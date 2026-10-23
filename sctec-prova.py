# ----------------------------------------------------------------------
# imports 
# ----------------------------------------------------------------------
import pandas as pd
import numpy as np
from rich.console import Console
from rich.panel import Panel
console = Console()
# ----------------------------------------------------------------------
# carregamento dos dados
# ----------------------------------------------------------------------
df = pd.read_csv("Base Varejo.csv", sep=";") 
pd.set_option("display.max_rows", 150)
# ----------------------------------------------------------------------
# tratamento dos dados
# ----------------------------------------------------------------------
#trocando os nomes para identificação mais facil 
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
# ----------------------------------------------------------------------
#trocan valores nulos para identificação mais facil no codigo
# ----------------------------------------------------------------------

df.replace(["#N/D", "N/D", "produto desconhecido", "produto desonhecido "], np.nan, inplace=True)
# funções de limpeza de dados (duplicados,linhas não prenchidas com dados)
def remover_duplicados(df):
    return df.drop_duplicates()

def remover_linhas_nulas(df, colunas=None):
    return df.dropna(subset=colunas)

#aplicando a função de limpeza de dados

df = remover_duplicados(df)
df = remover_linhas_nulas(df)
# ----------------------------------------------------------------------
#anlise de dados sobre genero 
# ----------------------------------------------------------------------

def mostrar_d_genero(df):
    #limpeza sobre dados de genero sendo contados duas vezes e pedendido para que olhe primeiro para id do cliente e ver se ele não se repete(repetiu não conta duas vezes)
    clientes_unicos = df[["codigo_de_cliente", "genero"]].drop_duplicates()
    #contagem de cada genero
    genero_numero = clientes_unicos["genero"].value_counts()
    #contagem de cada genero percentual
    genero_percentual = (clientes_unicos["genero"].value_counts(normalize=True) * 100).round(2)
    #quadrado para ficar bonito no terminal
    texto = (
        f"[bold]genero_numero:[/] (genero_numero)    "
        f"[bold]genero_percentual:[/] (genero_percentual)%"
    )
    console.print(Panel(texto, title="dados genero", expand=False))

# ----------------------------------------------------------------------
#anlise de dados sobre categorias
# ----------------------------------------------------------------------  

def mostrar_d_categorias(df):
    #contagem de consumo de cada categoria
    categorias_numero = df["categoria"].value_counts()
    #contagem de consumo de cada categoria percentual
    categorias_percentual = df["categoria"].value_counts(normalize=True) * 100
    #contagem de consumo de cada categoria e seus produtos percentual para cada area de consumo
    categorias_produto = df.groupby("categoria")["nome_do_produto"].value_counts(normalize=True) * 100
     #contagem de consumo de cada categoria e seus produtos percentua sobre o total consumido
    percentual_total = df["nome_do_produto"].value_counts(normalize=True) * 100
    texto = (
        f"[bold]categorias_numero:[/] ({categorias_numero})    "
        f"[bold]categorias_percentual:[/] ({categorias_percentual})%"
        f"[bold]categorias_produto:[/] ({categorias_produto})%"
        f"[bold]percentual_total:[/] ({percentual_total})%"
    )
    console.print(Panel(texto, title="dados categorias", expand=False))
    
# ----------------------------------------------------------------------
#anlise de dados sobre dependentes
# ----------------------------------------------------------------------


def categoria(df):
    #retirando duplicados para que não conte duas vezes o mesmo cliente
    clientes_unicos = df.drop_duplicates(subset="codigo_de_cliente")
    clientes_por_dep = clientes_unicos["dependentes"].value_counts().sort_index()
    #contagem de dependentes
    dependentes= df["dependentes"].value_counts().sort_index()
    #contagem de dependentes percentual por cada grupo pelas categorias consumidadas por cada grupo de dependentes
    dependentes_consumo=df.groupby("dependentes")["categoria"].value_counts(normalize=True) * 100
    texto = (
        f"[bold]dependentes:[/] ({dependentes})    "
        f"[bold]dependentes_consumo:[/] ({dependentes_consumo})%"
    )
    console.print(Panel(texto, title="dados categorias", expand=False))

#funções sendo chamadas e dando print no terminal 
mostrar_d_genero(df)
mostrar_d_categorias(df)
categoria(df)
