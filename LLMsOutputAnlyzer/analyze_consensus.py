#!/usr/bin/env python3
"""
Script para analisar o consenso de classificação de tabelas entre múltiplas LLMs.

Lê arquivos JSON de resultados de classificação (Mistral, DeepSeek, OpenAI)
e gera um relatório consolidado com métricas de consenso (média, desvio padrão,
concordância de score e concordância de relevância).
"""

import json
import sys
import os
from pathlib import Path
import pandas as pd
import numpy as np
from datetime import datetime
from typing import List, Dict, Any
import matplotlib.pyplot as plt
import seaborn as sns

# ==============================================================================
# 1. FUNÇÕES DE CARREGAMENTO E CONSOLIDAÇÃO DE DADOS
# ==============================================================================

def load_llm_results(file_paths: List[str]) -> Dict[str, pd.DataFrame]:
    """
    Carrega os resultados de classificação de múltiplas LLMs a partir de arquivos JSON.

    Args:
        file_paths: Lista de caminhos para os arquivos JSON de resultados.

    Returns:
        Um dicionário onde a chave é o nome da LLM (inferido do nome do arquivo)
        e o valor é um DataFrame do pandas com os resultados.
    """
    all_results = {}
    
    for file_path in file_paths:
        path = Path(file_path)
        if not path.exists():
            print(f"AVISO: Arquivo não encontrado: {file_path}. Ignorando esta LLM.")
            continue

        llm_name = path.stem.split("_")[-1]
        
        print(f"Carregando resultados de {llm_name.upper()} de: {file_path}")
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            classifications = data.get('classifications', [])
            df = pd.DataFrame(classifications)
            
            df = df.rename(columns={
                'score_relevancia': f'score_{llm_name}',
                'justificativa': f'justificativa_{llm_name}',
                'colunas_contribuintes': f'colunas_{llm_name}'
            })
            
            required_cols = ['table_name', 'schema', f'score_{llm_name}', f'justificativa_{llm_name}', f'colunas_{llm_name}']
            for col in required_cols:
                if col not in df.columns:
                    df[col] = None
            
            df = df[required_cols]
            df = df.set_index('table_name')
            
            all_results[llm_name] = df
            
        except json.JSONDecodeError as e:
            print(f"ERRO: Erro ao decodificar JSON em {file_path}: {e}")
        except Exception as e:
            print(f"ERRO: Um erro inesperado ocorreu ao processar {file_path}: {e}")
            
    return all_results

