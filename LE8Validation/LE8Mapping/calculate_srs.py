import json
import re
import os
from typing import List, Dict, Any, Tuple
from collections import defaultdict

# --- Configuração de Arquivos ---
# Obtendo o diretório atual onde o script está sendo executado
BASE_DIR = os.path.dirname(os.path.realpath(__file__))

# Definindo os caminhos dos arquivos com base no diretório atual
LE8_MAP_FILE = os.path.join(BASE_DIR, 'LE8Map.json')
METADATA_FILE = os.path.join(BASE_DIR, 'metadata_normalized.json')
OUTPUT_FILE = os.path.join(BASE_DIR, 'le8_metadata_match_results_v6_contextual.json')

# Lista de termos que, se encontrados sozinhos, são muito genéricos,
# mas que são importantes para o cálculo de co-ocorrência.
GENERIC_TERMS = {
    "uso", "controle", "exame", "laboratorial", "registro", "tempo", "nivel", "diario", 
    "saude", "qualidade", "corporal", "massa", "indice", "peso", "altura", "sono", 
    "duracao", "horas", "noite", "dieta", "alimentacao", "nutricao", "ingestao", 
    "comida", "sal", "acucar", "bebida", "gordura", "proteina", "fibras", 
    "carboidrato", "vitaminas", "minerais", "pressao", "glicose", "lipidio",
    "pa", "imc", "bmi", "af", "nds", "hdl", "ldl", "tg", "ct", "dm", "has", "mapa", "sisvan"
}

# --- Funções de Utilidade ---

