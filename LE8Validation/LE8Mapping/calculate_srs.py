import json
from pathlib import Path
import math
import unidecode
import re

def normalize_text(text):
    """Normaliza o texto: minúsculas, sem acentos, sem caracteres especiais."""
    if not text:
        return ""
    text = text.lower()
    text = unidecode.unidecode(text)
    # Remove caracteres que não são letras, números ou underscore
    text = re.sub(r'[^a-z0-9_]', '', text)
    return text.strip()

# 1. Definição dos Pesos e Categorias
WEIGHTS = {
    "key_terms_pt": 1,
    "proxy_terms": 1,
    "measurement_fields": 1,
    "treatment_indicators": 1,
    "lab_tests_or_codes": 1,
}

def load_json(path):
    """Carrega um arquivo JSON."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Erro: Arquivo não encontrado em {path}")
        return None
    except json.JSONDecodeError:
        print(f"Erro: O arquivo {path} não é um JSON válido.")
        return None

def calculate_srs(metadata_path, le8_map_path, output_path):
    """
    Calcula o Score de Relevância Semântica (SRS) para cada tabela.
    """
    # Carregar dados
    metadata = load_json(metadata_path)
    le8_map = load_json(le8_map_path)

    if not metadata or not le8_map:
        return

    # 2. Pré-processamento do Mapeamento LE8
    # Estrutura: {token: {componente: peso}}
    le8_term_weights = {}
    for comp_id, comp_data in le8_map["components"].items():
        for category, weight in WEIGHTS.items():
            for term in comp_data.get(category, []):
                # O termo já está normalizado (minúsculas, sem acentos, com espaços)
                # O script de normalização tokeniza por underscore, então o termo composto
                # (ex: "atividade fisica") deve ser procurado como uma sequência de tokens.
                
                # Para simplificar o matching, vamos usar apenas tokens únicos por enquanto.
                # O matching de sequências de tokens é mais complexo e pode ser adicionado depois.
                # Para o SRS, a contagem de tokens individuais já é um excelente proxy.
                
                # Tokeniza o termo do LE8 para pegar as palavras individuais
                le8_tokens = term.split()
                for token in le8_tokens:
                    if token not in le8_term_weights:
                        le8_term_weights[token] = {}
                    
                    # Se o token já foi visto em uma categoria de peso maior, mantém o peso maior
                    current_weight = le8_term_weights[token].get(comp_id, 0)
                    le8_term_weights[token][comp_id] = max(current_weight, weight)

    # 3. Cálculo do SRS para cada Tabela
    srs_results = []
    all_srs_scores = []

    for table_data in metadata:
        table_name = table_data.get("table_name")
        
        # 3.1. Coletar todos os tokens da tabela (nome + colunas + sample_values)
        
        # Estrutura para rastreabilidade: {componente: [{campo: token}]}
        occurrence_report = {comp_id: [] for comp_id in le8_map["components"].keys()}
        
        # 3.2. Função auxiliar para processar tokens e registrar ocorrências
        def process_tokens(tokens, source_field, source_name):
            nonlocal srs_raw_score
            
            for token in tokens:
                if token in le8_term_weights:
                    # O token é relevante para o LE8
                    for comp_id, weight in le8_term_weights[token].items():
                        # Adiciona o peso ao score do componente e ao score total
                        component_scores[comp_id] += weight
                        srs_raw_score += weight
                        
                        # Rastreabilidade
                        occurrence_report[comp_id].append({
                            "source_field": source_field,
                            "source_name": source_name,
                            "token": token,
                            "weight": weight
                        })

        # Inicialização
        srs_raw_score = 0
        component_scores = {comp_id: 0 for comp_id in le8_map["components"].keys()}
        
        # Processar nome da tabela
        process_tokens(table_data.get("table_name_tokens", []), "table_name", table_name)
        
        # Processar colunas
        for column in table_data.get("columns", []):
            column_name = column.get("name", "N/A")
            
            # Processar nome da coluna
            process_tokens(column.get("column_name_tokens", []), "column_name", column_name)
            
            # Processar sample_values (convertendo para tokens)
            sample_values = column.get("stats", {}).get("sample_values", [])
            if sample_values:
                # Normaliza e tokeniza os sample_values
                sample_tokens = []
                for value in sample_values:
                    # Usando a função de normalização completa para garantir consistência
                    normalized_value = normalize_text(str(value))
                    sample_tokens.extend(normalized_value.split())
                
                # Remove duplicatas e processa
                process_tokens(set(sample_tokens), "sample_values", column_name)
        
        # 3.3. Armazenar o resultado
        result = {
            "table_name": table_name,
            "srs_raw_score": srs_raw_score,
            "component_scores": component_scores,
            "occurrence_report": occurrence_report
        }
        srs_results.append(result)
        all_srs_scores.append(srs_raw_score)
        
        # 3.3. Armazenar o resultado
        result = {
            "table_name": table_name,
            "srs_raw_score": srs_raw_score,
            "component_scores": component_scores,
            "occurrence_report": occurrence_report
        }
        srs_results.append(result)
        all_srs_scores.append(srs_raw_score)

    # 4. Normalização do SRS
    if not all_srs_scores:
        print("Nenhuma tabela encontrada para pontuação.")
        return

    srs_min = min(all_srs_scores)
    srs_max = max(all_srs_scores)
    srs_range = srs_max - srs_min

    for result in srs_results:
        raw_score = result["srs_raw_score"]
        
        if srs_range == 0:
            # Evita divisão por zero (todas as tabelas têm o mesmo score)
            normalized_score = 0.0
        else:
            # Fórmula de normalização Min-Max para 0-100
            normalized_score = ((raw_score - srs_min) / srs_range) * 100
        
        result["srs_normalized_score"] = round(normalized_score, 2)

    # 5. Salvar o resultado
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(srs_results, f, indent=2, ensure_ascii=False)
    
    print(f"Cálculo do SRS concluído. Resultados salvos em {output_path}")

if __name__ == "__main__":
    base = Path(__file__).parent
    
    # Certifique-se de que os nomes dos arquivos estão corretos
    metadata_file = base / "metadata_normalized.json"
    le8_map_file = base / "le8_mapping_full_final.json" # Usando a versão final corrigida
    output_file = base / "srs_results.json"
    
    # Movendo os arquivos fornecidos pelo usuário para o diretório base para que o script encontre
    # Assumindo que o usuário forneceu os arquivos corretos no último prompt
    
    # Renomeando o arquivo LE8Map.json do usuário para o nome que o script espera
    # Para evitar erros, vamos usar o nome que o usuário forneceu no último prompt
    # e garantir que o script use esse nome.
    
    # Se o usuário forneceu o LE8Map.json, vamos usá-lo.
    # Se o usuário forneceu o metadata_normalized.json, vamos usá-lo.
    
    # Para garantir que o script funcione, vamos usar os nomes que foram gerados
    # e assumir que o usuário os moveu para o diretório base.
    
    # Para a execução, vamos usar os nomes que foram gerados na etapa anterior:
    # le8_map_file = base / "le8_mapping_full_final.json"
    # metadata_file = base / "metadata_normalized.jsoif __name__ == "__main__":
    base = Path(__file__).parent
    
    # Usando caminhos relativos, assumindo que os arquivos estão na mesma pasta
    # que o script calculate_srs.py
    calculate_srs(
        metadata_path="metadata_normalized.json",
        le8_map_path="LE8Map.json",
        output_path="srs_results.json"
    )