def consolidate_results(llm_results: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """
    Consolida os DataFrames de resultados em um único DataFrame para análise.
    """
    if not llm_results:
        return pd.DataFrame()

    # Usar 'outer' join para manter todas as tabelas de todos os arquivos
    # e depois filtrar as que não têm scores de todas as LLMs.
    dfs = [df for df in llm_results.values()]
    consolidated_df = pd.concat(dfs, axis=1, join='outer')

    # Remover colunas duplicadas de 'schema'
    consolidated_df = consolidated_df.loc[:, ~consolidated_df.columns.duplicated()]
    
    score_cols = [col for col in consolidated_df.columns if col.startswith('score_')]
    consolidated_df.dropna(subset=score_cols, inplace=True)

    if len(consolidated_df) == 0:
        print("ERRO: Não foi possível consolidar os resultados. Verifique se os arquivos JSON contêm tabelas em comum.")
        return pd.DataFrame()
        
    print(f"Resultados consolidados para {len(consolidated_df)} tabelas.")
    
    return consolidated_df

# ==============================================================================
# 2. FUNÇÕES DE CÁLCULO DE MÉTRICAS
# ==============================================================================

def calculate_metrics(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Calcula métricas de consenso e estatísticas a partir do DataFrame consolidado.
    """
    if df.empty:
        return {}

    llm_names = sorted([col.split('_')[1] for col in df.columns if col.startswith('score_')])
    score_cols = [f'score_{name}' for name in llm_names]
    
    for col in score_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    df['score_media'] = df[score_cols].mean(axis=1).round(2)
    df['score_std'] = df[score_cols].std(axis=1).round(2).fillna(0)
    
    def categorize_score(score: int) -> str:
        if score >= 80: return 'Alta'
        if score >= 50: return 'Média'
        if score >= 20: return 'Baixa'
        return 'Muito Baixa'
        
    for name in llm_names:
        df[f'relevancia_{name}'] = df[f'score_{name}'].apply(categorize_score)

    relevance_cols = [f'relevancia_{name}' for name in llm_names]

    df['concordancia_categoria'] = df[relevance_cols].apply(lambda x: x.nunique() == 1, axis=1)
    
    score_range = df[score_cols].max(axis=1) - df[score_cols].min(axis=1)
    df['concordancia_score_10'] = score_range <= 10
    
    total_tables = len(df)
    
    global_metrics = {
        'total_tabelas': total_tables,
        'llms_analisadas': llm_names,
        'score_medio_geral': df['score_media'].mean().round(2),
        'score_std_geral': df['score_media'].std().round(2),
        'percentual_concordancia_categoria': (df['concordancia_categoria'].sum() / total_tables * 100).round(2) if total_tables > 0 else 0,
        'percentual_concordancia_score_10': (df['concordancia_score_10'].sum() / total_tables * 100).round(2) if total_tables > 0 else 0,
        'tabelas_alto_consenso': df[df['score_std'] <= 5].shape[0],
        'tabelas_baixo_consenso': df[df['score_std'] > 15].shape[0]
    }
    
    return {'df_analise': df, 'global_metrics': global_metrics}

# ==============================================================================
# 3. FUNÇÕES DE GERAÇÃO DE RELATÓRIOS
# ==============================================================================

def generate_score_distribution_chart(df: pd.DataFrame, output_path: str, llm_names: List[str]):
    """Gera um gráfico de distribuição de scores para cada LLM."""
    plt.figure(figsize=(12, 6))
    
    # Prepara os dados para o gráfico de distribuição
    data_to_plot = pd.DataFrame()
    for name in llm_names:
        temp_df = pd.DataFrame({
            'LLM': name.upper(),
            'Score': df[f'score_{name}']
        })
        data_to_plot = pd.concat([data_to_plot, temp_df])

    sns.kdeplot(data=data_to_plot, x='Score', hue='LLM', fill=True, alpha=.5, linewidth=2)
    
    plt.title('Distribuição de Scores de Relevância por LLM', fontsize=16)
    plt.xlabel('Score de Relevância (0-100)', fontsize=12)
    plt.ylabel('Densidade', fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.xlim(0, 100)
    
    plt.savefig(output_path, bbox_inches='tight')
    plt.close()
    print(f"Gráfico de distribuição salvo em: {output_path}")

def generate_std_distribution_chart(df: pd.DataFrame, output_path: str):
    """Gera um gráfico de distribuição do Desvio Padrão (STD) dos scores."""
    plt.figure(figsize=(10, 6))
    
    sns.histplot(df['score_std'], bins=20, kde=True, color='skyblue')
    
    plt.title('Distribuição do Desvio Padrão (STD) dos Scores', fontsize=16)
    plt.xlabel('Desvio Padrão do Score', fontsize=12)
    plt.ylabel('Contagem de Tabelas', fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Adicionar linha para o limite de "Baixo Consenso" (STD > 15)
    low_consensus_threshold = 15
    plt.axvline(low_consensus_threshold, color='red', linestyle='--', linewidth=1.5, label=f'Baixo Consenso (STD > {low_consensus_threshold})')
    plt.legend()
    
    plt.savefig(output_path, bbox_inches='tight')
    plt.close()
    print(f"Gráfico de Desvio Padrão salvo em: {output_path}")

def generate_markdown_report(analysis_data: Dict[str, Any], output_file: str):
    """
    Gera um relatório consolidado em formato Markdown.
    """
    df = analysis_data['df_analise']
    metrics = analysis_data['global_metrics']
    llm_names = metrics['llms_analisadas']

    # Construção dinâmica dos cabeçalhos da tabela
    score_headers = ' | '.join([f"Score {name.upper()}" for name in llm_names])
    score_placeholders = ' | '.join(['---' for _ in llm_names])

    # --- Geração dos Gráficos ---
    chart_dir = Path("consensus_charts")
    chart_dir.mkdir(exist_ok=True)
    
    score_dist_path = chart_dir / "score_distribution.png"
    std_dist_path = chart_dir / "std_distribution.png"
    
    generate_score_distribution_chart(df, str(score_dist_path), llm_names)
    generate_std_distribution_chart(df, str(std_dist_path))
    # ----------------------------
    report = f"""# Relatório de Análise de Consenso de Classificação de Tabelas
    
**Data de Execução:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**LLMs Analisadas:** {', '.join([n.upper() for n in llm_names])}  
**Total de Tabelas Consolidadas:** {metrics['total_tabelas']}
    
---
    
## 1. Resumo das Métricas de Consenso
    
| Métrica | Valor | Unidade |
|---------|-------|---------|
| **Score Médio Geral** | {metrics['score_medio_geral']} | Pontos |
| **Desvio Padrão Geral do Score Médio** | {metrics['score_std_geral']} | Pontos |
| **Concordância Total de Categoria** | {metrics['percentual_concordancia_categoria']}% | Percentual |
| **Concordância de Score (Range <= 10)** | {metrics['percentual_concordancia_score_10']}% | Percentual |
| **Tabelas de Alto Consenso (STD <= 5)** | {metrics['tabelas_alto_consenso']} | Contagem |
| **Tabelas de Baixo Consenso (STD > 15)** | {metrics['tabelas_baixo_consenso']} | Contagem |
    
---
    
## 2. Tabelas de Maior Discordância (Top 10)
    
Esta seção lista as 10 tabelas onde as LLMs discordaram mais significativamente (maior Desvio Padrão do Score).
    
| Tabela | Schema | Média Score | Desvio Padrão | Categoria Consenso | {score_headers} |
|--------|--------|-------------|---------------|--------------------|{score_placeholders}|
"""
    
    # low_consensus_df agora pega o top 10 por score_std
    low_consensus_df = df.sort_values(by='score_std', ascending=False).head(10)
    
    for index, row in low_consensus_df.iterrows():
        categories = [row[f'relevancia_{name}'] for name in llm_names]
        consensus_category = categories[0] if len(set(categories)) == 1 else 'Discordância'
        score_values = ' | '.join([str(row[f'score_{name}']) for name in llm_names])
        report += f"| `{index}` | {row['schema']} | {row['score_media']} | {row['score_std']} | {consensus_category} | {score_values} |\n"
        
    if low_consensus_df.empty:
        report += f"| - | Nenhuma tabela consolidada encontrada. | - | - | - | {' | '.join(['-' for _ in llm_names])} |\n"

    report += """
    
---
    
## 3. Detalhamento de Justificativas (Top 3 de Maior Discordância)
    
Para as 3 tabelas com maior discordância, as justificativas de cada LLM são listadas abaixo para análise manual.
    
"""
    
    # Limita o detalhamento de justificativas ao Top 3
    for index, row in low_consensus_df.head(3).iterrows():
        report += f"### Tabela: `{index}`\n\n"
        for name in llm_names:
            report += f"**{name.upper()} (Score: {row[f'score_{name}']}):**\n"
            report += f"> {str(row.get(f'justificativa_{name}', 'N/A')).replace('\n', ' ')}\n\n"
        report += "\n---\n\n"

    report += f"""
---

## 4. Visualização Gráfica

### 4.1. Distribuição de Scores de Relevância por LLM

![Distribuição de Scores]({score_dist_path})

### 4.2. Distribuição do Desvio Padrão (STD) dos Scores

![Distribuição do Desvio Padrão]({std_dist_path})

*Relatório gerado automaticamente pelo script de análise de consenso.*
"""
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\nRelatório Markdown salvo em: {output_file}")

def generate_json_report(analysis_data: Dict[str, Any], output_file: str):
    """
    Gera um relatório consolidado em formato JSON.
    """
    df = analysis_data['df_analise'].copy()
    metrics = analysis_data['global_metrics']
    
    # Remover 'df_analise' para evitar redundância no JSON
    metrics_copy = metrics.copy()
    if 'df_analise' in metrics_copy:
        del metrics_copy['df_analise']

    analysis_results = df.reset_index().to_dict('records')
    
    report = {
        'metadata': {
            'execution_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'llms_analisadas': metrics['llms_analisadas'],
            'total_tabelas': metrics['total_tabelas'],
        },
        'summary_metrics': metrics_copy,
        'table_analysis': analysis_results
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"Relatório JSON salvo em: {output_file}")


# ==============================================================================
# 4. FUNÇÃO PRINCIPAL
# ==============================================================================

def main():
    """
    Função principal.
    """
    
    print("="*70)
    print("Script de Análise de Consenso de Classificação de Tabelas")
    print("="*70)
    
    # O usuário pode passar os nomes dos arquivos como argumentos
    if len(sys.argv) > 1:
        llm_files = [Path(f) for f in sys.argv[1:]]
    else:
        # Ou podemos procurar por eles no diretório padrão
        print("Procurando por arquivos de resultado no diretório 'LLMS_results'...")
        base_dir = Path(os.getcwd())
        output_dir = base_dir / "LLMS_results"
        llm_files = list(output_dir.glob("classification_results_*.json"))

    if not llm_files:
        print("ERRO: Nenhum arquivo de resultado JSON encontrado.")
        print("Execute o script passando os caminhos dos arquivos como argumentos, ex:")
        print("python analyze_consensus.py path/to/results1.json path/to/results2.json")
        sys.exit(1)

    json_output = Path("consensus_report.json")
    md_output = Path("consensus_report.md")
    
    llm_results = load_llm_results([str(f) for f in llm_files])
    
    if len(llm_results) < 2:
        print("\nERRO: Pelo menos 2 arquivos de resultados de LLM são necessários para a análise de consenso.")
        sys.exit(1)
        
    consolidated_df = consolidate_results(llm_results)
    
    if consolidated_df.empty:
        sys.exit(1)
        
    print("\nCalculando métricas de consenso...")
    analysis_data = calculate_metrics(consolidated_df)
    
    print("\n" + "="*70)
    print("Gerando relatórios de consenso...")
    print("="*70)
    
    generate_json_report(analysis_data, str(json_output))
    generate_markdown_report(analysis_data, str(md_output))
    
    print("\nProcesso de análise de consenso concluído com sucesso!")
    print(f"Relatório Markdown: {md_output}")
    print(f"Relatório JSON: {json_output}")
    print("="*70)


if __name__ == "__main__":
    # Garante que as dependências estejam instaladas antes de qualquer importação
    try:
        import pandas as pd
        import numpy as np
        import matplotlib.pyplot as plt
        import seaborn as sns
    except ImportError:
        print("Instalando dependências: pandas, numpy, matplotlib e seaborn...")
        os.system(f"{sys.executable} -m pip install pandas numpy matplotlib seaborn")
        
    # Re-importa para garantir que estejam disponíveis após a instalação
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns
        
    main()