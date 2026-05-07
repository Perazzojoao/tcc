# Dataset de Referencia (Versao Binaria Derivada)

## Fonte original (multiclasse)

- Link: https://data.mendeley.com/datasets/bv26kznkjs/1
- Titulo: Clinical cases of Dengue and Chikungunya
- DOI: 10.17632/bv26kznkjs.1
- Licenca: CC BY 4.0

> Importante: o dataset publicado no Mendeley e **multiclasse** (3 classes), nao binario.

## Contexto da pasta `binary_class`

Esta pasta contem uma derivacao binaria do dataset final do projeto para treinos de classificacao com 2 classes.

Arquivos principais:

- `binary_class/data/data_set_final_multiclass.csv`: **entrada padrao recomendada** (copia de rastreabilidade da base multiclasse original do projeto)
- `binary_class/data/data_set_final.csv`: **saida padrao final** (base binaria usada pelos notebooks desta pasta)
- `binary_class/scripts/create_binary_dataset.py`: script de transformacao multiclasse -> binario

## Fluxo de execucao recomendado

Comando recomendado (usa os defaults do script):

```bash
python3 binary_class/scripts/create_binary_dataset.py
```

Defaults atuais do script:

- `--input`: `binary_class/data/data_set_final_multiclass.csv`
- `--output`: `binary_class/data/data_set_final.csv`

Observacao de seguranca: o script aborta se a entrada aparentar ja estar em formato binario (ex.: existe classe `1` e nao existe classe `2`), para evitar sobrescrever o fluxo correto de derivacao.

## Regras de transformacao aplicadas

A transformacao para binario foi feita sobre a coluna `CLASSI_FIN`:

1. Remover linhas com `CLASSI_FIN == 1` (CHIKUNGUNYA)
2. Remapear `CLASSI_FIN == 2` para `1` (DENGUE)
3. Manter `CLASSI_FIN == 0` como `0` (OUTRAS_DOENCAS)

Resultado semantico final:

- `0 = OUTRAS_DOENCAS`
- `1 = DENGUE`

## Contagens reais da base binaria gerada

Contagens observadas no arquivo `binary_class/data/data_set_final.csv`:

- `CLASSI_FIN = 0 (OUTRAS_DOENCAS)`: **5724**
- `CLASSI_FIN = 1 (DENGUE)`: **5724**

Total de registros da base binaria: **11448**

## Comparacao com a base multiclasse de origem

Antes da transformacao (multiclasse codificada):

- `0 (OUTRAS_DOENCAS)`: 5724
- `1 (CHIKUNGUNYA)`: 5724
- `2 (DENGUE)`: 5724
- Total: 17172

Depois da transformacao binaria:

- `0 (OUTRAS_DOENCAS)`: 5724
- `1 (DENGUE)`: 5724
- Total: 11448
