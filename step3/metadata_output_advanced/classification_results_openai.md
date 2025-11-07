# Relatório de Classificação de Tabelas - OpenAI
    
**Data de Execução:** 2025-11-06 20:58:11  
**Modelo:** gpt-4o-mini  
**LLM Provider:** OpenAI  
**Temperatura:** 0.1
    
---
    
## Resumo Geral
    
| Métrica | Valor |
|---------|-------|
| **Total de Tabelas** | 885 |
| **Score Médio** | 22.10 |
| **Score Mínimo** | 0 | 
| **Score Máximo** | 85 |
| **Erros de Processamento** | 0 |
    
## Distribuição de Relevância por Score
    
| Categoria | Score Range | Quantidade | Percentual |
|-----------|-------------|------------|------------|
| **Alta Relevância** | 80-100 | 11 | 1.2% |
| **Média Relevância** | 50-79 | 37 | 4.2% |
| **Baixa Relevância** | 20-49 | 408 | 46.1% |
| **Muito Baixa Relevância** | 0-19 | 429 | 48.5% |
    
---
    
## Tabelas de Alta Relevância (Score ≥ 80)
    
Total: **11** tabelas
    
| # | Tabela | Row Count | Score | Justificativa |
|---|--------|-----------|-------|---------------|
| 1 | `ta_exame_colesterol_hdl` | 1,382 | 85 | Score 85 devido à presença de dados sobre colesterol HDL, um fator crítico na detecção de doenças ca... |
| 2 | `ta_exame_colesterol_ldl` | 1,358 | 85 | Score 85 devido à presença da coluna 'vl_colesterol_ldl', que é crucial para a detecção de doenças c... |
| 3 | `ta_exame_colesterol_total` | 2,530 | 85 | Score 85 devido à presença da coluna 'vl_colesterol_total', que é crucial para a detecção de doenças... |
| 4 | `tb_exame_colesterol_hdl` | 1,886 | 85 | Score 85 devido à presença de dados sobre colesterol HDL, um fator de risco importante para doenças ... |
| 5 | `tb_exame_colesterol_ldl` | 1,840 | 85 | Score 85 devido à presença de dados sobre colesterol LDL, um fator de risco importante para doenças ... |
| 6 | `tb_exame_colesterol_total` | 3,660 | 85 | Score 85 devido à presença de dados sobre colesterol total, um fator de risco importante para doença... |
| 7 | `tb_fat_cad_individual` | 235,405 | 85 | Score 85 devido à presença de colunas que indicam fatores de risco cardiovascular, como hipertensão ... |
| 8 | `tb_fat_rel_op_risco_cardio` | 27,691 | 85 | Score 85 devido à presença de colunas relevantes como hipertensão, diabetes e obesidade, que são fat... |
| 9 | `tb_fat_visita_domiciliar` | 975,591 | 85 | Score 85 devido à presença de colunas que indicam hipertensão e diabetes, fatores de risco para doen... |
| 10 | `tl_exame_colesterol_ldl` | 465 | 85 | Score 85 devido à presença de dados sobre colesterol LDL, um fator de risco importante para doenças ... |
| 11 | `tl_exame_colesterol_total` | 1,100 | 85 | Score 85 devido à presença do campo 'vl_colesterol_total', que é crucial para a detecção de doenças ... |

    
---
    
## Tabelas de Média Relevância (Score 50-79)
    
Total: **37** tabelas
    
