# Metodologia

## Plano Estrutural da Secao

1. Desenho da pesquisa.
2. Fonte, transformacao e obtencao dos dados clinicos.
3. Materiais computacionais.
4. Procedimentos metodologicos de preparacao dos dados.
5. Algoritmo de IA adotado e justificativa da escolha.
6. Treinamento, avaliacao e criterios tecnicos.
7. Nota de reprodutibilidade e rastreabilidade do pipeline.
8. Referencia do dataset utilizado.

## Texto-Base da Secao Metodologia

### 1. Desenho da pesquisa

Este trabalho adota um desenho de pesquisa observacional retrospectivo, com abordagem quantitativa e foco em modelagem preditiva supervisionada para **classificacao binaria**. O objetivo metodologico e discriminar casos clinicos em duas categorias finais da variavel alvo `CLASSI_FIN`: **OUTRAS_DOENCAS (0)** e **DENGUE (1)**. A estrategia experimental foi organizada em etapas sequenciais de verificacao da base, analise exploratoria, preparacao para aprendizado de maquina, treinamento da rede neural e avaliacao do desempenho.

### 2. Fonte, transformacao e obtencao dos dados clinicos

A base de referencia e secundaria, proveniente do dataset **Clinical cases of Dengue and Chikungunya** (Mendeley Data, DOI: 10.17632/bv26kznkjs.1), originalmente estruturado em formato multiclasse. No contexto desta versao binaria do projeto, foi utilizada uma derivacao controlada e rastreavel a partir da base multiclasse local.

No diretorio `binary_class`, o fluxo de dados foi definido da seguinte forma:

- Entrada multiclasse: `binary_class/data/data_set_final_multiclass.csv`
- Script de transformacao: `binary_class/scripts/create_binary_dataset.py`
- Saida binaria final: `binary_class/data/data_set_final.csv`

As alteracoes aplicadas sobre `CLASSI_FIN` foram:

1. **Remocao de todos os registros com `CLASSI_FIN = 1` (CHIKUNGUNYA)**;
2. **Remapeamento de `CLASSI_FIN = 2` para `CLASSI_FIN = 1` (DENGUE)**;
3. Manutencao de `CLASSI_FIN = 0` como `0` (OUTRAS_DOENCAS).

Com isso, a distribuicao final da base binaria ficou:

- `CLASSI_FIN = 0` (OUTRAS_DOENCAS): **5724** registros;
- `CLASSI_FIN = 1` (DENGUE, apos remapeamento): **5724** registros;
- **Total final: 11448 registros**.

Essas contagens estao documentadas em `binary_class/DATASET_MENDELEY.md` e sao consistentes com a execucao do script de geracao binaria.

### 3. Materiais computacionais

A implementacao foi conduzida em Python, com notebook dedicado em `binary_class/notebooks/dengue_binary_classification.ipynb`, utilizando bibliotecas cientificas consolidadas:

- `pandas` e `numpy` para leitura e manipulacao numerica dos dados;
- `matplotlib` e `seaborn` para visualizacao exploratoria e matriz de confusao;
- `scikit-learn` para divisao estratificada, padronizacao e metricas de avaliacao;
- `tensorflow/keras` para construcao, compilacao e treinamento do modelo de rede neural binaria.

No notebook, tambem ha verificacao de ambiente TensorFlow e disponibilidade de GPU, quando presente.

### 4. Procedimentos metodologicos de preparacao dos dados

A preparacao preserva os valores do arquivo final binario e aplica controles de qualidade antes da modelagem. Foram executadas verificacoes de tipos, contagem de valores ausentes e distribuicao da variavel alvo. Em seguida, os dados foram separados em:

- matriz de atributos `X` (todas as colunas, exceto `CLASSI_FIN`);
- vetor alvo `y` (`CLASSI_FIN`).

Foi realizada validacao programatica para garantir que o problema possua **exatamente duas classes (0 e 1)**. A divisao treino/teste foi executada com `train_test_split` estratificado, configurado com `test_size=0.2`, `random_state=42` e `stratify=y`, mantendo proporcionalidade de classes entre os subconjuntos.

