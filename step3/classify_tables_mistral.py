"""
Script para classificar tabelas de metadados usando Mistral.

Classifica cada tabela com um score de relevância (0-100) para estudos de doenças cardiovasculares.
Gera relatórios em JSON e Markdown para análise detalhada.

Versão adaptada para o novo prompt universal com otimização de tokens.
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime
from openai import OpenAI  # Mistral API é compatível com o cliente OpenAI
from dotenv import load_dotenv


def load_prompt(prompt_file: str) -> str:
    """
    Carrega o prompt de um arquivo de texto.
    
    Args:
        prompt_file: Caminho para o arquivo de prompt
    
    Returns:
        String com o conteúdo do prompt
    """
    print(f"Carregando prompt de: {prompt_file}")
    with open(prompt_file, 'r', encoding='utf-8') as f:
        return f.read()


def load_metadata(input_file: str, limit: int = None):
    """
    Carrega o arquivo JSON de metadados.
    
    Args:
        input_file: Caminho para o arquivo JSON
        limit: Número máximo de tabelas a processar (None = todas)
    
    Returns:
        Lista de tabelas
    """
    print(f"Carregando metadados de: {input_file}")
    with open(input_file, 'r', encoding='utf-8') as f:
        metadata = json.load(f)
    
    if limit:
        metadata = metadata[:limit]
        print(f"Limitando a {limit} tabelas para teste")
    
    print(f"Total de tabelas a processar: {len(metadata)}")
    return metadata


def build_full_prompt(base_prompt: str, table_metadata: dict) -> str:
    """
    Constrói o prompt completo combinando o prompt base com os metadados da tabela.
    
    O novo formato do prompt já contém instruções completas, então substituímos
    apenas a seção de metadados JSON no final.
    
    Args:
        base_prompt: Prompt base carregado do arquivo
        table_metadata: Dicionário com metadados COMPLETOS da tabela
    
    Returns:
        String com o prompt formatado
    """
    
    # Converter metadados da tabela para JSON formatado
    metadata_json = json.dumps(table_metadata, indent=2, ensure_ascii=False)
    
    # O prompt base já tem a estrutura completa, vamos substituir a seção de metadados
    # Procurar pela seção **METADADOS DA TABELA A SER AVALIADA (JSON):**
    if "**METADADOS DA TABELA A SER AVALIADA (JSON):**" in base_prompt:
        # Dividir o prompt na seção de metadados
        parts = base_prompt.split("**METADADOS DA TABELA A SER AVALIADA (JSON):**")
        
        # Pegar a parte antes dos metadados e adicionar os metadados reais
        prompt_before = parts[0] + "**METADADOS DA TABELA A SER AVALIADA (JSON):**\n"
        
        # Pegar a parte depois dos metadados (TAREFA FINAL e FORMATO DE SAÍDA)
        # Encontrar onde começa a próxima seção
        if len(parts) > 1 and "**TAREFA FINAL:**" in parts[1]:
            prompt_after = "\n\n**TAREFA FINAL:**" + parts[1].split("**TAREFA FINAL:**")[1]
        else:
            prompt_after = ""
        
        full_prompt = f"{prompt_before}\n{metadata_json}\n{prompt_after}"
    else:
        # Fallback: apenas adicionar metadados no final
        full_prompt = f"{base_prompt}\n\n**METADADOS DA TABELA A SER AVALIADA (JSON):**\n\n{metadata_json}\n"
    
    return full_prompt


def classify_table(client: OpenAI, base_prompt: str, table_metadata: dict, model: str = "mistral-small") -> dict:
    """
    Classifica uma tabela usando a API do Mistral.
    
    Args:
        client: Cliente OpenAI (compatível com Mistral)
        base_prompt: Prompt base carregado do arquivo
        table_metadata: Metadados COMPLETOS da tabela
        model: Modelo Mistral a ser usado
    
    Returns:
        Dicionário com a classificação
    """
    
    table_name = table_metadata.get('table_name', 'N/A')
    print(f"  Classificando: {table_name}...", end=" ")
    
    try:
        full_prompt = build_full_prompt(base_prompt, table_metadata)
        
        # Aumentar max_tokens para garantir resposta completa
        # O novo formato pede score, colunas contribuintes e justificativa
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system", 
                    "content": "Você é um especialista em informática médica e doenças cardiovasculares. Responda sempre em JSON válido seguindo exatamente o formato solicitado."
                },
                {
                    "role": "user", 
                    "content": full_prompt
                }
            ],
            temperature=0.1,  # Baixa temperatura para respostas mais determinísticas
            max_tokens=800  # Aumentado para garantir resposta completa
        )
        
        # Extrair resposta
        content = response.choices[0].message.content.strip()
        
        # Tentar parsear JSON (remover markdown se presente)
        if content.startswith("```"):
            # Remover blocos de código markdown
            lines = content.split('\n')
            json_lines = []
            in_code_block = False
            for line in lines:
                if line.strip().startswith("```"):
                    in_code_block = not in_code_block
                    continue
                if in_code_block or (not line.strip().startswith("```")):
                    json_lines.append(line)
            content = '\n'.join(json_lines)
        
        # Parsear JSON
        result = json.loads(content)
        
        # Adicionar informações extras do metadado original
        result['table_name'] = table_name
        result['schema'] = table_metadata.get('schema', 'N/A')
        result['row_count'] = table_metadata.get('row_count', 0)
        
        # Garantir que campos obrigatórios existem
        if 'score_relevancia' not in result:
            result['score_relevancia'] = 0
        if 'justificativa' not in result:
            result['justificativa'] = 'Não fornecida'
        if 'colunas_contribuintes' not in result:
            result['colunas_contribuintes'] = []
        
        print(f"✓ Score: {result['score_relevancia']}")
        
        return result
        
    except json.JSONDecodeError as e:
        print(f"✗ ERRO JSON: {str(e)}")
        print(f"   Resposta recebida: {content[:200]}...")
        return {
            "table_name": table_name,
            "schema": table_metadata.get('schema', 'N/A'),
            "row_count": table_metadata.get('row_count', 0),
            "tabela": table_name,
            "chave_primaria": "ERRO",
            "score_relevancia": 0,
            "colunas_contribuintes": [],
            "justificativa": f"Erro ao parsear JSON: {str(e)}"
        }
    except Exception as e:
        print(f"✗ ERRO: {str(e)}")
        return {
            "table_name": table_name,
            "schema": table_metadata.get('schema', 'N/A'),
            "row_count": table_metadata.get('row_count', 0),
            "tabela": table_name,
            "chave_primaria": "ERRO",
            "score_relevancia": 0,
            "colunas_contribuintes": [],
            "justificativa": f"Erro ao processar: {str(e)}"
        }


def generate_json_report(results: list, output_file: str, metadata: dict):
    """
    Gera relatório em JSON para análise programática.
    
    Args:
        results: Lista de resultados da classificação
        output_file: Caminho para o arquivo de saída
        metadata: Metadados da execução
    """
    
    # Calcular estatísticas de score
    scores = [r['score_relevancia'] for r in results if isinstance(r.get('score_relevancia'), (int, float))]
    
    report = {
        "metadata": metadata,
        "summary": {
            "total_tables": len(results),
            "score_statistics": {
                "avg": sum(scores) / len(scores) if scores else 0,
                "min": min(scores) if scores else 0,
                "max": max(scores) if scores else 0,
                "median": sorted(scores)[len(scores)//2] if scores else 0
            },
            "score_distribution": {
                "high_relevance_80_100": sum(1 for s in scores if s >= 80),
                "medium_relevance_50_79": sum(1 for s in scores if 50 <= s < 80),
                "low_relevance_20_49": sum(1 for s in scores if 20 <= s < 50),
                "very_low_relevance_0_19": sum(1 for s in scores if s < 20)
            },
            "errors": sum(1 for r in results if r.get('score_relevancia') == 0 and 'ERRO' in r.get('justificativa', ''))
        },
        "classifications": results
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\nRelatório JSON salvo em: {output_file}")


def generate_markdown_report(results: list, output_file: str, metadata: dict):
    """
    Gera relatório em Markdown para leitura humana.
    
    Args:
        results: Lista de resultados da classificação
        output_file: Caminho para o arquivo de saída
        metadata: Metadados da execução
    """
    
    total = len(results)
    scores = [r['score_relevancia'] for r in results if isinstance(r.get('score_relevancia'), (int, float))]
    
    avg_score = sum(scores) / len(scores) if scores else 0
    min_score = min(scores) if scores else 0
    max_score = max(scores) if scores else 0
    
    high_rel = sum(1 for s in scores if s >= 80)
    medium_rel = sum(1 for s in scores if 50 <= s < 80)
    low_rel = sum(1 for s in scores if 20 <= s < 50)
    very_low_rel = sum(1 for s in scores if s < 20)
    errors = sum(1 for r in results if r.get('score_relevancia') == 0 and 'ERRO' in r.get('justificativa', ''))
    
    report = f"""# Relatório de Classificação de Tabelas - Mistral

