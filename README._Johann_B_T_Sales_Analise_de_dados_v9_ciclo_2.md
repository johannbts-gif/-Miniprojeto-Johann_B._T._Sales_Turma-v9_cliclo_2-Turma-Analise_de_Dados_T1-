Mini-Projeto do SCTEC

Nome: Johann B. T. Sales Turma: Analise_de_Dados_T1

Para que serve o programa?

Para analisar alguns dos dados fornecidos pela fonte do Kaggle (https://www.kaggle.com/datasets/namespaiva/base-varejo/data). Meu objetivo foi utilizar o que conheço e o que aprendi para fornecer uma base de informações sobre a database.

Como usar

Abra o Visual Studio Code, abra a pasta do projeto e deixe o CSV da base na mesma pasta do programa. Os imports necessários são o pandas, o numpy e o rich (Console e Panel), além do os, que já vem com o Python. Instale com pip install pandas numpy rich e execute com python sctec-prova.py. Há mais detalhes no arquivo de instruções do repositório.

Sobre a base

A base tem 830.000 registros de compras. Cada linha traz o código da compra, o código do cliente, o gênero, o estado civil, o número de filhos (que no programa chamo de dependentes), o segmento, o código do produto, a categoria e o nome do produto.

O que o programa faz

Primeiro o programa carrega o CSV e troca os nomes das colunas por nomes mais fáceis de entender, como codigo_de_cliente, genero e dependentes. Depois troca os valores "#N/D" por NaN, para o pandas reconhecer que são dados ausentes, e preenche esses vazios com "Sem Categoria" (na categoria) e "Sem Nome" (no nome do produto), usando if/else, para não perder essas compras. A limpeza fica em uma classe chamada LimpezaDados, que remove colunas vazias, linhas com nulos e linhas duplicadas, e mostra um relatório. A base limpa é salva em um arquivo novo, o df_limpo.csv, e o CSV original não é alterado. Nesta base foram preenchidas 3.650 categorias vazias ("#N/D") e removidas 96.553 linhas duplicadas. Sobraram 733.447 registros dos 830.000 iniciais.

Em seguida o programa faz três análises e mostra cada uma em uma caixa do rich. Na de gênero, cada cliente é contado uma vez só (usei o código do cliente para não contar o mesmo cliente de novo a cada compra). Na de categorias, ele conta o consumo de cada categoria e a participação de cada produto. Na de dependentes, ele conta os registros por número de filhos, calcula o consumo de cada categoria dentro de cada grupo e mostra as estatísticas: média, mediana, desvio padrão, moda, máximo, mínimo, contagem e quartis.

Principais insights
A base tem 1.000 clientes distintos, sendo 519 do gênero feminino (51,9%) e 481 do masculino (48,1%). A divisão é bem equilibrada.
Alimentos é a categoria mais consumida, com 52,38% dos registros. Depois vêm Higiene (18,77%), Limpeza (17,54%), Bebidas (5,22%), Pet (3,89%) e Acessórios (1,75%). Os registros sem categoria somam 0,44%.
O produto mais vendido de toda a base é o presunto cozido, com 1,73% do total. Dentro de cada categoria também chamam atenção a chupeta, que responde por 50,22% dos acessórios, e a ração seca para cães, com 22,53% da categoria Pet.
Sobre o número de filhos, a média é 1,15, a mediana é 0, a moda é 0, o desvio padrão é 1,42, o mínimo é 0 e o máximo é 4. Os quartis são 0, 0 e 2. Isso mostra que a maior parte dos registros é de clientes sem filhos (52,5%). Essas estatísticas foram calculadas sobre os 733.447 registros de compra que sobraram depois da limpeza.
O consumo por categoria é praticamente igual para qualquer número de filhos. A maior diferença entre os grupos é de apenas 0,34 ponto percentual (em Alimentos), então ter mais ou menos filhos quase não muda o que o cliente compra.

Um ponto de atenção: as linhas com "#N/D" eram todas de um único produto (o de código 107), então não dá para saber a categoria dele. Elas ficaram como "Sem Categoria" e por isso as porcentagens das outras categorias são cerca de 0,2 ponto percentual menores do que seriam se essas linhas fossem ignoradas. 
Porque  manteve valores #N/D ?
interpretei que este valor se deve em relação a um produto que foi comprado mas no ato de registrar o produto a maquina falhou,supostamente e hipoteticamente, em reconhecer o produto assim registrando como n/d.Se eu retirase este valor ao rodar o programa um cliente que comprou um unico produto não seria registrado na conta do mercado ,ou seja,estaria alterando os valores de dependentes,genero,horario e entre outros.Desta forma,ao não excluir este dado ainda mantenho na minha data base o conhecimento do cliente registrado ao invés de ignorar e evitando criar um vies sobre meus clientes. 

