#!/usr/bin/env python3
"""
Análise de acordo entre LLMs usando métricas contínuas (sem categorização).

Métricas:
- ICC(2,1), ICC(2,k), ICC(3,1), ICC(3,k)  [Shrout & Fleiss, 1979; McGraw & Wong, 1996]
- CCC pareado (Lin, 1989)  [concordância absoluta]
- Spearman pareado (ρ)     [associação monotônica]
- Kendall's W (global)     [concordância de ranqueamento multirrater]

Escalas de interpretação:
- ICC (Koo & Li, 2016): <0.50 fraco; 0.50–0.75 moderado; 0.75–0.90 bom; >0.90 excelente.
- CCC (McBride, 2005): <0.90 pobre; 0.90–0.95 moderado; 0.95–0.99 substancial; >0.99 quase perfeito.
"""

import json
import sys
import os
from pathlib import Path
import pandas as pd
import numpy as np
from datetime import datetime
from typing import List, Dict, Any, Tuple
import matplotlib.pyplot as plt
import seaborn as sns

# ==============================================================================
# 1) CARREGAMENTO E CONSOLIDAÇÃO
# ==============================================================================

def load_llm_results(file_paths: List[str]) -> Dict[str, pd.DataFrame]:
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

            required = ['table_name', 'schema', f'score_{llm_name}', f'justificativa_{llm_name}', f'colunas_{llm_name}']
            for col in required:
                if col not in df.columns:
                    df[col] = None

            all_results[llm_name] = df[required].set_index('table_name')

        except json.JSONDecodeError as e:
            print(f"ERRO: JSON inválido em {file_path}: {e}")
        except Exception as e:
            print(f"ERRO: Falha processando {file_path}: {e}")
    return all_results