**Data de Execução:** {metadata['execution_date']}  
**Modelo:** {metadata['model']}  
**LLM Provider:** {metadata['llm_provider']}  
**Temperatura:** {metadata['temperature']}

---

## Resumo Geral

| Métrica | Valor |
|---------|-------|
| **Total de Tabelas** | {total} |
| **Score Médio** | {avg_score:.2f} |
| **Score Mínimo** | {min_score} |
| **Score Máximo** | {max_score} |
| **Erros de Processamento** | {errors} |

## Distribuição de Relevância por Score

| Categoria | Score Range | Quantidade | Percentual |
|-----------|-------------|------------|------------|
| **Alta Relevância** | 80-100 | {high_rel} | {(high_rel/total*100):.1f}% |
| **Média Relevância** | 50-79 | {medium_rel} | {(medium_rel/total*100):.1f}% |
| **Baixa Relevância** | 20-49 | {low_rel} | {(low_rel/total*100):.1f}% |
| **Muito Baixa Relevância** | 0-19 | {very_low_rel} | {(very_low_rel/total*100):.1f}% |

---

## Tabelas de Alta Relevância (Score ≥ 80)

Total: **{high_rel}** tabelas

| # | Tabela | Row Count | Score | Justificativa |
|---|--------|-----------|-------|---------------|
"""
    
    # Adicionar tabelas de alta relevância
    high_rel_tables = sorted(
        [r for r in results if r.get('score_relevancia', 0) >= 80],
        key=lambda x: x.get('score_relevancia', 0),
        reverse=True
    )
    
    for idx, r in enumerate(high_rel_tables, 1):
        justification = r.get('justificativa', 'N/A')
        if len(justification) > 100:
            justification = justification[:100] + "..."
        report += f"| {idx} | `{r['table_name']}` | {r['row_count']:,} | {r.get('score_relevancia', 0)} | {justification} |\n"
    
    if not high_rel_tables:
        report += "| - | Nenhuma tabela encontrada | - | - | - |\n"
    
    report += f"""

