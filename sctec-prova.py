
# ----------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------

import os
 
import numpy as np
import pandas as pd
from rich.console import Console
from rich.panel import Panel
 
# ----------------------------------------------------------------------
# Constantes
# ----------------------------------------------------------------------
 
DIRETORIO_SCRIPT = os.path.dirname(os.path.abspath(__file__))
CAMINHO_CSV = os.path.join(DIRETORIO_SCRIPT, "Base varejo.csv")
SEPARADOR_CSV = ";"
MAX_LINHAS_EXIBIDAS = 150
 
# Nomes originais das colunas -> nomes de identificação mais fácil
COLUNAS_RENOMEADAS = {
    "CO_ID": "codigo_de_compra",
    "CL_ID": "codigo_de_cliente",
    "CL_GENERO": "genero",
    "CL_EC": "estado_civil",
    "CL_FHL": "dependentes",
    "CL_SEG": "segmento",
    "PR_CAT": "categoria",
    "PR_NOME": "nome_do_produto",
    "PR_ID": "codigo_do_produto",
}
 
# Textos que representam valores ausentes e serão trocados por NaN
VALORES_NULOS = [
    "#N/D",
    "N/D",
    "produto desconhecido",
    "produto desonhecido ",
]
 
console = Console()
 
 
# ----------------------------------------------------------------------
# Limpeza dos dados
# ----------------------------------------------------------------------
 
class LimpezaDados:
    """Limpa um DataFrame e informa quantos registros foram removidos."""
 
    def __init__(self, df):
        self.df = df
        self.registros_iniciais = len(df)
 
    def remover_duplicados(self):
        """Remove linhas duplicadas e reinicia o índice."""
        self.df = self.df.drop_duplicates().reset_index(drop=True)
        return self
 
    def remover_colunas_vazias(self):
        """Remove colunas em que todos os valores são nulos."""
        self.df = self.df.dropna(axis=1, how="all")
        return self
 
    def remover_nulos(self):
        """Remove linhas que tenham algum valor nulo."""
        self.df = self.df.dropna()
        return self
 
    def executar(self):
        """Executa todas as etapas de limpeza e devolve o DataFrame."""
        self.remover_colunas_vazias().remover_nulos().remover_duplicados()
        return self.df
 
    def mostrar_relatorio(self):
        """Mostra no terminal o resumo da limpeza."""
        print(f"Registros iniciais: {self.registros_iniciais}")
        print(f"Registros removidos: {self.registros_iniciais - len(self.df)}")
        print(f"Registros finais: {len(self.df)}")
 
    def salvar_csv(self, nome_arquivo_saida):
        """Salva a base limpa em CSV."""
        caminho_saida = os.path.join(DIRETORIO_SCRIPT, nome_arquivo_saida)
        self.df.to_csv(caminho_saida, index=False, sep=SEPARADOR_CSV)
        print(f"Base limpa salva com sucesso em: {caminho_saida}")
 
 
def carregar_dados():
    """Lê o arquivo CSV da base Varejo."""
    return pd.read_csv(CAMINHO_CSV, sep=SEPARADOR_CSV)
 
 
def tratar_dados(df):
    """Renomeia as colunas e troca os valores ausentes por NaN."""
    df = df.rename(columns=COLUNAS_RENOMEADAS)
    df.replace(VALORES_NULOS, np.nan, inplace=True)
    return df
 
 
def executar_limpeza():
    """Aplica a limpeza sobre o CSV e salva o resultado."""
    limpeza = LimpezaDados(pd.read_csv(CAMINHO_CSV, sep=SEPARADOR_CSV))
    limpeza.executar()
    limpeza.mostrar_relatorio()
    limpeza.salvar_csv(CAMINHO_CSV)
    print(f"Base limpa salva em: {CAMINHO_CSV}")
 
 
# ----------------------------------------------------------------------
# Análise de dados sobre gênero
# ----------------------------------------------------------------------
 
def mostrar_d_genero(df):
    """Mostra a quantidade e o percentual de clientes por gênero."""
    # Remove clientes duplicados pelo ID para evitar contagens repetidas
    clientes_unicos = df[["codigo_de_cliente", "genero"]].drop_duplicates()
 
    # Contagem de cada gênero
    genero_numero = clientes_unicos["genero"].value_counts()
 
    # Percentual de cada gênero
    genero_percentual = (
        clientes_unicos["genero"].value_counts(normalize=True) * 100
    ).round(2)
 
    # Colocando no quadro
    texto = (
        f"[bold]gênero número:[/] {genero_numero}    "
        f"[bold]gênero percentual:[/] {genero_percentual}%"
    )
    console.print(Panel(texto, title="DADOS GÊNERO", expand=False))
 
 
# ----------------------------------------------------------------------
# Análise de dados sobre categorias
# ----------------------------------------------------------------------
 
def mostrar_d_categorias(df):
    """Mostra o consumo por categoria e por produto."""
    # Contagem de consumo de cada categoria
    categorias_numero = df["categoria"].value_counts()
 
    # Percentual de consumo de cada categoria
    categorias_percentual = df["categoria"].value_counts(normalize=True) * 100
 
    # Percentual de cada produto dentro da sua categoria
    categorias_produto = (
        df.groupby("categoria")["nome_do_produto"]
        .value_counts(normalize=True) * 100
    )
 
    # Percentual de cada produto sobre o total consumido
    percentual_total = df["nome_do_produto"].value_counts(normalize=True) * 100
 
    texto = (
        f"[bold]categorias_numero:[/] {categorias_numero}    "
        f"[bold]categorias_percentual:[/] {categorias_percentual}%"
        f"[bold]categorias_produto:[/] {categorias_produto}%"
        f"[bold]percentual_total:[/] {percentual_total}%"
    )
    console.print(Panel(texto, title="DADOS CATEGORIAS", expand=False))
 
 
# ----------------------------------------------------------------------
# Análise de dados sobre dependentes
# ----------------------------------------------------------------------
 
def mostrar_d_dependentes(df):
    """Mostra a contagem de dependentes e o consumo de cada grupo."""
    # Retira duplicados para não contar duas vezes o mesmo cliente
    clientes_unicos = df.drop_duplicates(subset="codigo_de_cliente")
    clientes_por_dep = (
        clientes_unicos["dependentes"].value_counts().sort_index()
    )
 
    # Contagem de dependentes
    dependentes = df["dependentes"].value_counts().sort_index()
 
    # Percentual de cada categoria consumida por grupo de dependentes
    dependentes_consumo = (
        df.groupby("dependentes")["categoria"]
        .value_counts(normalize=True) * 100
    )
 
    # Colocando no quadro
    texto = (
        f"[bold]dependentes:[/] {dependentes}    "
        f"[bold]dependentes_consumo:[/] {dependentes_consumo}%"
    )
    console.print(Panel(texto, title="DADOS DEPENDENTES", expand=False))
 
 
# ----------------------------------------------------------------------
# Programa principal
# ----------------------------------------------------------------------
 
def main():
    """Carrega, trata e limpa a base e exibe as análises no terminal."""
    df = carregar_dados()
    pd.set_option("display.max_rows", MAX_LINHAS_EXIBIDAS)
    df = tratar_dados(df)
 
    executar_limpeza()
 
    mostrar_d_genero(df)
    mostrar_d_categorias(df)
    mostrar_d_dependentes(df)
 
 
if __name__ == "__main__":
    main()
