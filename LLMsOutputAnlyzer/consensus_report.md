# Relatório de Análise de Consenso de Classificação de Tabelas
    
**Data de Execução:** 2025-11-06 15:15:03  
**LLMs Analisadas:** DEEPSEEK, MISTRAL, OPENAI  
**Total de Tabelas Consolidadas:** 10
    
---
    
## 1. Resumo das Métricas de Consenso
    
| Métrica | Valor | Unidade |
|---------|-------|---------|
| **Score Médio Geral** | 16.77 | Pontos |
| **Desvio Padrão Geral do Score Médio** | 11.92 | Pontos |
| **Concordância Total de Categoria** | 70.0% | Percentual |
| **Concordância de Score (Range <= 10)** | 70.0% | Percentual |
| **Tabelas de Alto Consenso (STD <= 5)** | 7 | Contagem |
| **Tabelas de Baixo Consenso (STD > 15)** | 2 | Contagem |
    
---
    
## 2. Tabelas de Maior Discordância (Top 10)
    
Esta seção lista as 10 tabelas onde as LLMs discordaram mais significativamente (maior Desvio Padrão do Score).
    
| Tabela | Schema | Média Score | Desvio Padrão | Categoria Consenso | Score DEEPSEEK | Score MISTRAL | Score OPENAI |
|--------|--------|-------------|---------------|--------------------|--- | --- | ---|
| `ta_evolucao_subjetivo` | public | 45.0 | 17.32 | Discordância | 35 | 35 | 65 |
| `tb_acomp_cidadaos_vinculados` | public | 26.67 | 16.07 | Discordância | 15 | 20 | 45 |
| `ta_ad_cidadao` | public | 16.67 | 7.64 | Discordância | 15 | 10 | 25 |
| `tb_acomp_cidadaos_vinc_prcs` | public | 10.0 | 5.0 | Muito Baixa | 5 | 10 | 15 |
| `TB_MIGRACAO_DADOS` | public | 8.33 | 2.89 | Muito Baixa | 5 | 10 | 10 |
| `tb_dim_imunobiologico` | public | 11.67 | 2.89 | Muito Baixa | 15 | 10 | 10 |
| `tb_dim_dose_imunobiologico` | public | 8.33 | 2.89 | Muito Baixa | 5 | 10 | 10 |
| `tb_alim_bebida` | public | 23.33 | 2.89 | Baixa | 25 | 20 | 25 |
| `tb_auditoria_evento` | public | 8.33 | 2.89 | Muito Baixa | 5 | 10 | 10 |
| `tb_beneficio` | public | 9.33 | 1.15 | Muito Baixa | 8 | 10 | 10 |

    
---
    
## 3. Detalhamento de Justificativas (Top 3 de Maior Discordância)
    
Para as 3 tabelas com maior discordância, as justificativas de cada LLM são listadas abaixo para análise manual.
    
### Tabela: `ta_evolucao_subjetivo`

**DEEPSEEK (Score: 35):**
> Score 35 devido à presença limitada de dados sobre hipertensão arterial no campo ds_subjetivo, que representa apenas uma pequena fração dos registros. A tabela contém principalmente identificadores e metadados de auditoria irrelevantes, com alta taxa de nulos (25%) no único campo semanticamente relevante. A conexão direta com doenças cardiovasculares é fraca e esparsa.

**MISTRAL (Score: 35):**
> Score 35 devido à presença de termos relacionados a hipertensão arterial na coluna 'ds_subjetivo'. A tabela possui dados relevantes, mas a maioria das informações é irrelevante para o estudo de doenças cardiovasculares. A coluna 'ds_subjetivo' contém termos como 'HIPERTENSÃO ARTERIAL', que são relevantes, mas a tabela como um todo não é específica o suficiente para o problema do usuário.

**OPENAI (Score: 65):**
> Score 65 devido à presença de informações sobre hipertensão arterial e acompanhamento de saúde. A tabela possui alta completude, mas a falta de dados diretos sobre obesidade e diabetes limita sua relevância.


---

### Tabela: `tb_acomp_cidadaos_vinculados`

**DEEPSEEK (Score: 15):**
> Score baixo devido à ausência completa de dados clínicos sobre doenças cardiovasculares, fatores de risco ou indicadores de saúde relevantes. A tabela contém apenas dados demográficos básicos e informações administrativas, sem conexão direta com detecção de doenças cardíacas. Apesar da boa completude geral, os dados são semanticamente irrelevantes para o objetivo do usuário.

**MISTRAL (Score: 20):**
> Score 20 devido a falta de informações específicas sobre doenças cardiovasculares. A tabela possui dados demográficos básicos como idade, sexo e raça, que são relevantes, mas não suficientes para detectar doenças cardíacas. A tabela não contém informações sobre pressão arterial, colesterol, obesidade ou outros fatores de risco cardiovascular.

**OPENAI (Score: 45):**
> Score 45 devido à presença de dados demográficos relevantes, mas falta de informações diretas sobre fatores de risco cardiovascular. A tabela possui alta completude, mas muitos campos são irrelevantes para a detecção de doenças cardíacas.


---

### Tabela: `ta_ad_cidadao`

**DEEPSEEK (Score: 15):**
> Score baixo devido à ausência de dados específicos sobre doenças cardiovasculares, fatores de risco ou indicadores de saúde relevantes. A tabela contém principalmente campos administrativos e identificadores, com apenas um código CID-10 genérico (9207) que não está diretamente relacionado aos termos-chave do usuário. A maioria das colunas são irrelevantes para detecção de doenças cardíacas.

**MISTRAL (Score: 10):**
> Score baixo devido à falta de conexão direta com doenças cardiovasculares. A tabela contém códigos CID-10 sem descrições claras, não atendendo aos critérios de relevância semântica. A qualidade dos dados é limitada pela ausência de informações específicas sobre fatores de risco cardiovascular.

**OPENAI (Score: 25):**
> Score 25 devido à presença de um código CID principal que pode estar relacionado a doenças cardiovasculares, mas falta informação sobre fatores de risco como pressão arterial e obesidade. A tabela tem baixa completude e relevância semântica para o problema do usuário.


---


---

## 4. Visualização Gráfica

### 4.1. Distribuição de Scores de Relevância por LLM

![Distribuição de Scores](consensus_charts\score_distribution.png)

### 4.2. Distribuição do Desvio Padrão (STD) dos Scores

![Distribuição do Desvio Padrão](consensus_charts\std_distribution.png)

*Relatório gerado automaticamente pelo script de análise de consenso.*