---

## Tabelas de Média Relevância (Score 50-79)

Total: **{medium_rel}** tabelas

| # | Tabela | Row Count | Score | Justificativa |
|---|--------|-----------|-------|---------------|
"""
    
    # Adicionar tabelas de média relevância (limitar a 30)
    medium_rel_tables = sorted(
        [r for r in results if 50 <= r.get('score_relevancia', 0) < 80],
        key=lambda x: x.get('score_relevancia', 0),
        reverse=True
    )
    
    for idx, r in enumerate(medium_rel_tables[:30], 1):
        justification = r.get('justificativa', 'N/A')
        if len(justification) > 100:
            justification = justification[:100] + "..."
        report += f"| {idx} | `{r['table_name']}` | {r['row_count']:,} | {r.get('score_relevancia', 0)} | {justification} |\n"
    
    if not medium_rel_tables:
        report += "| - | Nenhuma tabela encontrada | - | - | - |\n"
    elif len(medium_rel_tables) > 30:
        report += f"\n*... e mais {len(medium_rel_tables) - 30} tabelas de média relevância*\n"
    
    report += """

---

## Detalhamento das Tabelas de Alta Relevância

"""
    
    # Detalhamento completo das tabelas de alta relevância
    for idx, r in enumerate(high_rel_tables, 1):
        colunas = r.get('colunas_contribuintes', [])
        chave_primaria = r.get('chave_primaria', 'N/A')
        
        report += f"""### {idx}. {r['table_name']}

- **Schema:** {r['schema']}
- **Row Count:** {r['row_count']:,}
- **Score de Relevância:** {r.get('score_relevancia', 0)}
- **Chave Primária:** {chave_primaria}

**Justificativa:**
{r.get('justificativa', 'N/A')}

**Colunas Contribuintes para o Score:**
"""
        if colunas:
            for col in colunas:
                report += f"- `{col}`\n"
        else:
            report += "- Nenhuma coluna específica identificada\n"
        
        report += "\n---\n\n"
    
    # Adicionar seção de erros se houver
    if errors > 0:
        report += f"""## Erros de Processamento

Total: **{errors}** tabelas com erro

| Tabela | Erro |
|--------|------|
"""
        error_tables = [r for r in results if r.get('score_relevancia') == 0 and 'ERRO' in r.get('justificativa', '')]
        for r in error_tables:
            report += f"| `{r['table_name']}` | {r.get('justificativa', 'N/A')} |\n"
    
    report += """

---