def consolidate_results(llm_results: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    if not llm_results:
        return pd.DataFrame()
    consolidated_df = pd.concat([df for df in llm_results.values()], axis=1, join='outer')
    consolidated_df = consolidated_df.loc[:, ~consolidated_df.columns.duplicated()]

    score_cols = [c for c in consolidated_df.columns if c.startswith('score_')]
    consolidated_df.dropna(subset=score_cols, inplace=True)

    if consolidated_df.empty:
        print("ERRO: Sem interseção de tabelas com scores entre LLMs.")
        return pd.DataFrame()

    print(f"Resultados consolidados para {len(consolidated_df)} tabelas.")
    return consolidated_df

# ==============================================================================
# 2) MÉTRICAS CONTÍNUAS
# ==============================================================================

def _anova_components(X: np.ndarray) -> Tuple[float, float, float, float, float, float]:
    """
    Componentes da ANOVA two-way para ICCs:
    X: matriz N x k (N itens/tabelas, k avaliadores/LLMs)
    Retorna: MSR, MSC, MSE, N, k, grand_mean
    """
    N, k = X.shape
    grand_mean = X.mean()
    row_means = X.mean(axis=1, keepdims=True)
    col_means = X.mean(axis=0, keepdims=True)

    SST = ((X - grand_mean) ** 2).sum()
    SS_row = (k * (row_means - grand_mean) ** 2).sum()
    SS_col = (N * (col_means - grand_mean) ** 2).sum()
    SS_error = SST - SS_row - SS_col

    MSR = SS_row / (N - 1) if N > 1 else np.nan
    MSC = SS_col / (k - 1) if k > 1 else np.nan
    MSE = SS_error / ((N - 1) * (k - 1)) if (N > 1 and k > 1) else np.nan
    return MSR, MSC, MSE, float(N), float(k), float(grand_mean)


def icc_all(X: np.ndarray) -> Dict[str, float]:
    """
    ICCs clássicos:
    - ICC(2,1) e ICC(2,k): two-way random, absolute agreement
    - ICC(3,1) e ICC(3,k): two-way mixed, consistency
    """
    MSR, MSC, MSE, N, k, _ = _anova_components(X)

    # Evitar divisões por zero
    if any(np.isnan([MSR, MSC, MSE])) or N <= 1 or k <= 1:
        return {m: np.nan for m in ["ICC2_1", "ICC2_k", "ICC3_1", "ICC3_k"]}

    # Shrout & Fleiss (1979) / McGraw & Wong (1996)
    ICC2_1 = (MSR - MSE) / (MSR + (k - 1) * MSE + (k * (MSC - MSE) / N))
    ICC2_k = (MSR - MSE) / (MSR + ((MSC - MSE) / N))
    ICC3_1 = (MSR - MSE) / (MSR + (k - 1) * MSE)
    ICC3_k = (MSR - MSE) / MSR

    return {
        "ICC2_1": float(ICC2_1),
        "ICC2_k": float(ICC2_k),
        "ICC3_1": float(ICC3_1),
        "ICC3_k": float(ICC3_k)
    }


def lin_ccc(x: np.ndarray, y: np.ndarray) -> float:
    """
    Lin's Concordance Correlation Coefficient (CCC) entre duas séries (mesmo tamanho).
    """
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    if x.size == 0 or y.size == 0:
        return np.nan
    mu_x, mu_y = x.mean(), y.mean()
    s_x2, s_y2 = x.var(ddof=1), y.var(ddof=1)
    s_xy = np.cov(x, y, ddof=1)[0, 1]
    denom = s_x2 + s_y2 + (mu_x - mu_y) ** 2
    if denom == 0:
        return np.nan
    return float((2 * s_xy) / denom)


def pairwise_matrix(df_scores: pd.DataFrame, metric: str = "spearman") -> pd.DataFrame:
    """
    Gera matriz pareada para 'spearman' ou 'ccc' usando os scores.
    """
    cols = list(df_scores.columns)
    M = pd.DataFrame(np.nan, index=[c.split('_')[1].upper() for c in cols],
                     columns=[c.split('_')[1].upper() for c in cols])
    for i in range(len(cols)):
        for j in range(i, len(cols)):
            a = df_scores[cols[i]].to_numpy(dtype=float)
            b = df_scores[cols[j]].to_numpy(dtype=float)
            if metric == "spearman":
                rho = pd.Series(a).corr(pd.Series(b), method='spearman')
                val = float(rho) if rho is not None else np.nan
            elif metric == "ccc":
                val = lin_ccc(a, b)
            else:
                val = np.nan
            M.iloc[i, j] = val
            M.iloc[j, i] = val
        M.iloc[i, i] = 1.0
    return M


def kendalls_w(df_scores: pd.DataFrame) -> float:
    """
    Kendall's W para concordância entre k avaliadores em N itens.
    """
    # Ranquear cada coluna (avaliador) por linha (itens)
    ranks = df_scores.rank(axis=0, method='average', na_option='keep')
    # Substituir NaN por média da coluna de ranks (caso haja)
    ranks = ranks.apply(lambda col: col.fillna(col.mean()), axis=0)

    N, k = ranks.shape  # N itens, k avaliadores
    if N < 2 or k < 2:
        return np.nan

    R_i = ranks.sum(axis=1)                     # soma de ranks por item
    R_bar = R_i.mean()
    S = ((R_i - R_bar) ** 2).sum()
    W = 12 * S / (k ** 2 * (N ** 3 - N))
    return float(W)

# Interpretações (rótulos) — não alteram as métricas, apenas ajudam a ler o relatório
def interpret_icc(v: float) -> str:
    if pd.isna(v):
        return "—"
    if v < 0.50: return "Fraco"
    if v < 0.75: return "Moderado"
    if v < 0.90: return "Bom"
    return "Excelente"

def interpret_ccc(v: float) -> str:
    if pd.isna(v):
        return "—"
    if v < 0.90: return "Pobre"
    if v < 0.95: return "Moderado"
    if v < 0.99: return "Substancial"
    return "Quase perfeito"

# ==============================================================================
# 3) CÁLCULO PRINCIPAL
# ==============================================================================

def calculate_metrics(df: pd.DataFrame) -> Dict[str, Any]:
    if df.empty:
        return {}

    llm_names = sorted([c.split('_')[1] for c in df.columns if c.startswith('score_')])
    score_cols = [f'score_{n}' for n in llm_names]

    # Sanitização e estatísticas de dispersão
    for c in score_cols:
        df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0.0).clip(0.0, 100.0)
    df['score_media'] = df[score_cols].mean(axis=1).round(2)
    df['score_std']   = df[score_cols].std(axis=1).round(2).fillna(0.0)

    # Matriz N x k de scores
    X = df[score_cols].to_numpy(dtype=float)

    # ICCs globais (sobre todos os avaliadores)
    iccs = icc_all(X)

    # Matriz Spearman (pares)
    spearman_df = pairwise_matrix(df[score_cols], metric="spearman").round(4)

    # Matriz CCC (pares)
    ccc_df = pairwise_matrix(df[score_cols], metric="ccc").round(4)

    # Kendall's W (global)
    W = kendalls_w(df[score_cols])

    # Médias de matrizes pareadas (triângulo superior sem diagonal)
    def upper_offdiag_mean(M: pd.DataFrame) -> float:
        vals = []
        for i in range(M.shape[0]):
            for j in range(i + 1, M.shape[1]):
                if pd.notna(M.iloc[i, j]):
                    vals.append(float(M.iloc[i, j]))
        return round(float(np.mean(vals)), 4) if vals else float('nan')

    global_metrics = {
        'total_tabelas': int(len(df)),
        'llms_analisadas': llm_names,
        'score_medio_geral': float(df['score_media'].mean().round(2)),
        'score_std_geral': float(df['score_media'].std().round(2)),
        # ICCs:
        'ICC2_1': round(iccs["ICC2_1"], 4) if iccs["ICC2_1"] == iccs["ICC2_1"] else None,
        'ICC2_k': round(iccs["ICC2_k"], 4) if iccs["ICC2_k"] == iccs["ICC2_k"] else None,
        'ICC3_1': round(iccs["ICC3_1"], 4) if iccs["ICC3_1"] == iccs["ICC3_1"] else None,
        'ICC3_k': round(iccs["ICC3_k"], 4) if iccs["ICC3_k"] == iccs["ICC3_k"] else None,
        # Interpretações:
        'ICC2_1_label': interpret_icc(iccs["ICC2_1"]),
        'ICC2_k_label': interpret_icc(iccs["ICC2_k"]),
        'ICC3_1_label': interpret_icc(iccs["ICC3_1"]),
        'ICC3_k_label': interpret_icc(iccs["ICC3_k"]),
        # Spearman & CCC:
        'spearman_medio': upper_offdiag_mean(spearman_df),
        'ccc_medio': upper_offdiag_mean(ccc_df),
        'ccc_medio_label': interpret_ccc(upper_offdiag_mean(ccc_df)),
        # Kendall's W:
        'kendalls_w': round(W, 4) if W == W else None
    }

    return {
        'df_analise': df,
        'global_metrics': global_metrics,
        'pairwise': {
            'spearman': spearman_df,
            'ccc': ccc_df
        }
    }