| # | Tabela | Row Count | Score | Justificativa |
|---|--------|-----------|-------|---------------|
| 1 | `tb_fat_consolidado_cidadao_fai` | 21,372 | 75 | Score 75 devido à presença de colunas relevantes como diabetes e obesidade, que são fatores de risco... |
| 2 | `ta_cuidado_compartilhado` | 49 | 75 | Score 75 devido à presença de discussões sobre hipertensão e diabetes, que são relevantes para doenç... |
| 3 | `ta_cuidado_compartilhado_evol` | 64 | 75 | Score 75 devido à presença de informações sobre pacientes hipertensos e diabéticos, que são fatores ... |
| 4 | `ta_exame_triglicerideos` | 2,428 | 75 | Score 75 devido à presença da coluna 'vl_triglicerideos', que é relevante para a detecção de doenças... |
| 5 | `ta_medicao` | 105,546 | 75 | Score 75 devido à presença de colunas relevantes como pressão arterial e peso, que são indicadores d... |
| 6 | `tb_cuidado_compartilhado_evol` | 32 | 75 | Score 75 devido à presença de informações sobre condições como hipertensão e diabetes, que são relev... |
| 7 | `tb_exame_triglicerideos` | 3,547 | 75 | Score 75 devido à presença da coluna 'vl_triglicerideos', que é relevante para a detecção de doenças... |
| 8 | `tb_fat_atd_ind_problemas` | 306,196 | 75 | Score 75 devido à presença de colunas que indicam diagnósticos e condições de saúde relevantes. A ta... |
| 9 | `tb_fat_atd_ind_procedimentos` | 182,586 | 75 | Score 75 devido à presença de colunas relacionadas a faixa etária e sexo, que são relevantes para an... |
| 10 | `tb_fat_atendimento_individual` | 284,566 | 75 | Score 75 devido à presença de colunas relevantes como pressão arterial e dados antropométricos. A ta... |
| 11 | `tb_fat_avaliacao_elegibilidade` | 122 | 75 | Score 75 devido à presença de colunas que indicam condições de saúde e demografia relevantes para do... |
| 12 | `tb_fat_cuidado_compartilhado` | 32 | 75 | Score 75 devido à presença de colunas relacionadas a faixa etária e condições de saúde, que são rele... |
| 13 | `tb_fat_proced_atend` | 390,311 | 75 | Score 75 devido à presença de colunas relevantes como pressão arterial e dados antropométricos. A ta... |
| 14 | `tb_fat_procedimento` | 372,033 | 75 | Score 75 devido à presença de colunas relacionadas à pressão arterial e medições de peso, que são re... |
| 15 | `tb_historico_dados_proced` | 362,012 | 75 | Score 75 devido à presença de procedimentos relacionados à aferição de pressão arterial, que é cruci... |
| 16 | `tb_medicao` | 149,389 | 75 | Score 75 devido à presença de dados relevantes como pressão arterial e peso, que são indicadores crí... |
| 17 | `tb_neuro_fator_risco_evolucao` | 1,017 | 75 | Score 75 devido à presença de fatores de risco e avaliação de condições. A tabela possui alta comple... |
| 18 | `tl_exame_colesterol_hdl` | 489 | 75 | Score 75 devido à presença de dados sobre colesterol HDL, que é um fator relevante na detecção de do... |
| 19 | `tb_historico_dados_fcc` | 32 | 70 | Score 70 devido à presença de condições como hipertensão e obesidade, que são relevantes para doença... |
| 20 | `tl_exame_triglicerideos` | 1,088 | 70 | Score 70 devido à presença da coluna 'vl_triglicerideos', que é relevante para a detecção de doenças... |
| 21 | `ta_evolucao_subjetivo` | 198,642 | 65 | Score 65 devido à presença de informações sobre hipertensão arterial e acompanhamento de saúde. A ta... |
| 22 | `tb_cds_ficha_proced` | 4,962 | 65 | Score 65 devido à presença de aferições de pressão arterial e glicemia, que são relevantes para doen... |
| 23 | `tb_fat_ivcf` | 74 | 65 | Score 65 devido à presença de colunas que indicam resultados de saúde e comorbidades, relevantes par... |
| 24 | `ta_problema` | 32,508 | 65 | Score 65 devido à presença de códigos CIAP e CID10, que podem estar relacionados a doenças cardiovas... |
| 25 | `ta_requisicao_exame` | 19,047 | 65 | Score 65 devido à presença de justificativas relacionadas a hipertensão e diabetes. A tabela possui ... |
| 26 | `tb_antecedente_item` | 15,339 | 65 | Score 65 devido à presença de dados sobre antecedentes que podem incluir fatores de risco como hiper... |
| 27 | `tb_atend` | 276,939 | 65 | Score 65 devido à presença de colunas que indicam status de atendimento e classificação de risco, re... |
| 28 | `tb_cuidado_compartilhado` | 16 | 65 | Score 65 devido à presença de informações sobre condições de saúde como hipertensão e diabetes, que ... |
| 29 | `tb_fat_atd_ind_encaminhamentos` | 5,781 | 65 | Score 65 devido à presença de colunas que indicam classificação de risco e diagnósticos relacionados... |
| 30 | `tb_fat_atend_dom_prob_cond` | 22,454 | 65 | Score 65 devido à presença de colunas relacionadas a diagnósticos e condições de saúde, que são rele... |

*... e mais 7 tabelas de média relevância*

    
---
    
## Detalhamento das Tabelas de Alta Relevância
    
### 1. ta_exame_colesterol_hdl
    
- **Schema:** public
- **Row Count:** 1,382
- **Score de Relevância:** 85
- **Chave Primária:** co_seq_taexamecolesterolhdl
    
**Justificativa:**
Score 85 devido à presença de dados sobre colesterol HDL, um fator crítico na detecção de doenças cardiovasculares. A tabela possui alta completude e dados numéricos relevantes.
    
**Colunas Contribuintes para o Score:**
- `vl_colesterol_hdl`

---

### 2. ta_exame_colesterol_ldl
    
- **Schema:** public
- **Row Count:** 1,358
- **Score de Relevância:** 85
- **Chave Primária:** co_seq_taexamecolesterolldl
    
**Justificativa:**
Score 85 devido à presença da coluna 'vl_colesterol_ldl', que é crucial para a detecção de doenças cardiovasculares. A tabela possui alta completude e dados relevantes para análise.
    
**Colunas Contribuintes para o Score:**
- `vl_colesterol_ldl`

---

### 3. ta_exame_colesterol_total
    
- **Schema:** public
- **Row Count:** 2,530
- **Score de Relevância:** 85
- **Chave Primária:** co_seq_taexamecolesteroltotal
    
**Justificativa:**
Score 85 devido à presença da coluna 'vl_colesterol_total', que é crucial para a detecção de doenças cardiovasculares. A tabela possui alta completude e dados relevantes para análise de risco.
    
