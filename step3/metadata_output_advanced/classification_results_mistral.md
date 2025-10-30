# Relatório de Classificação de Tabelas - Mistral

**Data de Execução:** 2025-10-30 19:15:12  
**Modelo:** mistral-small  
**LLM Provider:** Mistral  
**Temperatura:** 0.1

---

## Resumo Geral

| Métrica | Valor |
|---------|-------|
| **Total de Tabelas** | 10 |
| **Score Médio** | 41.80 |
| **Score Mínimo** | 20 |
| **Score Máximo** | 70 |
| **Erros de Processamento** | 0 |

## Distribuição de Relevância por Score

| Categoria | Score Range | Quantidade | Percentual |
|-----------|-------------|------------|------------|
| **Alta Relevância** | 80-100 | 0 | 0.0% |
| **Média Relevância** | 50-79 | 5 | 50.0% |
| **Baixa Relevância** | 20-49 | 5 | 50.0% |
| **Muito Baixa Relevância** | 0-19 | 0 | 0.0% |

---

## Tabelas de Alta Relevância (Score ≥ 80)

Total: **0** tabelas

| # | Tabela | Row Count | Score | Justificativa |
|---|--------|-----------|-------|---------------|
| - | Nenhuma tabela encontrada | - | - | - |


---

## Tabelas de Média Relevância (Score 50-79)

Total: **5** tabelas

| # | Tabela | Row Count | Score | Justificativa |
|---|--------|-----------|-------|---------------|
| 1 | `tb_acomp_cidadaos_vinculados` | 15,724 | 70 | Score 70 devido à presença de colunas relevantes como nome, data de nascimento, sexo e identificador... |
| 2 | `ta_evolucao_subjetivo` | 198,642 | 68 | Score 68 devido ao Sub-Critério A (30%) com a coluna 'ds_subjetivo' contendo textos relacionados a c... |
| 3 | `ta_ad_cidadao` | 1 | 60 | Score 60 devido ao Sub-Critério A (30%) com a presença da palavra-chave 'co_cid10_principal' relacio... |
| 4 | `tb_acomp_cidadaos_vinc_prcs` | 867 | 50 | Score 50 devido à presença da palavra-chave 'PROCESSADO' relacionada ao processamento de registros d... |
| 5 | `tb_auditoria_evento` | 3,125,068 | 50 | Score 50 devido à presença da coluna ds_detalhes, que pode conter informações relacionadas a sintoma... |


---

## Detalhamento das Tabelas de Alta Relevância



---

## Metadados da Execução

```json
{
  "execution_date": "2025-10-30 19:15:12",
  "llm_provider": "Mistral",
  "model": "mistral-small",
  "temperature": 0.1,
  "prompt_file": "prompt_final_universal.txt",
  "input_file": "metadata_advanced_consolidated_filtered.json",
  "total_tables_processed": 10,
  "limit": 10
}
```

---

*Relatório gerado automaticamente pelo script de classificação de tabelas com Mistral.*
