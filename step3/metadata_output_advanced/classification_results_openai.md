# Relatório de Classificação de Tabelas - OpenAI
    
**Data de Execução:** 2025-10-30 19:13:53  
**Modelo:** gpt-4o-mini  
**LLM Provider:** OpenAI  
**Temperatura:** 0.1
    
---
    
## Resumo Geral
    
| Métrica | Valor |
|---------|-------|
| **Total de Tabelas** | 10 |
| **Score Médio** | 45.40 |
| **Score Mínimo** | 10 |
| **Score Máximo** | 83 |
| **Erros de Processamento** | 0 |
    
## Distribuição de Relevância por Score
    
| Categoria | Score Range | Quantidade | Percentual |
|-----------|-------------|------------|------------|
| **Alta Relevância** | 80-100 | 3 | 30.0% |
| **Média Relevância** | 50-79 | 0 | 0.0% |
| **Baixa Relevância** | 20-49 | 5 | 50.0% |
| **Muito Baixa Relevância** | 0-19 | 2 | 20.0% |
    
---
    
## Tabelas de Alta Relevância (Score ≥ 80)
    
Total: **3** tabelas
    
| # | Tabela | Row Count | Score | Justificativa |
|---|--------|-----------|-------|---------------|
| 1 | `tb_acomp_cidadaos_vinculados` | 15,724 | 83 | Score 83 devido à presença de registros de cidadãos com diagnósticos de doenças cardiovasculares. A ... |
| 2 | `ta_evolucao_subjetivo` | 198,642 | 83 | Score 83 devido à presença de registros de hipertensão arterial e outros sintomas cardiovasculares. ... |
| 3 | `tb_acomp_cidadaos_vinc_prcs` | 867 | 83 | Score 83 devido à presença de registros processados e datas de início e fim, que são relevantes para... |

    
---
    
## Tabelas de Média Relevância (Score 50-79)
    
Total: **0** tabelas
    
| # | Tabela | Row Count | Score | Justificativa |
|---|--------|-----------|-------|---------------|
| - | Nenhuma tabela encontrada | - | - | - |

    
---
    
## Detalhamento das Tabelas de Alta Relevância
    
### 1. tb_acomp_cidadaos_vinculados
    
- **Schema:** public
- **Row Count:** 15,724
- **Score de Relevância:** 83
- **Chave Primária:** co_seq_acomp_cidadaos_vinc
    
**Justificativa:**
Score 83 devido à presença de registros de cidadãos com diagnósticos de doenças cardiovasculares. A tabela possui alta completude e adequação, com 0% de nulos em colunas chave.
    
**Colunas Contribuintes para o Score:**
- `st_possui_fci`
- `dt_nascimento_cidadao`
- `no_cidadao`

---

### 2. ta_evolucao_subjetivo
    
- **Schema:** public
- **Row Count:** 198,642
- **Score de Relevância:** 83
- **Chave Primária:** co_seq_taevolucaosubjetivo
    
**Justificativa:**
Score 83 devido à presença de registros de hipertensão arterial e outros sintomas cardiovasculares. A tabela possui alta completude e adequação, com 0% de dados nulos.
    
**Colunas Contribuintes para o Score:**
- `ds_subjetivo`
- `co_tipo_auditoria`

---

### 3. tb_acomp_cidadaos_vinc_prcs
    
- **Schema:** public
- **Row Count:** 867
- **Score de Relevância:** 83
- **Chave Primária:** co_seq_acomp_cidad_vinc_prcs
    
**Justificativa:**
Score 83 devido à presença de registros processados e datas de início e fim, que são relevantes para o acompanhamento de doenças cardiovasculares. A tabela possui alta completude e adequação, com 867 registros sem dados nulos.
    
**Colunas Contribuintes para o Score:**
- `dt_inicio`
- `dt_fim`

---


    
---
    
## Metadados da Execução
    
```json
{
  "execution_date": "2025-10-30 19:13:53",
  "llm_provider": "OpenAI",
  "model": "gpt-4o-mini",
  "temperature": 0.1,
  "prompt_file": "prompt_final_universal.txt",
  "input_file": "metadata_advanced_consolidated_filtered.json",
  "total_tables_processed": 10,
  "limit": 10
}
```
    
---
    
*Relatório gerado automaticamente pelo script de classificação de tabelas com OpenAI.*