**Colunas Contribuintes para o Score:**
- `vl_colesterol_total`

---

### 4. tb_exame_colesterol_hdl
    
- **Schema:** public
- **Row Count:** 1,886
- **Score de Relevância:** 85
- **Chave Primária:** co_seq_exame_colesterol_hdl
    
**Justificativa:**
Score 85 devido à presença de dados sobre colesterol HDL, um fator de risco importante para doenças cardiovasculares. A tabela possui alta completude e dados relevantes para a análise de saúde cardiovascular.
    
**Colunas Contribuintes para o Score:**
- `vl_colesterol_hdl`

---

### 5. tb_exame_colesterol_ldl
    
- **Schema:** public
- **Row Count:** 1,840
- **Score de Relevância:** 85
- **Chave Primária:** co_seq_exame_colesterol_ldl
    
**Justificativa:**
Score 85 devido à presença de dados sobre colesterol LDL, um fator de risco importante para doenças cardiovasculares. A tabela possui alta completude e dados numéricos relevantes.
    
**Colunas Contribuintes para o Score:**
- `vl_colesterol_ldl`

---

### 6. tb_exame_colesterol_total
    
- **Schema:** public
- **Row Count:** 3,660
- **Score de Relevância:** 85
- **Chave Primária:** co_seq_exame_colesterol_total
    
**Justificativa:**
Score 85 devido à presença de dados sobre colesterol total, um fator de risco importante para doenças cardiovasculares. A tabela possui alta completude e dados relevantes para a análise de saúde cardiovascular.
    
**Colunas Contribuintes para o Score:**
- `vl_colesterol_total`

---

### 7. tb_fat_cad_individual
    
- **Schema:** public
- **Row Count:** 235,405
- **Score de Relevância:** 85
- **Chave Primária:** co_seq_fat_cad_individual
    
**Justificativa:**
Score 85 devido à presença de colunas que indicam fatores de risco cardiovascular, como hipertensão e diabetes. A tabela possui alta completude e diversidade de dados relevantes.
    
**Colunas Contribuintes para o Score:**
- `st_hipertensao_arterial`
- `st_diabete`
- `st_doenca_cardiaca`
- `st_fumante`
- `st_alcool`

---

### 8. tb_fat_rel_op_risco_cardio
    
- **Schema:** public
- **Row Count:** 27,691
- **Score de Relevância:** 85
- **Chave Primária:** co_seq_fat_rel_op_risco_cardio
    
**Justificativa:**
Score 85 devido à presença de colunas relevantes como hipertensão, diabetes e obesidade, que são fatores de risco para doenças cardiovasculares. A tabela possui uma boa completude em dados relevantes, apesar de algumas colunas com alta taxa de nulos.
    
**Colunas Contribuintes para o Score:**
- `dt_hipertensao_arterial_fai`
- `dt_diabetes_fai`
- `dt_obesidade_fai`
- `st_risco_cardio`

---

### 9. tb_fat_visita_domiciliar
    
- **Schema:** public
- **Row Count:** 975,591
- **Score de Relevância:** 85
- **Chave Primária:** co_seq_fat_visita_domiciliar
    
**Justificativa:**
Score 85 devido à presença de colunas que indicam hipertensão e diabetes, fatores de risco para doenças cardiovasculares. A tabela possui alta completude e um grande número de registros.
    
**Colunas Contribuintes para o Score:**
- `st_acomp_pessoa_hipertensao`
- `st_acomp_pessoa_diabetes`
- `nu_medicao_pressao_arterial`

---

### 10. tl_exame_colesterol_ldl
    
- **Schema:** public
- **Row Count:** 465
- **Score de Relevância:** 85
- **Chave Primária:** NÃO ENCONTRADA
    
**Justificativa:**
Score 85 devido à presença de dados sobre colesterol LDL, um fator de risco importante para doenças cardiovasculares. A tabela possui alta completude e dados relevantes para a análise de saúde cardiovascular.
    
**Colunas Contribuintes para o Score:**
- `vl_colesterol_ldl`
- `co_exame_requisitado`

---

### 11. tl_exame_colesterol_total
    
- **Schema:** public
- **Row Count:** 1,100
- **Score de Relevância:** 85
- **Chave Primária:** NÃO ENCONTRADA
    
**Justificativa:**
Score 85 devido à presença do campo 'vl_colesterol_total', que é crucial para a detecção de doenças cardiovasculares. A tabela possui alta completude e dados relevantes para a análise de risco cardiovascular.
    
**Colunas Contribuintes para o Score:**
- `vl_colesterol_total`

---


    
---
    
## Metadados da Execução
    
```json
{
  "execution_date": "2025-11-06 20:58:11",
  "llm_provider": "OpenAI",
  "model": "gpt-4o-mini",
  "temperature": 0.1,
  "prompt_file": "prompt_final_universal.txt",
  "input_file": "metadata_advanced_consolidated_filtered.json",
  "total_tables_processed": 885,
  "limit": null
}
```
    
---
    
*Relatório gerado automaticamente pelo script de classificação de tabelas com OpenAI.*
