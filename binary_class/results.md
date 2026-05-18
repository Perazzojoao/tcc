# Resultados e Discussão — Classificação Binária de Dengue

**Projeto:** binary_class  
**Dataset:** `data/data_set_final.csv` (carregado nos notebooks como `../data/data_set_final.csv`)  
**Target:** `CLASSI_FIN`  
**Split:** `train_test_split(test_size=0.2, random_state=42, stratify=y)`  
**Ambiente:** Python 3.12.4 (Anaconda3, env `tf_gpu`)

---

## 4.1 — Desempenho do Random Forest

**Métricas principais (teste):**
- Precisão (precision): **0.6712**
- Recall: **0.6934**
- F1-score: **0.6821**
- AUC-ROC: **0.7331**
- Acurácia: **0.6769**

**Matriz de confusão (real x predito):**
- TN = 756
- FP = 389
- FN = 351
- TP = 794

**Interpretação do comportamento:**
- Modelo com desempenho intermediário e estável para dados tabulares.
- Recall ligeiramente maior que precision, indicando tendência a recuperar mais casos positivos ao custo de mais falsos positivos.

**Pontos fortes:**
- Boa robustez sem necessidade de escalonamento.
- Treinamento e interpretação operacional simples.

**Limitações:**
- Separação entre classes inferior ao XGBoost (AUC menor).
- Número relevante de FP/FN para um cenário clínico sensível.

---

## 4.2 — Desempenho do XGBoost

**Métricas principais (teste):**
- Precisão (precision): **0.7009**
- Recall: **0.7039**
- F1-score: **0.7024**
- AUC-ROC: **0.7681**
- Acurácia: **0.7017**

**Matriz de confusão (real x predito):**
- TN = 801
- FP = 344
- FN = 339
- TP = 806

**Interpretação do comportamento:**
- Melhor equilíbrio entre precisão e recall dentre os três modelos.
- Melhor poder de discriminação global (maior AUC), sugerindo maior capacidade de separação das classes 0 e 1.

**Pontos fortes:**
- Melhor desempenho geral neste experimento.
- Menor quantidade de erros totais na matriz de confusão em relação aos demais.

**Limitações:**
- Dependência de pacote externo (`xgboost`) e maior custo de tuning.
- Pode demandar mais cuidado de hiperparâmetros para reprodutibilidade entre ambientes.

---

## 4.3 — Desempenho do MLP

**Métricas principais (teste):**
- Precisão (precision): **0.6558**
- Recall: **0.6873**
- F1-score: **0.6712**
- AUC-ROC: **0.7060**
- Acurácia: **0.6633**

**Matriz de confusão (real x predito):**
- TN = 732
- FP = 413
- FN = 358
- TP = 787

**Interpretação do comportamento:**
- Desempenho inferior aos modelos de árvore/boosting neste conjunto tabular.
- Apesar de capturar não linearidades, apresentou maior volume de falsos positivos.

**Pontos fortes:**
- Estratégia de preparação correta com **StandardScaler sem vazamento** (fit no treino, transform no treino e teste).
- Modelo flexível para relações complexas.

**Limitações:**
- Menores métricas globais neste cenário.
- Sensível a hiperparâmetros e convergência (necessita tuning adicional).

---

## Comparação final entre modelos e recomendação técnica

### Comparativo sintético
- **XGBoost**: melhor desempenho geral (Accuracy, F1 e AUC mais altos).
- **Random Forest**: segunda melhor opção, robusta e simples.
- **MLP**: desempenho inferior no dataset atual, mesmo com escalonamento adequado.

### Recomendação técnica
Para o cenário de classificação binária de dengue com este dataset, a recomendação é **XGBoost como modelo principal**, devido ao melhor equilíbrio entre precision/recall e maior AUC-ROC (0.7681), indicando melhor capacidade discriminativa.  
Como alternativa de baseline operacional mais simples, manter **Random Forest**.  
O **MLP** pode ser retomado em ciclos futuros com tuning mais profundo (arquitetura, regularização e parada antecipada), mas não é a melhor escolha no estado atual.

---

## Reprodutibilidade
- Seed fixa: `RANDOM_STATE = 42`
- Split estratificado em todos os notebooks.
- Métricas obrigatórias presentes em todos: classification report, matriz de confusão, curva ROC + AUC.
- Célula final de validação em cada notebook com status e versão do Python.
