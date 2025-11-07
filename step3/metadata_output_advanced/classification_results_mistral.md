# Relatório de Classificação de Tabelas - Mistral

**Data de Execução:** 2025-11-06 17:22:17  
**Modelo:** mistral-small  
**LLM Provider:** Mistral  
**Temperatura:** 0.1

---

## Resumo Geral

| Métrica | Valor |
|---------|-------|
| **Total de Tabelas** | 885 |
| **Score Médio** | 15.23 |
| **Score Mínimo** | 0 |
| **Score Máximo** | 85 |
| **Erros de Processamento** | 0 |

## Distribuição de Relevância por Score

| Categoria | Score Range | Quantidade | Percentual |
|-----------|-------------|------------|------------|
| **Alta Relevância** | 80-100 | 11 | 1.2% |
| **Média Relevância** | 50-79 | 26 | 2.9% |
| **Baixa Relevância** | 20-49 | 249 | 28.1% |
| **Muito Baixa Relevância** | 0-19 | 599 | 67.7% |

---

## Tabelas de Alta Relevância (Score ≥ 80)

Total: **11** tabelas

| # | Tabela | Row Count | Score | Justificativa |
|---|--------|-----------|-------|---------------|
| 1 | `tb_fat_consolidado_cidadao_fci` | 21,303 | 85 | Score 85 devido à presença de colunas diretamente relacionadas a doenças cardiovasculares e fatores ... |
| 2 | `ta_exame_colesterol_hdl` | 1,382 | 85 | Score 85 devido à alta relevância semântica com o tema de doenças cardiovasculares, especialmente pe... |
| 3 | `ta_exame_colesterol_total` | 2,530 | 85 | Score alto devido à presença de dados de colesterol total, um fator de risco cardiovascular relevant... |
| 4 | `ta_medicao` | 105,546 | 85 | Score 85 devido a presença de colunas diretamente relacionadas a fatores de risco cardiovascular com... |
| 5 | `tb_exame_colesterol_hdl` | 1,886 | 85 | Score 85 devido à alta relevância semântica, pois contém dados diretos sobre colesterol HDL, um fato... |
| 6 | `tb_fat_cad_individual` | 235,405 | 85 | Score 85 devido a presença de colunas diretamente relacionadas a doenças cardiovasculares, como hipe... |
| 7 | `tb_fat_rel_op_risco_cardio` | 27,691 | 85 | Score 85 devido à forte conexão com fatores de risco cardiovascular como hipertensão, diabetes e obe... |
| 8 | `tb_fat_visita_domiciliar` | 975,591 | 85 | Score 85 devido à presença de colunas diretamente relacionadas a fatores de risco cardiovascular com... |
| 9 | `tb_medicao` | 149,389 | 85 | Score 85 devido à presença de colunas diretamente relacionadas à saúde cardiovascular, como pressão ... |
| 10 | `tl_exame_colesterol_hdl` | 489 | 85 | Score 85 devido à presença da coluna 'vl_colesterol_hdl', que é diretamente relevante para a detecçã... |
| 11 | `tl_exame_colesterol_ldl` | 465 | 85 | Score 85 devido à alta relevância semântica, pois contém dados diretos sobre colesterol LDL, um fato... |


---

## Tabelas de Média Relevância (Score 50-79)

Total: **26** tabelas