# ==============================================================================
# 4) GRÁFICOS
# ==============================================================================

def generate_score_distribution_chart(df: pd.DataFrame, output_path: str, llm_names: List[str]):
    plt.figure(figsize=(12, 6))
    data_to_plot = pd.DataFrame()
    for name in llm_names:
        temp = pd.DataFrame({'LLM': name.upper(), 'Score': df[f'score_{name}']})
        data_to_plot = pd.concat([data_to_plot, temp], ignore_index=True)

    sns.kdeplot(data=data_to_plot, x='Score', hue='LLM', fill=True, alpha=.5, linewidth=2)
    plt.title('Distribuição de Scores por LLM', fontsize=16)
    plt.xlabel('Score (0–100)')
    plt.ylabel('Densidade')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.xlim(0, 100)
    plt.savefig(output_path, bbox_inches='tight')
    plt.close()
    print(f"Gráfico salvo em: {output_path}")

def generate_std_distribution_chart(df: pd.DataFrame, output_path: str):
    plt.figure(figsize=(10, 6))
    sns.histplot(df['score_std'], bins=20, kde=True, color='skyblue')
    plt.title('Distribuição do Desvio Padrão (STD) entre LLMs por Tabela', fontsize=16)
    plt.xlabel('Desvio Padrão')
    plt.ylabel('Contagem de Tabelas')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.savefig(output_path, bbox_inches='tight')
    plt.close()
    print(f"Gráfico salvo em: {output_path}")

