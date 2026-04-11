# Metodologia

## Plano Estrutural da Secao

1. Desenho da pesquisa.
2. Fonte e obtencao dos dados clinicos.
3. Materiais computacionais (Google Colab, Python e bibliotecas).
4. Procedimentos metodologicos de preparacao e modelagem.
5. Algoritmo de IA adotado e justificativa da escolha.
6. Treinamento, avaliacao e criterios tecnicos.
7. Nota resumida de reprodutibilidade do pipeline de dados.
8. Referencia do dataset utilizado.

## Texto-Base da Secao Metodologia

### 1. Desenho da pesquisa

Este trabalho adota um desenho de pesquisa observacional retrospectivo, com abordagem quantitativa e foco em modelagem preditiva supervisionada multiclasse. O objetivo metodologico e classificar casos clinicos em tres categorias diagnosticas, representadas pela variavel alvo CLASSI_FIN: OUTRAS_DOENCAS (0), CHIKUNGUNYA (1) e DENGUE (2). A estrategia experimental foi estruturada em etapas sequenciais de inspecao dos dados, analise exploratoria, preparacao para aprendizado de maquina, treinamento do modelo e avaliacao de desempenho.

### 2. Fonte e obtencao dos dados clinicos

Os dados utilizados sao secundarios e foram obtidos a partir do pacote Clinical cases of Dengue and Chikungunya, disponibilizado no Mendeley Data (DOI: 10.17632/bv26kznkjs.1). Conforme documentacao da base, o conjunto agrega registros provenientes do SINAN (Amazonas) e dos Dados Abertos do Recife, ambos no periodo de 2015 a 2020.

No fluxo implementado, foi utilizado o arquivo data_set_final.csv, contendo 17172 registros e 27 colunas, com distribuicao balanceada entre as tres classes (5724 amostras por classe). O notebook realiza leitura direta desse arquivo e validacao explicita da coluna alvo como tipo numerico inteiro, assegurando compatibilidade com o treinamento multiclasse.

### 3. Materiais computacionais

A implementacao foi conduzida em ambiente Google Colab, utilizando Python e bibliotecas cientificas consolidadas para manipulacao de dados, visualizacao e modelagem.

As bibliotecas empregadas no pipeline foram:

- pandas: leitura e manipulacao tabular do dataset.
- numpy: operacoes numericas e estruturacao de arrays para treinamento.
- matplotlib e seaborn: geracao dos graficos de analise exploratoria, matriz de correlacao e matriz de confusao.
- scikit-learn: divisao estratificada entre treino e teste, padronizacao de atributos e metricas de avaliacao.
- tensorflow/keras: construcao, compilacao e treinamento da rede neural multiclasses.

No registro de execucao do notebook, consta TensorFlow versao 2.21.0, compilacao com suporte CUDA e deteccao de GPU visivel no ambiente.

### 4. Procedimentos metodologicos de preparacao dos dados

A etapa de preparacao foi realizada sem alteracao semantica dos atributos finais do dataset. Inicialmente, os dados foram submetidos a verificacoes de qualidade, incluindo tipos de variaveis, ausencia de valores nulos e distribuicao da classe alvo. Em seguida, foi conduzida analise exploratoria com grafico de distribuicao das classes e mapa de correlacao entre variaveis numericas.

Posteriormente, os dados foram separados em matriz de atributos (X) e vetor alvo (y), com verificacao programatica de consistencia para garantir exatamente tres classes codificadas (0, 1 e 2). A divisao entre treino e teste foi feita com train_test_split estratificado, proporcao 80/20, random_state=42 e preservacao da proporcao de classes nos subconjuntos. Para evitar vazamento de informacao entre conjuntos, a padronizacao com StandardScaler foi ajustada apenas no conjunto de treino e aplicada ao conjunto de teste.

### 5. Algoritmo de IA escolhido e justificativa

O algoritmo adotado foi uma Rede Neural Artificial do tipo Multilayer Perceptron (MLP), implementada com arquitetura sequencial densa. A configuracao aplicada contem camada de entrada com dimensionalidade dos atributos, duas camadas ocultas totalmente conectadas (128 e 64 neuronios, ambas com ativacao ReLU), regularizacao por Dropout de 0.25 apos cada camada oculta e camada de saida com 3 neuronios e ativacao Softmax.

A escolha desta arquitetura foi motivada pela natureza do problema, que envolve classificacao supervisionada multiclasse em dados tabulares clinicos codificados numericamente. A funcao de ativacao ReLU foi empregada por favorecer estabilidade de treinamento e eficiencia computacional em camadas densas. O uso de duas camadas ocultas com 128 e 64 neuronios busca equilibrar capacidade de representacao e controle de complexidade do modelo. O Dropout de 0.25 foi utilizado para reduzir risco de sobreajuste durante as epocas de treinamento. A camada Softmax, em conjunto com a perda sparse_categorical_crossentropy, e adequada para saida probabilistica em classes mutuamente exclusivas representadas por rotulos inteiros.

### 6. Treinamento e avaliacao do modelo

A compilacao do modelo foi realizada com otimizador Adam (learning_rate=1e-3), funcao de perda sparse_categorical_crossentropy e metrica principal de acuracia. O treinamento foi configurado com ate 120 epocas, batch_size=32 e validacao interna com validation_split=0.2 no conjunto de treino.

Para controle de sobreajuste, foi utilizada a estrategia EarlyStopping monitorando val_loss, com patience=15 e restauracao automatica dos melhores pesos ao final do processo. A avaliacao final foi executada no conjunto de teste e incluiu: loss e acuracia, acuracia via sklearn, matriz de confusao e classification report (precision, recall e F1-score por classe). Adicionalmente, foram analisadas curvas de treinamento e validacao (loss e accuracy por epoca) para observacao da convergencia do aprendizado.

### 7. Nota de reprodutibilidade do pipeline de dados

Antes da execucao do notebook, foram utilizados dois scripts auxiliares do projeto para preparar o arquivo final consumido pelo modelo:

- scripts/fix_csv_format.py: padroniza o delimitador do CSV de origem para formato com virgula, preservando consistencia estrutural.
- scripts/encode_classi_fin.py: codifica a coluna CLASSI_FIN para rotulos numericos (OUTRAS_DOENCAS=0, CHIKUNGUNYA=1, DENGUE=2), gerando o arquivo data_set_final.csv.

Essas etapas permitem rastreabilidade do fluxo de dados desde o arquivo bruto ate o conjunto final utilizado na modelagem.

### 8. Referencia do dataset

Tabosa, Thomas; Silva Neto, Sebastiao; Teixeira, Igor; Oliveira, Samuel; Rodrigues, Maria Gabriela; Sampaio, Vanderson; Endo, Patricia (2021), Clinical cases of Dengue and Chikungunya, Mendeley Data, V1. DOI: 10.17632/bv26kznkjs.1.

---

## Observacao de uso

Este texto foi redigido para servir como base da secao Metodologia da monografia. Recomenda-se ajustar apenas padroes de citacao, numeracao de secoes e eventuais exigencias formais da instituicao, mantendo a correspondencia com o fluxo efetivamente implementado no notebook dengue_classification.ipynb.
