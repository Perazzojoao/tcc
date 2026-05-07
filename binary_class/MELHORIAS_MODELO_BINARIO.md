# Melhorias do Modelo Binário

## 1) Contexto atual (resumo)

- **Tipo de problema**: classificação binária.
- **Pipeline atual (alto nível)**: preparação de dados tabulares, divisão treino/teste, treinamento de modelo base, avaliação por métricas globais e por classe.
- **Métricas atuais aproximadas (notebook)**:
  - **Accuracy**: ~**0,68**
  - **Recall por classe**: ~**0,68** (em média, com variação por classe)
- **Leitura prática**: o modelo está melhor que aleatório, mas ainda com margem relevante para ganhos de sensibilidade (recall) e estabilidade entre classes.

---

## 2) Estratégias para melhorar performance

## Curto prazo (rápido retorno)

1. **Threshold tuning (ajuste de limiar de decisão)**
   - Não fixar corte em 0,5 automaticamente.
   - Buscar limiar que maximize o objetivo do negócio (ex.: recall mínimo com precisão aceitável).

2. **Validação cruzada estratificada (Stratified K-Fold)**
   - Substituir avaliação por uma única divisão por validação robusta (ex.: 5 ou 10 folds).
   - Reduzir risco de overfitting ao split atual.

3. **Ajuste de hiperparâmetros (baseline forte)**
   - Fazer busca controlada (Random Search/Bayesian) para modelo atual antes de trocar arquitetura.
   - Otimizar diretamente métricas-alvo (ex.: recall macro, F1 macro, PR-AUC).

4. **Tratamento de desbalanceamento (se aplicável)**
   - Testar `class_weight`, undersampling/oversampling (SMOTE) e comparar impacto em recall.

## Médio prazo (ganho estrutural)

1. **Modelos tabulares de alto desempenho**
   - Testar **XGBoost**, **LightGBM** e **CatBoost** com validação estratificada.
   - Esses modelos geralmente superam baselines lineares/árvores simples em dados tabulares.

2. **Engenharia de atributos orientada a erro**
   - Criar variáveis com base nos padrões de falsos negativos/falsos positivos.
   - Explorar interações, agregações, binning e transformações log para caudas longas.

3. **Calibração de probabilidades**
   - Aplicar Platt Scaling ou Isotonic Regression para melhorar qualidade das probabilidades.
   - Fundamental quando threshold tuning é decisivo.

4. **Ensemble simples e efetivo**
   - Soft voting/stacking entre 2–4 modelos fortes e complementares.

## Longo prazo (escala e robustez)

1. **Pipeline de experimentação reprodutível**
   - Versionar dados, features, parâmetros e métricas (MLflow/DVC ou equivalente).

2. **Feature store e padronização de entrada**
   - Garantir consistência treino vs produção.

3. **Monitoramento contínuo + re-treino periódico**
   - Definir gatilhos de drift e desempenho para atualização automática/semi-automática.

---

## 3) Experimentos recomendados (ordem prática)

1. **Threshold tuning em validação cruzada**
   - Testar limiares de 0,10 a 0,90 (passo 0,01/0,02).
   - Selecionar limiar por critério: recall mínimo + melhor F1/precisão possível.

2. **CV estratificada com repetição**
   - Ex.: RepeatedStratifiedKFold (5x3) para estimar média e desvio das métricas.

3. **Tuning de hiperparâmetros**
   - Espaço inicial:
     - Learning rate, max_depth, min_child_weight, subsample, colsample, reg_alpha/reg_lambda.
   - Rodar budget fixo (ex.: 100–300 trials por algoritmo).

4. **Comparativo de algoritmos tabulares**
   - Baseline atual vs XGBoost vs LightGBM vs CatBoost sob o mesmo protocolo de CV.

5. **Engenharia de atributos incremental**
   - Inserir blocos de features e medir ganho marginal por bloco (ablação).