def generate_matrix_heatmap(mat: pd.DataFrame, title: str, output_path: str, vmin: float=-1.0, vmax: float=1.0):
    plt.figure(figsize=(8, 6))
    sns.heatmap(mat, annot=True, fmt=".2f", vmin=vmin, vmax=vmax, cmap="vlag", square=True, cbar=True)
    plt.title(title, fontsize=14)
    plt.yticks(rotation=0)
    plt.savefig(output_path, bbox_inches='tight')
    plt.close()
    print(f"Heatmap salvo em: {output_path}")

# ==============================================================================
# 5) RELATÓRIOS (MD e JSON)
# ==============================================================================

def generate_markdown_report(analysis_data: Dict[str, Any], output_file: str):
    df = analysis_data['df_analise']
    metrics = analysis_data['global_metrics']
    llm_names = metrics['llms_analisadas']
    pairwise = analysis_data['pairwise']

    # --- diretório e gráficos ---
    chart_dir = Path("agreement_charts")
    chart_dir.mkdir(exist_ok=True)

    score_dist_path = chart_dir / "score_distribution.png"
    std_dist_path = chart_dir / "std_distribution.png"
    spearman_heat_path = chart_dir / "heatmap_spearman.png"
    ccc_heat_path = chart_dir / "heatmap_ccc.png"

    generate_score_distribution_chart(df, str(score_dist_path), llm_names)
    generate_std_distribution_chart(df, str(std_dist_path))
    generate_matrix_heatmap(pairwise['spearman'], "Spearman (scores) – pares de LLMs", str(spearman_heat_path), vmin=-1, vmax=1)
    generate_matrix_heatmap(pairwise['ccc'], "Lin's CCC – pares de LLMs", str(ccc_heat_path), vmin=0, vmax=1)

    # --- cabeçalhos dinâmicos ---
    score_headers = ' | '.join([f"Score {n.upper()}" for n in llm_names])
    score_placeholders = ' | '.join(['---' for _ in llm_names])

    report = f"""# Relatório de Acordo entre LLMs (Métricas Contínuas)

**Data de Execução:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**LLMs Analisadas:** {', '.join([n.upper() for n in llm_names])}  
**Total de Tabelas Consolidadas:** {metrics['total_tabelas']}

---

## 1. Resumo das Métricas Globais

| Métrica | Valor | Interpretação |
|--------|-------|---------------|
| **Score Médio Geral** | {metrics['score_medio_geral']} | — |
| **STD Geral do Score Médio** | {metrics['score_std_geral']} | — |
| **ICC(2,1)** | {metrics['ICC2_1']} | {metrics['ICC2_1_label']} |
| **ICC(2,k)** | {metrics['ICC2_k']} | {metrics['ICC2_k_label']} |
| **ICC(3,1)** | {metrics['ICC3_1']} | {metrics['ICC3_1_label']} |
| **ICC(3,k)** | {metrics['ICC3_k']} | {metrics['ICC3_k_label']} |
| **Spearman médio (pares)** | {metrics['spearman_medio']} | — |
| **CCC médio (pares)** | {metrics['ccc_medio']} | {metrics['ccc_medio_label']} |
| **Kendall's W (global)** | {metrics['kendalls_w']} | — |

> **Notas de escala**: ICC (Koo & Li, 2016) — <0,50 fraco; 0,50–0,75 moderado; 0,75–0,90 bom; >0,90 excelente.  
> CCC (McBride, 2005) — <0,90 pobre; 0,90–0,95 moderado; 0,95–0,99 substancial; >0,99 quase perfeito.

---

## 2. Tabelas de Maior Dispersão (Top 10 por STD)

| Tabela | Schema | Média Score | Desvio Padrão | {score_headers} |
|--------|--------|-------------|---------------|{score_placeholders}|
"""

    low_consensus_df = df.sort_values(by='score_std', ascending=False).head(10)
    if not low_consensus_df.empty:
        for idx, row in low_consensus_df.iterrows():
            schema_val = row['schema'] if ('schema' in row and pd.notna(row['schema'])) else '-'
            score_values = ' | '.join([str(row[f'score_{n}']) for n in llm_names])
            report += f"| `{idx}` | {schema_val} | {row['score_media']} | {row['score_std']} | {score_values} |\n"
    else:
        report += f"| - | Nenhuma tabela encontrada. | - | - | {' | '.join(['-' for _ in llm_names])} |\n"

    report += """

---

## 3. Detalhamento de Justificativas (Top 3 de Maior STD)
"""
    for idx, row in low_consensus_df.head(3).iterrows():
        report += f"### Tabela: `{idx}`\n\n"
        for n in llm_names:
            score_key = f"score_{n}"
            score_val = row[score_key]
            report += f"**{n.upper()} (Score: {score_val}):**\n"

            just_key = f"justificativa_{n}"
            txt = str(row.get(just_key, "N/A"))
            txt = txt.replace("\n", " ")
            report += f"> {txt}\n\n"
        report += "\n---\n\n"

    report += f"""
---

## 4. Visualizações

### 4.1. Distribuição de Scores por LLM
![Distribuição de Scores]({score_dist_path})

### 4.2. Distribuição do Desvio Padrão (STD) entre LLMs por Tabela
![Distribuição do Desvio Padrão]({std_dist_path})

### 4.3. Heatmap – Spearman (scores)
![Heatmap Spearman]({spearman_heat_path})

### 4.4. Heatmap – Lin's CCC
![Heatmap CCC]({ccc_heat_path})

*Relatório gerado automaticamente pelo script de análise de acordo (métricas contínuas).*
"""
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"Relatório Markdown salvo em: {output_file}")