## Metadados da Execução

```json
"""
    report += json.dumps(metadata, indent=2, ensure_ascii=False)
    report += """
```

---

*Relatório gerado automaticamente pelo script de classificação de tabelas com Mistral.*
"""
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"Relatório Markdown salvo em: {output_file}")


def main():
    """
    Função principal.
    """
    
    # Carregar variáveis de ambiente
    load_dotenv()
    
    api_key = os.getenv('MISTRAL_API_KEY')
    if not api_key:
        print("ERRO: MISTRAL_API_KEY não encontrada nas variáveis de ambiente")
        print("Configure a variável MISTRAL_API_KEY no arquivo .env ou nas variáveis de ambiente do sistema")
        sys.exit(1)
    
    # Configurações
    prompt_file = "prompt_final_universal.txt"
    input_file = "metadata_advanced_consolidated_filtered.json"
    output_dir = "metadata_output_advanced"
    json_output = f"{output_dir}/classification_results_mistral.json"
    md_output = f"{output_dir}/classification_results_mistral.md"
    model = "mistral-small"  # Modelo Mistral
    limit = None
    
    # Processar argumentos da linha de comando
    if len(sys.argv) > 1:
        try:
            limit = int(sys.argv[1])
            print(f"Modo de teste: processando apenas {limit} tabelas")
        except ValueError:
            print("ERRO: O argumento deve ser um número inteiro (limit)")
            sys.exit(1)
    
    # Verificar se os arquivos necessários existem
    if not Path(prompt_file).exists():
        print(f"ERRO: Arquivo de prompt não encontrado: {prompt_file}")
        sys.exit(1)
    
    if not Path(input_file).exists():
        print(f"ERRO: Arquivo de entrada não encontrado: {input_file}")
        sys.exit(1)
    
    # Criar diretório de saída
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Carregar prompt base
    base_prompt = load_prompt(prompt_file)
    
    # Carregar metadados
    metadata_tables = load_metadata(input_file, limit)
    
    # Inicializar cliente Mistral (compatível com OpenAI)
    print(f"\nInicializando cliente Mistral (modelo: {model})...")
    client = OpenAI(
        api_key=api_key,
        base_url="https://api.mistral.ai/v1"  # Endpoint da API Mistral
    )
    
    # Classificar tabelas
    print(f"\nClassificando {len(metadata_tables)} tabelas...\n")
    results = []
    
    for idx, table in enumerate(metadata_tables, 1):
        print(f"[{idx}/{len(metadata_tables)}]", end=" ")
        result = classify_table(client, base_prompt, table, model)
        results.append(result)
    
    # Metadados da execução
    execution_metadata = {
        "execution_date": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "llm_provider": "Mistral",
        "model": model,
        "temperature": 0.1,
        "prompt_file": prompt_file,
        "input_file": input_file,
        "total_tables_processed": len(results),
        "limit": limit
    }
    
    # Gerar relatórios
    print("\n" + "="*70)
    print("Gerando relatórios...")
    print("="*70)
    
    generate_json_report(results, json_output, execution_metadata)
    generate_markdown_report(results, md_output, execution_metadata)
    
    # Resumo final
    scores = [r['score_relevancia'] for r in results if isinstance(r.get('score_relevancia'), (int, float))]
    avg_score = sum(scores) / len(scores) if scores else 0
    high_rel = sum(1 for s in scores if s >= 80)
    medium_rel = sum(1 for s in scores if 50 <= s < 80)
    errors = sum(1 for r in results if r.get('score_relevancia') == 0 and 'ERRO' in r.get('justificativa', ''))
    
    print("\n" + "="*70)
    print("RESUMO FINAL")
    print("="*70)
    print(f"Total processado: {len(results)}")
    print(f"Score médio: {avg_score:.2f}")
    print(f"Alta relevância (≥80): {high_rel} ({high_rel/len(results)*100:.1f}%)")
    print(f"Média relevância (50-79): {medium_rel} ({medium_rel/len(results)*100:.1f}%)")
    print(f"Erros: {errors}")
    print("="*70)
    print("\nProcesso concluído com sucesso!")


if __name__ == "__main__":
    print("="*70)
    print("Script de Classificação de Tabelas - Mistral")
    print("="*70)
    print()
    print("Uso: python classify_tables_mistral_updated.py [limit]")
    print()
    print("Argumentos:")
    print("  limit : Número de tabelas a processar (opcional, para testes)")
    print("          Exemplo: python classify_tables_mistral_updated.py 10")
    print()
    print("="*70)
    print()
    
    main()