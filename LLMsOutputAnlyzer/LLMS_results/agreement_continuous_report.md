# Relatório de Acordo entre LLMs (Métricas Contínuas)

**Data de Execução:** 2025-11-06 21:35:42  
**LLMs Analisadas:** DEEPSEEK, MISTRAL, OPENAI  
**Total de Tabelas Consolidadas:** 885

---

## 1. Resumo das Métricas Globais

| Métrica | Valor | Interpretação |
|--------|-------|---------------|
| **Score Médio Geral** | 16.9 | — |
| **STD Geral do Score Médio** | 14.39 | — |
| **ICC(2,1)** | 0.7229 | Moderado |
| **ICC(2,k)** | 0.8867 | Bom |
| **ICC(3,1)** | 0.7859 | Bom |
| **ICC(3,k)** | 0.9167 | Excelente |
| **Spearman médio (pares)** | 0.7172 | — |
| **CCC médio (pares)** | 0.7299 | Pobre |
| **Kendall's W (global)** | 0.7105 | — |

> **Notas de escala**: ICC (Koo & Li, 2016) — <0,50 fraco; 0,50–0,75 moderado; 0,75–0,90 bom; >0,90 excelente.  
> CCC (McBride, 2005) — <0,90 pobre; 0,90–0,95 moderado; 0,95–0,99 substancial; >0,99 quase perfeito.

---

## 2. Tabelas de Maior Dispersão (Top 10 por STD)

| Tabela | Schema | Média Score | Desvio Padrão | Score DEEPSEEK | Score MISTRAL | Score OPENAI |
|--------|--------|-------------|---------------|--- | --- | ---|
| `ta_problema` | public | 26.67 | 34.03 | 15 | 0 | 65.0 |
| `tb_fat_avaliacao_elegibilidade` | public | 36.67 | 33.29 | 15 | 20 | 75.0 |
| `tb_fat_cuidado_compartilhado` | public | 36.67 | 33.29 | 15 | 20 | 75.0 |
| `tb_fat_atd_ind_procedimentos` | public | 40.0 | 30.41 | 25 | 20 | 75.0 |
| `tb_fat_atd_ind_problemas` | public | 63.33 | 29.3 | 85 | 30 | 75.0 |
| `tb_fat_atend_dom_prob_cond` | public | 60.0 | 27.84 | 85 | 30 | 65.0 |
| `tb_atend` | public | 33.33 | 27.54 | 15 | 20 | 65.0 |
| `tb_neuro_fator_risco_evolucao` | public | 43.33 | 27.54 | 25 | 30 | 75.0 |
| `tb_fat_atd_ind_encaminhamentos` | public | 33.33 | 27.54 | 15 | 20 | 65.0 |
| `tb_fat_ivcf` | public | 33.33 | 27.54 | 15 | 20 | 65.0 |


---

## 3. Detalhamento de Justificativas (Top 3 de Maior STD)
### Tabela: `ta_problema`

**DEEPSEEK (Score: 15):**
> Score baixo devido à ausência de dados semânticos diretos sobre doenças cardiovasculares. A tabela contém principalmente identificadores e códigos (CID10/CIAP) sem contexto específico sobre fatores de risco cardiovasculares. Embora códigos CID10 possam conter informações sobre doenças, não há garantia de especificidade cardiovascular. A tabela é muito genérica para detecção direta de doenças cardíacas.

**MISTRAL (Score: 0):**
> Erro ao processar: Error code: 429 - {'object': 'error', 'message': 'Service tier capacity exceeded for this model.', 'type': 'service_tier_capacity_exceeded', 'param': None, 'code': '3505'}

**OPENAI (Score: 65.0):**
> Score 65 devido à presença de códigos CIAP e CID10, que podem estar relacionados a doenças cardiovasculares. A tabela possui uma boa quantidade de registros, mas a alta taxa de nulos em algumas colunas limita sua completude.


---

### Tabela: `tb_fat_avaliacao_elegibilidade`

**DEEPSEEK (Score: 15):**
> Score baixo devido à ausência de dados específicos sobre doenças cardiovasculares, fatores de risco diretos ou indicadores clínicos relevantes. A tabela foca em elegibilidade para cuidados domiciliares com dados administrativos predominantes. As colunas de CID oferecem potencial indireto limitado para identificação de condições cardíacas.

**MISTRAL (Score: 20):**
> Score 20 devido à falta de colunas diretamente relacionadas a fatores de risco cardiovasculares como pressão arterial, obesidade, diabetes, colesterol e hipertensão. A tabela possui informações sobre condições de saúde, mas não as específicas solicitadas.

**OPENAI (Score: 75.0):**
> Score 75 devido à presença de colunas que indicam condições de saúde e demografia relevantes para doenças cardiovasculares. A tabela possui alta completude e dados populacionais.


---

### Tabela: `tb_fat_cuidado_compartilhado`

**DEEPSEEK (Score: 15):**
> Score baixo devido à ausência de dados específicos sobre doenças cardiovasculares, fatores de risco ou indicadores clínicos relevantes. A tabela foca em metadados administrativos de cuidado compartilhado sem conexão direta com detecção de doenças cardíacas. Possui apenas dados demográficos básicos (faixa etária e sexo) que são insuficientes para análise cardiovascular.

**MISTRAL (Score: 20):**
> Score 20 devido a baixa conexão direta com doenças cardiovasculares. A tabela possui informações sobre evolução de cuidados, mas não contém dados específicos sobre pressão arterial, HDL, obesidade, sono, insônia, nutrição, colesterol ou hipertensão, que são essenciais para a detecção de doenças cardíacas. As colunas contribuintes estão relacionadas a diagnósticos e informações demográficas, mas não são suficientes para uma análise cardiovascular precisa.

**OPENAI (Score: 75.0):**
> Score 75 devido à presença de colunas relacionadas a faixa etária e condições de saúde, que são relevantes para a detecção de doenças cardiovasculares. A tabela possui alta completude e dados de evolução clínica.


---


---

## 4. Visualizações

### 4.1. Distribuição de Scores por LLM
![Distribuição de Scores](agreement_charts\score_distribution.png)

### 4.2. Distribuição do Desvio Padrão (STD) entre LLMs por Tabela
![Distribuição do Desvio Padrão](agreement_charts\std_distribution.png)

### 4.3. Heatmap – Spearman (scores)
![Heatmap Spearman](agreement_charts\heatmap_spearman.png)

### 4.4. Heatmap – Lin's CCC
![Heatmap CCC](agreement_charts\heatmap_ccc.png)

*Relatório gerado automaticamente pelo script de análise de acordo (métricas contínuas).*