Para evitar vazamento de informacao, a padronizacao por `StandardScaler` foi ajustada exclusivamente no conjunto de treino (`fit_transform`) e posteriormente aplicada ao conjunto de teste (`transform`).

### 5. Algoritmo de IA adotado e justificativa da escolha

O algoritmo adotado foi uma Rede Neural Artificial do tipo **Multilayer Perceptron (MLP)**, implementada via API sequencial do Keras. A arquitetura utilizada no notebook contem:

- camada de entrada com dimensionalidade dos atributos;
- duas camadas ocultas densas (128 e 64 neuronios) com ativacao **ReLU**;
- duas camadas de regularizacao `Dropout(0.25)` apos cada camada oculta;
- camada de saida com 1 neuronio e ativacao **Sigmoid**.

Justificativa tecnica:

- **ReLU nas camadas ocultas**: favorece treinamento estavel em redes densas, reduz saturacao e melhora eficiencia computacional;
- **Sigmoid na saida**: converte a saida do modelo em probabilidade no intervalo [0, 1], adequada para decisao binaria;
- **Adam**: otimizador adaptativo robusto para convergencia em problemas tabulares com redes neurais;
- **`binary_crossentropy`**: funcao de perda apropriada para classificacao binaria, pois penaliza desvios entre probabilidades preditas e rotulos binarios reais, orientando o ajuste dos pesos para separar as duas classes.

### 6. Treinamento, avaliacao e criterios tecnicos

A compilacao do modelo foi configurada com:

- otimizador `Adam(learning_rate=1e-3)`;
- perda `binary_crossentropy`;
- metrica principal `accuracy`.

O treinamento foi realizado com:

- ate `120` epocas;
- `batch_size=32`;
- validacao interna com `validation_split=0.2` sobre o conjunto de treino;
- callback `EarlyStopping` monitorando `val_loss`, com `patience=15` e `restore_best_weights=True`.

A avaliacao final foi feita no conjunto de teste e incluiu:

- `test_loss` e `test_accuracy` via `model.evaluate`;
- acuracia calculada com `accuracy_score` (scikit-learn);
- matriz de confusao;
- `classification_report` com precision, recall e F1-score por classe.

As predicoes binarias foram obtidas a partir das probabilidades da camada Sigmoid com limiar de decisao de 0.5 (`y_pred = probs >= 0.5`). Adicionalmente, curvas de treino e validacao (loss e accuracy por epoca) foram analisadas para verificar convergencia e possivel sobreajuste.

### 7. Nota de reprodutibilidade e rastreabilidade do pipeline

A reprodutibilidade do fluxo e assegurada pelos artefatos versionados no proprio diretorio `binary_class`:

1. `binary_class/data/data_set_final_multiclass.csv` (base de entrada rastreavel);
2. `binary_class/scripts/create_binary_dataset.py` (regra explicita de transformacao para binario);
3. `binary_class/data/data_set_final.csv` (base final usada no treinamento);
4. `binary_class/notebooks/dengue_binary_classification.ipynb` (pipeline completo de modelagem e avaliacao);
5. `binary_class/DATASET_MENDELEY.md` (documentacao da origem, regras e contagens finais).

Esse encadeamento permite auditar o processo desde a origem multiclasse ate o treinamento binario final, com controle das regras de remocao e remapeamento da variavel alvo.

### 8. Referencia do dataset

Tabosa, Thomas; Silva Neto, Sebastiao; Teixeira, Igor; Oliveira, Samuel; Rodrigues, Maria Gabriela; Sampaio, Vanderson; Endo, Patricia (2021), *Clinical cases of Dengue and Chikungunya*, Mendeley Data, V1. DOI: 10.17632/bv26kznkjs.1.

---

## Observacao de uso

Este texto foi elaborado para a secao de Metodologia da versao de classificacao binaria do projeto. Recomenda-se apenas adequar normas de citacao e formatacao institucional, mantendo coerencia com os scripts e notebooks efetivamente utilizados em `binary_class`.