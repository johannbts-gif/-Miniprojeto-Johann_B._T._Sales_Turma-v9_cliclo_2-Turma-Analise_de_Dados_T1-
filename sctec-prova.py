# ----------------------------------------------------------------------
# Imports 
# ----------------------------------------------------------------------

import pandas as pd
import numpy as np
from rich.console import Console
from rich.panel import Panel
import os
console = Console()

# ----------------------------------------------------------------------
# Carregamento dos dados
# ----------------------------------------------------------------------

CAMINHO_CSV = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Base varejo.csv")
df = pd.read_csv(CAMINHO_CSV, sep=";")
pd.set_option("display.max_rows", 150)


# ----------------------------------------------------------------------
# Tratamento dos dados
# ----------------------------------------------------------------------


# Trocando os nomes para identificação mais facil 
# ----------------------------------------------------------------------

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
# Limpeza dos dados
# ----------------------------------------------------------------------

df.replace(["#N/D", "N/D", "produto desconhecido", "produto desonhecido "], np.nan, inplace=True)
# funções de limpeza de dados (duplicados,linhas não prenchidas com dados)
class LimpezaDados:
    def __init__(self, df):
        self.df = df
        self.registros_iniciais = len(df)

    def remover_duplicados(self):
        self.df = self.df.drop_duplicates().reset_index(drop=True)
        return self

    def remover_colunas_vazias(self):
        self.df = self.df.dropna(axis=1, how="all")
        return self
    def remover_nulos(self):
      self.df = self.df.dropna()
      return self
    def executar(self):
       self.remover_colunas_vazias().remover_nulos().remover_duplicados()
       return self.df
    def mostrar_relatorio(self):
       print(f"Registros iniciais: {self.registros_iniciais}")
       print(f"Registros removidos: {self.registros_iniciais -len(self.df)}")
       print(f"Registros finais: {len(self.df)}")
    def salvar_csv(self, nome_arquivo_saida):
        caminho_saida = os.path.join(os.path.dirname(os.path.abspath(__file__)), nome_arquivo_saida)
        self.df.to_csv(caminho_saida, index=False, sep=";")
        print(f"Base limpa salva com sucesso em: {caminho_saida}")

# Aplicando a função de limpeza de dados

if __name__ == "__main__":
 limpeza = LimpezaDados(pd.read_csv(CAMINHO_CSV, sep=";"))
 limpeza.executar()
 limpeza.mostrar_relatorio()
 limpeza.salvar_csv(CAMINHO_CSV)
 print(f"Base limpa salva em: {CAMINHO_CSV}")
 

# ----------------------------------------------------------------------
# Análise de dados sobre gênero 
# ----------------------------------------------------------------------

def mostrar_d_genero(df):
    # Remove clientes duplicados pelo ID para evitar contagens repetidas
    clientes_unicos = df[["codigo_de_cliente", "genero"]].drop_duplicates()

    #contagem de cada gênero
    genero_numero = clientes_unicos["genero"].value_counts()

    #contagem de cada gênero percentual
    genero_percentual = (clientes_unicos["genero"].value_counts(normalize=True) * 100).round(2)

    #       colocando no quadro
    texto = (
        f"[bold]gênero número:[/] {genero_numero}    "
        f"[bold]gênero percentual:[/] {genero_percentual}%"
    )
    console.print(Panel(texto, title="dados gênero", expand=False))

# ----------------------------------------------------------------------
# Análise de dados sobre categorias
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
        f"[bold]categorias_numero:[/] {categorias_numero}    "
        f"[bold]categorias_percentual:[/] {categorias_percentual}%"
        f"[bold]categorias_produto:[/] {categorias_produto}%"
        f"[bold]percentual_total:[/] {percentual_total}%"
    )
    console.print(Panel(texto, title="dados categorias", expand=False))
    
# ----------------------------------------------------------------------
# Análise de dados sobre dependentes
# ----------------------------------------------------------------------


def categoria(df):
    #retirando duplicados para que não conte duas vezes o mesmo cliente
    clientes_unicos = df.drop_duplicates(subset="codigo_de_cliente")
    clientes_por_dep = clientes_unicos["dependentes"].value_counts().sort_index()
    #contagem de dependentes
    dependentes= df["dependentes"].value_counts().sort_index()
    #contagem de dependentes percentual por cada grupo pelas categorias consumidadas por cada grupo de dependentes
    dependentes_consumo=df.groupby("dependentes")["categoria"].value_counts(normalize=True) * 100
   
    #    colocando no quadro

    texto = (
        f"[bold]dependentes:[/] {dependentes}    "
        f"[bold]dependentes_consumo:[/] {dependentes_consumo}%"
    )
    console.print(Panel(texto, title="dados categorias", expand=False))

# ----------------------------------------------------------------------
# Funções sendo chamadas e dando print no terminal 
# ----------------------------------------------------------------------

mostrar_d_genero(df)
mostrar_d_categorias(df)
categoria(df)