| # | Tabela | Row Count | Score | Justificativa |
|---|--------|-----------|-------|---------------|
| 1 | `tb_fat_consolidado_cidadao_fai` | 21,372 | 75 | Score 75 devido à presença de colunas diretamente relacionadas a fatores de risco cardiovascular com... |
| 2 | `tl_cds_visita_domiciliar` | 1,031,898 | 75 | Score 75 devido à presença de colunas diretamente relacionadas a fatores de risco cardiovascular, co... |
| 3 | `ta_cuidado_compartilhado_evol` | 64 | 75 | Score 75 devido à presença de informações relevantes sobre hipertensão, diabetes e condutas de cuida... |
| 4 | `ta_exame_colesterol_ldl` | 1,358 | 75 | Score 75 devido à presença de dados de colesterol LDL, que é um fator de risco para doenças cardiova... |
| 5 | `ta_exame_hemoglobina_glicada` | 1,771 | 75 | Score 75 devido à presença de dados sobre hemoglobina glicada, diretamente relacionados ao diabetes,... |
| 6 | `tb_cds_visita_domiciliar` | 978,865 | 75 | Score 75 devido à presença de colunas diretamente relacionadas a fatores de risco cardiovascular, co... |
| 7 | `tb_exame_colesterol_ldl` | 1,840 | 75 | Score 75 devido à presença de dados de colesterol LDL, um fator de risco cardiovascular relevante. A... |
| 8 | `tb_exame_colesterol_total` | 3,660 | 75 | Score 75 devido à presença de dados de colesterol total, um fator de risco cardiovascular relevante.... |
| 9 | `tb_exame_hemoglobina_glicada` | 2,450 | 75 | Score 75 devido à forte conexão com diabetes, um fator de risco significativo para doenças cardiovas... |
| 10 | `tb_fat_proced_atend` | 390,311 | 75 | Score 75 devido à presença de colunas diretamente relacionadas a fatores de risco cardiovascular, co... |
| 11 | `tb_historico_dados_fai` | 255,644 | 75 | Score 75 devido à presença de informações relevantes sobre hipertensão e diabetes, que são fatores d... |
| 12 | `tb_historico_dados_proced` | 362,012 | 75 | Score 75 devido à presença de informações relevantes como aferição de pressão arterial e avaliação a... |
| 13 | `tl_exame_colesterol_total` | 1,100 | 75 | Score 75 devido à presença de dados de colesterol total, um fator de risco cardiovascular relevante.... |
| 14 | `tl_medicao` | 104,237 | 75 | Score 75 devido à presença de colunas diretamente relacionadas a fatores de risco cardiovascular com... |
| 15 | `tb_dim_grupo_atendimento` | 34 | 70 | Score 70 devido à presença de termos diretamente relacionados a doenças cardiovasculares e grupos de... |
| 16 | `tl_exame_hemoglobina_glicada` | 652 | 70 | Score 70 devido a relevância semântica moderada. A tabela possui dados sobre hemoglobina glicada, qu... |
| 17 | `tb_cds_ficha_proced` | 4,962 | 65 | Score 65 devido à presença de colunas relevantes como pressão arterial, glicemia e peso, que são ind... |
| 18 | `ta_encaminhamento` | 6,930 | 65 | Score 65 devido à presença de informações relevantes sobre fatores de risco cardiovascular como hipe... |
| 19 | `ta_evolucao_objetivo` | 183,071 | 65 | Score 65 devido à presença de informações relevantes sobre pressão arterial e outros fatores de risc... |
| 20 | `tb_encaminhamento` | 8,137 | 65 | Score 65 devido à presença de informações relevantes sobre fatores de risco cardiovascular como hipe... |
| 21 | `tb_evolucao_avaliacao` | 223,896 | 65 | Score 65 devido à presença de informações relevantes sobre pressão arterial e acompanhamento de cond... |
| 22 | `tb_evolucao_objetivo` | 287,175 | 65 | Score 65 devido à presença de informações relevantes como pressão arterial e colesterol na coluna ds... |
| 23 | `tl_cds_ficha_proced` | 13,702 | 65 | Score 65 devido à presença de colunas relacionadas à pressão arterial e medições de saúde, que são r... |
| 24 | `tl_evolucao_objetivo` | 104,237 | 65 | Score 65 devido à presença de informações relevantes sobre saúde cardiovascular, como pressão arteri... |
| 25 | `ta_cuidado_compartilhado` | 49 | 60 | Score 60 devido à presença de informações relevantes sobre hipertensão e diabetes na coluna ds_discu... |
| 26 | `tb_historico_dados_fae` | 121 | 60 | Score 60 devido à presença de informações relevantes sobre doenças cardiovasculares e fatores de ris... |


---

## Detalhamento das Tabelas de Alta Relevância

### 1. tb_fat_consolidado_cidadao_fci

- **Schema:** public
- **Row Count:** 21,303
- **Score de Relevância:** 85
- **Chave Primária:** co_seq_fat_conslddo_ciddo_fci