def load_json(file_path: str) -> Any:
    """Carrega um arquivo JSON."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Erro: Arquivo não encontrado em {file_path}")
        return None
    except json.JSONDecodeError:
        print(f"Erro: Falha ao decodificar JSON em {file_path}")
        return None

def normalize_text(text: str) -> str:
    """Normaliza o texto para minúsculas e remove pontuação, mantendo apenas palavras."""
    if not isinstance(text, str):
        return ""
    text = str(text).lower()
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def tokenize_text(text: str) -> List[str]:
    """Tokeniza o texto normalizado em palavras."""
    return normalize_text(text).split()

def build_le8_term_set(le8_map: Dict) -> Dict[str, List[str]]:
    """
    Processa o mapeamento do LE8 para criar um dicionário de termos normalizados
    por componente.
    """
    le8_terms = {}
    for component_data in le8_map.get("le8_components_mapping", []):
        component_name = component_data["componente"]
        terms = component_data.get("sinonimos_variacoes", [])
        
        # Normaliza e tokeniza os termos
        normalized_terms = []
        for term in terms:
            normalized_term = normalize_text(term)
            if normalized_term:
                normalized_terms.append(normalized_term)
        
        # Ordena os termos por tamanho decrescente para priorizar a correspondência de frases mais longas
        le8_terms[component_name] = sorted(list(set(normalized_terms)), key=len, reverse=True)
        
    return le8_terms

# --- Lógica de Pontuação Contextual (Pseudo-TF-IDF/Co-ocorrência) ---

def calculate_contextual_score(text: str, le8_terms: List[str]) -> Tuple[float, List[str]]:
    """
    Calcula uma pontuação contextual para o texto com base nos termos do LE8.
    Pontuação: (Termos Específicos) * 2 + (Termos Genéricos) * 1 + (Co-ocorrência de Termos) * 3
    """
    tokens = tokenize_text(text)
    score = 0.0
    matched_terms = []
    
    # 1. Contagem de Termos
    for term in le8_terms:
        # Usa regex para garantir que o termo seja uma palavra inteira (ou sequência)
        pattern = r'\b' + re.escape(term) + r'\b'
        
        if re.search(pattern, normalize_text(text)):
            matched_terms.append(term)
            
            # 2. Atribuição de Peso
            if term in GENERIC_TERMS:
                score += 1.0 # Peso menor para termos genéricos
            else:
                score += 2.0 # Peso maior para termos específicos
    
    # 3. Pontuação por Co-ocorrência (Se houver mais de um termo do LE8)
    if len(matched_terms) >= 2:
        score += 3.0 # Bônus significativo por co-ocorrência
        
    # 4. Pontuação por Frases (Termos com mais de uma palavra)
    for term in matched_terms:
        if len(term.split()) > 1:
            score += 1.5 # Bônus por correspondência de frase
            
    # Remove duplicatas de matched_terms
    matched_terms = list(set(matched_terms))
    
    return score, matched_terms

def process_metadata(metadata: List[Dict], le8_terms_map: Dict[str, List[str]], threshold: float = 3.0) -> List[Dict]:
    """
    Processa os metadados para encontrar correspondências com os termos do LE8,
    usando a pontuação contextual e um limite (threshold).
    """
    results = []
    
    for table in metadata:
        table_name = table.get("table_name", "N/A")
        table_name_normalized = table.get("table_name_normalized", "")
        
        table_match_status = {
            "table_name": table_name,
            "table_name_normalized": table_name_normalized,
            "le8_match": {
                comp: {"match": 0, "score": 0.0, "details": []} 
                for comp in le8_terms_map.keys()
            }
        }
        
        # 1. Agrupar todo o texto relevante da tabela para cálculo de score
        table_context = defaultdict(list)
        
        # Adicionar nome da tabela
        table_context["table_name_normalized"].append(table_name_normalized)
        
        # Adicionar metadados de colunas
        for column in table.get("columns", []):
            column_name = column.get("name", "N/A")
            
            # Lista de campos de metadados a serem verificados
            fields_to_check = [
                ("column_name_normalized", column.get("column_name_normalized", "")),
            ]
            
            # Adicionar sample_values
            sample_values = column.get("stats", {}).get("sample_values", [])
            for val in sample_values:
                fields_to_check.append(("sample_value", str(val)))
            
            # Adicionar frequent_values
            frequent_values = column.get("stats", {}).get("frequent_values", [])
            for freq_val in frequent_values:
                fields_to_check.append(("frequent_value", str(freq_val.get("value", ""))))
                
            # Adicionar ao contexto da tabela
            for source_field, field_text in fields_to_check:
                table_context[source_field].append(field_text)
        
        # 2. Calcular a pontuação contextual para cada componente
        for component, terms in le8_terms_map.items():
            
            # Concatena todo o texto da tabela para o cálculo do score
            full_table_text = " ".join([normalize_text(t) for t_list in table_context.values() for t in t_list])
            
            score, matched_terms = calculate_contextual_score(full_table_text, terms)
            
            if score >= threshold:
                table_match_status["le8_match"][component]["match"] = 1
                table_match_status["le8_match"][component]["score"] = round(score, 2)
                
                # Adicionar detalhes de onde o termo foi encontrado (para depuração)
                for matched_term in matched_terms:
                    # Tenta encontrar o campo de origem para o termo
                    for source_field, field_texts in table_context.items():
                        for field_text in field_texts:
                            if re.search(r'\b' + re.escape(matched_term) + r'\b', normalize_text(field_text)):
                                # Tenta encontrar o nome da coluna se não for o nome da tabela
                                column_name = "N/A"
                                if source_field != "table_name_normalized":
                                    # Lógica simplificada para encontrar o nome da coluna que contém o field_text
                                    for col in table.get("columns", []):
                                        col_fields = [col.get("column_name_normalized", "")]
                                        col_fields.extend(col.get("stats", {}).get("sample_values", []))
                                        for freq_val in col.get("stats", {}).get("frequent_values", []):
                                            col_fields.append(freq_val.get("value", ""))
                                        
                                        if field_text in col_fields:
                                            column_name = col.get("name", "N/A")
                                            break
                                
                                table_match_status["le8_match"][component]["details"].append({
                                    "column_name": column_name,
                                    "source_field": source_field,
                                    "source_value": field_text,
                                    "matched_term": matched_term
                                })
                                # Adiciona apenas a primeira ocorrência para evitar detalhes excessivos
                                break 
                        else:
                            continue
                        break
                
                # Remove duplicatas de detalhes
                unique_details = []
                seen_details = set()
                for detail in table_match_status["le8_match"][component]["details"]:
                    detail_tuple = (detail["column_name"], detail["source_field"], detail["matched_term"])
                    if detail_tuple not in seen_details:
                        seen_details.add(detail_tuple)
                        unique_details.append(detail)
                table_match_status["le8_match"][component]["details"] = unique_details
                
            else:
                table_match_status["le8_match"][component]["score"] = 0.0
                
        results.append(table_match_status)
        
    return results

def main():
    print("Iniciando o mapeamento de metadados do LE8 (v6 - Pontuação Contextual)...")
    
    # 1. Carregar e processar o mapeamento do LE8
    le8_map_data = load_json(LE8_MAP_FILE)
    if le8_map_data is None:
        return
        
    le8_terms_map = build_le8_term_set(le8_map_data)
    print(f"Mapeamento do LE8 carregado com {len(le8_terms_map)} componentes.")
    
    # 2. Carregar os metadados
    metadata = load_json(METADATA_FILE)
    if metadata is None:
        return
        
    print(f"Metadados carregados com {len(metadata)} tabelas.")
    
    # 3. Processar e mapear com pontuação contextual (Threshold = 3.0)
    match_results = process_metadata(metadata, le8_terms_map, threshold=3.0)
    print(f"Mapeamento concluído. Resultados para {len(match_results)} tabelas.")
    
    # 4. Salvar os resultados
    try:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(match_results, f, indent=2, ensure_ascii=False)
        print(f"Resultados salvos com sucesso em {OUTPUT_FILE}")
    except Exception as e:
        print(f"Erro ao salvar o arquivo de saída: {e}")

if __name__ == "__main__":
    main()
