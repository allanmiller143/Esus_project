# Relatório de Análise de Consenso de Classificação de Tabelas
    
**Data de Execução:** 2025-11-05 14:57:34  
**LLMs Analisadas:** DEEPSEEK, MISTRAL, OPENAI  
**Total de Tabelas Consolidadas:** 10
    
---
    
## 1. Resumo das Métricas de Consenso
    
| Métrica | Valor | Unidade |
|---------|-------|---------|
| **Score Médio Geral** | 36.8 | Pontos |
| **Desvio Padrão Geral do Score Médio** | 21.13 | Pontos |
| **Concordância Total de Categoria** | 50.0% | Percentual |
| **Concordância de Score (Range <= 10)** | 10.0% | Percentual |
| **Tabelas de Alto Consenso (STD <= 5)** | 0 | Contagem |
| **Tabelas de Baixo Consenso (STD > 15)** | 4 | Contagem |
    
---
    
## 2. Tabelas de Maior Discordância (Top 10)
    
Esta seção lista as 10 tabelas onde as LLMs discordaram mais significativamente (maior Desvio Padrão do Score).
    
| Tabela | Schema | Média Score | Desvio Padrão | Categoria Consenso | Score DEEPSEEK | Score MISTRAL | Score OPENAI |
|--------|--------|-------------|---------------|--------------------|--- | --- | ---|
| `tb_acomp_cidadaos_vinculados` | public | 55.0 | 37.8 | Discordância | 12 | 70 | 83 |
| `tb_acomp_cidadaos_vinc_prcs` | public | 48.33 | 35.53 | Discordância | 12 | 50 | 83 |
| `tb_auditoria_evento` | public | 35.67 | 20.65 | Discordância | 12 | 50 | 45 |
| `TB_MIGRACAO_DADOS` | public | 25.67 | 17.21 | Baixa | 12 | 20 | 45 |
| `ta_ad_cidadao` | public | 59.0 | 13.53 | Discordância | 72 | 60 | 45 |
| `tb_beneficio` | public | 16.0 | 12.17 | Baixa | 8 | 30 | 10 |
| `tb_dim_imunobiologico` | public | 22.33 | 9.29 | Baixa | 12 | 30 | 25 |
| `tb_dim_dose_imunobiologico` | public | 17.67 | 8.74 | Baixa | 8 | 20 | 25 |
| `ta_evolucao_subjetivo` | public | 74.33 | 7.77 | Discordância | 72 | 68 | 83 |
| `tb_alim_bebida` | public | 14.0 | 5.29 | Baixa | 12 | 20 | 10 |

    
---
    
## 3. Detalhamento de Justificativas (Top 3 de Maior Discordância)
    
Para as 3 tabelas com maior discordância, as justificativas de cada LLM são listadas abaixo para análise manual.
    
### Tabela: `tb_acomp_cidadaos_vinculados`

**DEEPSEEK (Score: 12):**
> Score baixo devido à ausência completa de variáveis relacionadas a doenças cardiovasculares, pressão arterial ou diagnósticos médicos. A tabela contém apenas dados demográficos básicos e endereços, sem informações clínicas relevantes para identificar condições cardíacas. Alta completude em dados pessoais, mas irrelevante para o objetivo de pesquisa.  
---

**MISTRAL (Score: 70):**
> Score 70 devido à presença de colunas relevantes como nome, data de nascimento, sexo e identificadores únicos. No entanto, a tabela carece de colunas específicas relacionadas às doenças cardiovasculares, o que limita seu potencial para o estudo em questão.  
---

**OPENAI (Score: 83):**
> Score 83 devido à presença de registros de cidadãos com diagnósticos de doenças cardiovasculares. A tabela possui alta completude e adequação, com 0% de nulos em colunas chave.  
---

### Tabela: `tb_acomp_cidadaos_vinc_prcs`

**DEEPSEEK (Score: 12):**
> Score baixo devido à ausência completa de dados clínicos sobre doenças cardiovasculares. A tabela contém apenas metadados de processamento e datas, sem informações sobre diagnósticos, sintomas ou variáveis cardiovasculares. Apesar da boa completude (0% nulos), os dados são irrelevantes para identificar condições cardíacas em registros de pacientes.  
---

**MISTRAL (Score: 50):**
> Score 50 devido à presença da palavra-chave 'PROCESSADO' relacionada ao processamento de registros de pessoas. No entanto, a tabela não possui colunas diretamente ligadas às doenças cardiovasculares ou à pressão arterial, o que impacta negativamente o score.  
---

**OPENAI (Score: 83):**
> Score 83 devido à presença de registros processados e datas de início e fim, que são relevantes para o acompanhamento de doenças cardiovasculares. A tabela possui alta completude e adequação, com 867 registros sem dados nulos.  
---

### Tabela: `tb_auditoria_evento`

**DEEPSEEK (Score: 12):**
> Score baixo devido à ausência de termos específicos de doenças cardiovasculares. A tabela é de auditoria de sistema, não contendo dados clínicos diretos. Apenas a coluna ds_detalhes poderia conter informações textuais relacionadas, mas sem evidências de termos cardíacos nos metadados. Alta completude geral, mas irrelevante para o contexto médico.  
---

**MISTRAL (Score: 50):**
> Score 50 devido à presença da coluna ds_detalhes, que pode conter informações relacionadas a sintomas e classificações textuais de doenças cardiovasculares. No entanto, a tabela não possui colunas diretamente relacionadas ao foco de desfecho ou às variáveis-chave do estudo, o que justifica um score moderado.  
---

**OPENAI (Score: 45):**
> Score 45 devido à falta de variáveis diretamente relacionadas a doenças cardiovasculares. A tabela possui alta completude, mas a adequação é baixa, pois não contém informações relevantes sobre diagnósticos ou sintomas.  
---


---

## 4. Visualização Gráfica

### 4.1. Distribuição de Scores de Relevância por LLM

![Distribuição de Scores](consensus_charts\score_distribution.png)

### 4.2. Distribuição do Desvio Padrão (STD) dos Scores

![Distribuição do Desvio Padrão](consensus_charts\std_distribution.png)

*Relatório gerado automaticamente pelo script de análise de consenso.*
