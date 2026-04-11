# Dataset de Referencia: Clinical cases of Dengue and Chikungunya

## Fonte

- Link: https://data.mendeley.com/datasets/bv26kznkjs/1
- Titulo: Clinical cases of Dengue and Chikungunya
- DOI: 10.17632/bv26kznkjs.1
- Publicacao: 16 Dec 2021 (Version 1)
- Licenca: CC BY 4.0

## Autores

- Thomas Tabosa
- Sebastiao Silva Neto
- Igor Teixeira
- Samuel Oliveira
- Maria Gabriela Rodrigues
- Vanderson Sampaio
- Patricia Endo

## Descricao Geral do Dataset

Este dataset apresenta informacoes clinicas e sociodemograficas de pacientes com casos confirmados de Dengue e Chikungunya, alem de casos descartados para essas doencas.

As bases de origem sao:

- SINAN (Amazonas, 2015 a 2020)
- Dados Abertos do Recife (Pernambuco, 2015 a 2020)

Arquivos publicados no pacote:

- data set.csv: versao pre-processada
- attributes.csv: dicionario/resumo dos atributos
- sinan-db.csv: base original SINAN
- recife-db.csv: base original Recife

## Dimensoes Informadas

- Base final balanceada: 17.172 registros e 27 atributos
- Distribuicao final por classe (balanceada):
  - DENGUE: 5.724
  - CHIKUNGUNYA: 5.724
  - OTHERS (OUTRAS_DOENCAS): 5.724

## Como os Dados Foram Tratados (Steps to reproduce)

Segundo a documentacao do dataset no Mendeley, o tratamento incluiu:

1. Integracao de duas fontes

- SINAN-db: 57.445 registros e 146 variaveis.
- Recife-db: 83.073 registros e 124 variaveis.

2. Definicao das classes de saida em CLASSI_FIN

- DENGUE: casos confirmados de dengue.
- CHIKUNGUNYA: casos confirmados de chikungunya.
- OTHERS: casos inconclusivos ou negativos para ambas.

3. Filtros de qualidade

- Manutencao apenas de registros confirmados ou negados por diagnostico clinico.
- Remocao de registros sem sinais/sintomas relevantes.
- Remocao de variaveis com mais de 50% de dados ausentes.
- Remocao de registros com valores faltantes em todas as variaveis.

4. Engenharia e selecao de atributos

- Criacao da variavel DIAS (dias entre inicio dos sintomas e notificacao).
- Selecao de atributos com apoio de especialistas.

5. Padronizacao e limpeza

- Codificacao de variaveis em formato numerico.
- Remocao de duplicatas.
- Substituicao de ausentes por "not informed" por variavel.

6. Balanceamento

- Aplicacao de random undersampling para equalizar as classes.
- Resultado final balanceado: 17.172 registros (5.724 por classe) e 27 atributos.

## Relacao com o Projeto Atual

No projeto atual, os arquivos em data/ correspondem ao pacote publicado no Mendeley.
A coluna CLASSI_FIN foi posteriormente codificada para inteiros para uso em modelos:

- OUTRAS_DOENCAS = 0
- CHIKUNGUNYA = 1
- DENGUE = 2

## Links Relacionados (informados na pagina do dataset)

- Repositorio associado: https://github.com/dotlab-brazil/Clinical-cases-of-Dengue-and-Chikungunya
- Fonte SINAN/DATASUS: https://datasus.saude.gov.br/transferencia-de-arquivos/#
- Dados Abertos Recife: http://dados.recife.pe.gov.br/dataset/casos-de-dengue-zika-e-chikungunya

## Citacao Recomendada

Tabosa, Thomas; Silva Neto, Sebastiao; Teixeira, Igor; Oliveira, Samuel; Rodrigues, Maria Gabriela; Sampaio, Vanderson; Endo, Patricia (2021), "Clinical cases of Dengue and Chikungunya", Mendeley Data, V1, doi: 10.17632/bv26kznkjs.1