6. **Calibração**
   - Comparar sem calibração vs Platt vs Isotonic.
   - Avaliar Brier Score + impacto em threshold tuning.

7. **Ensemble**
   - Testar soft voting com top-3 modelos e, se necessário, stacking com meta-modelo simples.

---

## 4) Novas arquiteturas/algoritmos possíveis e quando usar

- **Regressão Logística (regularizada)**
  - Quando precisa de baseline interpretável, rápido e estável.
- **Random Forest / ExtraTrees**
  - Quando há não linearidade moderada e necessidade de robustez com baixo tuning.
- **XGBoost / LightGBM / CatBoost**
  - Primeira escolha para tabular com relações não lineares e alto potencial de ganho.
  - **CatBoost** é forte com variáveis categóricas e menor esforço de pré-processamento.
- **SVM (kernel)**
  - Pode funcionar em datasets menores e fronteiras complexas; escalar com cuidado.
- **MLP (rede densa para tabular)**
  - Considerar apenas após exaurir boosting; geralmente exige mais tuning e dados.
- **Anomaly-aware / Cost-sensitive learning**
  - Quando custo de falso negativo é muito maior que falso positivo.

---

## 5) Plano de execução por prioridade (P0/P1/P2)

## P0 — 1 a 2 semanas (ganhos imediatos)

- Implementar **Stratified CV** + **threshold tuning**.
- Fazer tuning do modelo atual.
- Definir métrica principal (ex.: recall macro) e secundárias (F1 macro, precisão, PR-AUC).

**Meta de sucesso (P0):**
- Accuracy: **0,70+**
- Recall médio por classe: **0,72+**
- Desvio padrão de recall em CV controlado (estabilidade).

## P1 — 2 a 4 semanas (salto de performance)

- Rodar benchmark com **XGBoost/LightGBM/CatBoost**.
- Adicionar engenharia de atributos incremental.
- Testar calibração + reotimização de limiar.

**Meta de sucesso (P1):**
- Accuracy: **0,73–0,76**
- Recall médio por classe: **0,75+**
- Melhora consistente em 2+ rodadas de CV repetida.

## P2 — 1 a 2 meses (robustez e produção)

- Montar ensemble final (voting/stacking).
- Implantar monitoramento de drift e rotina de re-treino.
- Validar performance por subgrupos críticos.

**Meta de sucesso (P2):**
- Performance estável em produção (queda < 3 p.p. vs validação offline).
- Alertas e ciclos de atualização operacionais.

---

## 6) Checklist de monitoramento em produção

- [ ] **Monitorar qualidade de dados**: nulos, faixas inválidas, mudanças de distribuição.
- [ ] **Drift de features**: PSI/KS por variável e score global.
- [ ] **Drift de predição**: distribuição de probabilidades e taxa de positivos previstos.
- [ ] **Métricas online por janela**: accuracy, recall por classe, precisão, F1, PR-AUC.
- [ ] **Monitoramento por subgrupos** (fairness/performance): região, perfil, faixa de valor etc.
- [ ] **Falsos negativos críticos**: análise semanal/mensal com plano corretivo.
- [ ] **Calibração em produção**: checar se probabilidades continuam confiáveis.
- [ ] **Gatilhos de re-treino**: queda de recall/PR-AUC, drift acima do limite.
- [ ] **Backtesting pós re-treino**: comparar modelo novo vs vigente antes de promover.
- [ ] **Versionamento completo**: dados, features, código, parâmetros, limiar e artefatos.

---

## 7) Resumo executivo

Para sair de ~0,68 de accuracy/recall, o caminho mais eficiente é:
1. **avaliar melhor** (CV estratificada),
2. **decidir melhor** (threshold tuning),
3. **modelar melhor** (boosting + tuning),
4. **operar melhor** (calibração, ensemble e monitoramento).

Esse fluxo tende a gerar ganhos rápidos sem aumentar muito complexidade no início e prepara o modelo para evolução contínua em produção.