def generate_json_report(analysis_data: Dict[str, Any], output_file: str):
    df = analysis_data['df_analise'].copy()
    metrics = analysis_data['global_metrics']

    report = {
        'metadata': {
            'execution_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'llms_analisadas': metrics['llms_analisadas'],
            'total_tabelas': metrics['total_tabelas'],
        },
        'summary_metrics': metrics,
        'table_analysis': df.reset_index().to_dict('records')
    }

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    print(f"Relatório JSON salvo em: {output_file}")

# ==============================================================================
# 6) MAIN
# ==============================================================================

def main():
    print("="*70)
    print("Acordo entre LLMs com métricas contínuas (ICC, CCC, Spearman, Kendall's W)")
    print("="*70)

    if len(sys.argv) > 1:
        llm_files = [Path(f) for f in sys.argv[1:]]
    else:
        print("Procurando por arquivos no diretório 'LLMS_results'...")
        base_dir = Path(os.getcwd())
        output_dir = base_dir / "LLMS_results"
        llm_files = list(output_dir.glob("classification_results_*.json"))

    if not llm_files:
        print("ERRO: Nenhum arquivo de resultado JSON encontrado.")
        print("Ex.: python analyze_agreement_continuous.py path/to/results1.json path/to/results2.json")
        sys.exit(1)

    json_output = Path("agreement_continuous_report.json")
    md_output = Path("agreement_continuous_report.md")

    llm_results = load_llm_results([str(f) for f in llm_files])
    if len(llm_results) < 2:
        print("\nERRO: Pelo menos 2 arquivos de resultados de LLM são necessários.")
        sys.exit(1)

    df = consolidate_results(llm_results)
    if df.empty:
        sys.exit(1)

    print("\nCalculando métricas (ICC, CCC, Spearman, Kendall's W)...")
    analysis_data = calculate_metrics(df)

    print("\n" + "="*70)
    print("Gerando relatórios...")
    print("="*70)

    generate_json_report(analysis_data, str(json_output))
    generate_markdown_report(analysis_data, str(md_output))

    print("\nConcluído!")
    print(f"Relatório Markdown: {md_output}")
    print(f"Relatório JSON: {json_output}")
    print("="*70)


if __name__ == "__main__":
    try:
        import pandas as pd
        import numpy as np
        import matplotlib.pyplot as plt
        import seaborn as sns
    except ImportError:
        print("Instalando dependências: pandas, numpy, matplotlib, seaborn...")
        os.system(f"{sys.executable} -m pip install pandas numpy matplotlib seaborn")

    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns

    main()