**Justificativa:**
Score 85 devido à presença de colunas diretamente relacionadas a doenças cardiovasculares e fatores de risco como diabetes, infarto, AVC e problemas cardíacos. A tabela possui dados populacionais e informações sobre a saúde dos cidadãos, o que é altamente relevante para a detecção de doenças cardiovasculares. As colunas contribuintes são aquelas que indicam a presença ou ausência de condições de saúde críticas.

**Colunas Contribuintes para o Score:**
- `co_dim_tempo_diabete_sim`
- `co_dim_tempo_diabete_nao`
- `co_dim_tempo_avc_sim`
- `co_dim_tempo_infarto_sim`
- `co_dim_tempo_donca_crdaca_sim`
- `co_dim_tempo_problema_rins_sim`
- `co_dim_tempo_avc_nao`
- `co_dim_tempo_infarto_nao`
- `co_dim_tempo_donca_crdaca_nao`
- `co_dim_tempo_problema_rins_nao`

---

### 2. ta_exame_colesterol_hdl

- **Schema:** public
- **Row Count:** 1,382
- **Score de Relevância:** 85
- **Chave Primária:** co_seq_taexamecolesterolhdl

**Justificativa:**
Score 85 devido à alta relevância semântica com o tema de doenças cardiovasculares, especialmente pela coluna 'vl_colesterol_hdl' que está diretamente relacionada ao colesterol HDL, um fator de risco cardiovascular. A tabela também possui alta completude nos campos relevantes e dados numéricos adequados para análise.

**Colunas Contribuintes para o Score:**
- `vl_colesterol_hdl`
- `co_exame_requisitado`

---

### 3. ta_exame_colesterol_total

- **Schema:** public
- **Row Count:** 2,530
- **Score de Relevância:** 85
- **Chave Primária:** co_seq_taexamecolesteroltotal

**Justificativa:**
Score alto devido à presença de dados de colesterol total, um fator de risco cardiovascular relevante. A tabela possui alta completude nos campos relevantes e dados específicos sobre um indicador importante para a detecção de doenças cardiovasculares.

**Colunas Contribuintes para o Score:**
- `vl_colesterol_total`

---

### 4. ta_medicao

- **Schema:** public
- **Row Count:** 105,546
- **Score de Relevância:** 85
- **Chave Primária:** co_seq_tamedicao

**Justificativa:**
Score 85 devido a presença de colunas diretamente relacionadas a fatores de risco cardiovascular como pressão arterial, frequência cardíaca, peso e IMC. A tabela possui alta completude nos campos relevantes e dados específicos para análise de saúde cardiovascular.

**Colunas Contribuintes para o Score:**
- `nu_medicao_pressao_arterial`
- `nu_medicao_frequencia_cardiaca`
- `nu_medicao_peso`
- `nu_medicao_imc`

---

### 5. tb_exame_colesterol_hdl

- **Schema:** public
- **Row Count:** 1,886
- **Score de Relevância:** 85
- **Chave Primária:** co_seq_exame_colesterol_hdl

**Justificativa:**
Score 85 devido à alta relevância semântica, pois contém dados diretos sobre colesterol HDL, um fator de risco cardiovascular. A tabela possui alta completude nos campos relevantes e dados numéricos adequados para análise.

**Colunas Contribuintes para o Score:**
- `vl_colesterol_hdl`

---

### 6. tb_fat_cad_individual

- **Schema:** public
- **Row Count:** 235,405
- **Score de Relevância:** 85
- **Chave Primária:** co_seq_fat_cad_individual

**Justificativa:**
Score 85 devido a presença de colunas diretamente relacionadas a doenças cardiovasculares, como hipertensão arterial, diabetes, problemas cardíacos e renais. A tabela possui alta completude e dados relevantes para a detecção de doenças cardiovasculares, com colunas específicas que indicam condições de saúde críticas.

**Colunas Contribuintes para o Score:**
- `st_hipertensao_arterial`
- `st_diabete`
- `st_doenca_cardiaca`
- `st_doenca_card_insuficiencia`
- `st_doenca_card_outro`
- `st_doenca_card_n_sabe`
- `st_problema_rins`
- `st_problema_rins_insuficiencia`
- `st_problema_rins_outro`
- `st_problema_rins_nao_sabe`

