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
ARQUIVO_LIMPO = "df_limpo.csv"
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
 
 
def preencher_categoria(valor):
    """Se a categoria estiver vazia, devolve 'Sem Categoria'."""
    if pd.isna(valor):
        return "Sem Categoria"
    else:
        return valor
 
 
def preencher_nome(valor):
    """Se o nome do produto estiver vazio, devolve 'Sem Nome'."""
    if pd.isna(valor):
        return "Sem Nome"
    else:
        return valor
 
 
def tratar_dados(df):
    """Renomeia as colunas, troca os ausentes por NaN e preenche os vazios."""
    df = df.rename(columns=COLUNAS_RENOMEADAS)
    df.replace(VALORES_NULOS, np.nan, inplace=True)
 
    # Preenche categoria e nome vazios para não perder as compras
    categorias_vazias = int(df["categoria"].isna().sum())
    df["categoria"] = df["categoria"].map(preencher_categoria)
    df["nome_do_produto"] = df["nome_do_produto"].map(preencher_nome)
    print(f"Categorias preenchidas com 'Sem Categoria': {categorias_vazias}")
    return df
 
 
def executar_limpeza(df):
    """Limpa o DataFrame, salva a base limpa e devolve o resultado."""
    limpeza = LimpezaDados(df)
    df_limpo = limpeza.executar()
    limpeza.mostrar_relatorio()
    limpeza.salvar_csv(ARQUIVO_LIMPO)
    return df_limpo
 
 
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
        f"[bold]gênero número:[/] \n{genero_numero} \n\n   "
        f"[bold]gênero percentual:[/] \n{genero_percentual}%\n\n"
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
        f"[bold]categorias_numero:[/] \n{categorias_numero} \n\n   "
        f"[bold]categorias_percentual:[/] \n{categorias_percentual}%\n\n  "
        f"[bold]categorias_produto:[/] \n{categorias_produto}%\n\n"
        f"[bold]percentual_total:[/] \n{percentual_total}%\n\n"
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
 
    media = df["dependentes"].mean()
    mediana = df["dependentes"].median()
    desvio_padrao = df["dependentes"].std()
    moda = df["dependentes"].mode()[0]
    maximo = df["dependentes"].max()
    minimo = df["dependentes"].min()
    contagem = df["dependentes"].count()
    quartis = df["dependentes"].quantile([0.25, 0.50, 0.75])
 
    # Colocando no quadro
    texto = (
        f"[bold]dependentes:[/] \n{dependentes}\n\n    "
        f"[bold]clientes_consumo:[/] \n{dependentes_consumo} \n\n   "
        f"[bold]media:[/] \n{media}\n\n"
        f"[bold]mediana:[/] \n{mediana}\n\n"
        f"[bold]desvio_padrao:[/] \n{desvio_padrao}\n\n"
        f"[bold]moda:[/] \n{moda}\n\n"
        f"[bold]maximo:[/] \n{maximo}\n\n"
        f"[bold]minimo:[/] \n{minimo}\n\n"
        f"[bold]contagem:[/] \n{contagem}\n\n"
        f"[bold]quartis:[/] \n{quartis}\n\n"
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
    df = executar_limpeza(df)
 
    mostrar_d_genero(df)
    mostrar_d_categorias(df)
    mostrar_d_dependentes(df)
 
 
if __name__ == "__main__":
    main()