---

### 7. tb_fat_rel_op_risco_cardio

- **Schema:** public
- **Row Count:** 27,691
- **Score de Relevância:** 85
- **Chave Primária:** co_seq_fat_rel_op_risco_cardio

**Justificativa:**
Score 85 devido à forte conexão com fatores de risco cardiovascular como hipertensão, diabetes e obesidade. A tabela possui dados relevantes para a detecção de doenças cardíacas, com colunas específicas que contribuem significativamente para a análise. A completude contextual é adequada para os campos semanticamente relevantes.

**Colunas Contribuintes para o Score:**
- `dt_hipertensao_arterial_fai`
- `dt_hiprtnsao_arterial_fci_sim`
- `dt_hiprtnsao_arterial_fci_nao`
- `dt_diabetes_fai`
- `dt_diabetes_fci_sim`
- `dt_diabetes_fci_nao`
- `dt_obesidade_fai`
- `nu_imc`
- `st_risco_cardio`

---

### 8. tb_fat_visita_domiciliar

- **Schema:** public
- **Row Count:** 975,591
- **Score de Relevância:** 85
- **Chave Primária:** co_seq_fat_visita_domiciliar

**Justificativa:**
Score 85 devido à presença de colunas diretamente relacionadas a fatores de risco cardiovascular como hipertensão e diabetes. A tabela possui dados demográficos e de saúde relevantes, como pressão arterial, peso, altura e idade, que são essenciais para a detecção de doenças cardíacas. A alta completude contextual e a adequação prática dos dados também contribuem para a relevância.

**Colunas Contribuintes para o Score:**
- `st_acomp_pessoa_hipertensao`
- `st_acomp_pessoa_diabetes`
- `nu_medicao_pressao_arterial`
- `dt_nascimento`
- `nu_peso`
- `nu_altura`

---

### 9. tb_medicao

- **Schema:** public
- **Row Count:** 149,389
- **Score de Relevância:** 85
- **Chave Primária:** co_seq_medicao

**Justificativa:**
Score 85 devido à presença de colunas diretamente relacionadas à saúde cardiovascular, como pressão arterial, frequência cardíaca e IMC. A tabela possui alta completude nos campos relevantes e dados específicos para análise de doenças cardíacas.

**Colunas Contribuintes para o Score:**
- `nu_medicao_pressao_arterial`
- `nu_medicao_frequencia_cardiaca`
- `nu_medicao_imc`

---

### 10. tl_exame_colesterol_hdl

- **Schema:** public
- **Row Count:** 489
- **Score de Relevância:** 85
- **Chave Primária:** NÃO ENCONTRADA

**Justificativa:**
Score 85 devido à presença da coluna 'vl_colesterol_hdl', que é diretamente relevante para a detecção de doenças cardiovasculares. A tabela possui alta completude nos dados relevantes e não contém identificadores ou códigos irrelevantes. A ausência de outras colunas relacionadas a fatores de risco como hipertensão e obesidade limita a relevância, mas a coluna principal compensa significativamente.

**Colunas Contribuintes para o Score:**
- `vl_colesterol_hdl`

---

### 11. tl_exame_colesterol_ldl

- **Schema:** public
- **Row Count:** 465
- **Score de Relevância:** 85
- **Chave Primária:** NÃO ENCONTRADA

**Justificativa:**
Score 85 devido à alta relevância semântica, pois contém dados diretos sobre colesterol LDL, um fator de risco cardiovascular. A tabela possui alta completude nos dados relevantes e é específica para o tema.

**Colunas Contribuintes para o Score:**
- `vl_colesterol_ldl`

---



---

## Metadados da Execução

```json
{
  "execution_date": "2025-11-06 17:22:17",
  "llm_provider": "Mistral",
  "model": "mistral-small",
  "temperature": 0.1,
  "prompt_file": "prompt_final_universal.txt",
  "input_file": "metadata_advanced_consolidated_filtered.json",
  "total_tables_processed": 885,
  "limit": null
}
```

---

*Relatório gerado automaticamente pelo script de classificação de tabelas com Mistral.*
