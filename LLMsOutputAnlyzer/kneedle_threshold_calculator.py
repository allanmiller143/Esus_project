import json
import sys
import numpy as np
from kneed import KneeLocator

def find_knee_point(data, curve='convex', direction='increasing'):
    """
    Aplica o algoritmo Kneedle para encontrar o ponto de inflexão (knee point).
    
    Args:
        data (list or np.array): A lista de valores a serem analisados.
        curve (str): O tipo de curva ('convex' ou 'concave').
        direction (str): A direção da curva ('increasing' ou 'decreasing').
        
    Returns:
        float or None: O valor do knee point ou None se não for encontrado.
    """
    # Ordena os dados para garantir que o KneeLocator funcione corretamente
    # O Kneedle espera uma curva, então a ordenação é crucial.
    # Se a direção for 'increasing', ordenamos de forma crescente.
    # Se a direção for 'decreasing', ordenamos de forma decrescente.
    sorted_data = np.sort(data)
    
    # O KneeLocator precisa de um eixo X (índices) e um eixo Y (valores)
    x = np.arange(len(sorted_data))
    y = sorted_data
    
    # Se a direção for 'decreasing', precisamos inverter a curva para que o Kneedle
    # encontre o "cotovelo" (elbow) que representa o threshold.
    # No entanto, para um threshold, geralmente procuramos o ponto onde o ganho
    # marginal começa a diminuir (knee/elbow).
    # Vamos manter a direção 'increasing' e 'convex' para encontrar o ponto
    # onde a inclinação começa a diminuir, que é um threshold comum.
    # Para o caso de scores, queremos o ponto onde o score começa a ser
    # significativamente maior que os anteriores.
    
    # Vamos usar a direção 'increasing' e a curva 'convex' para encontrar o "cotovelo"
    # onde a taxa de aumento do score começa a diminuir.
    # Para encontrar um threshold de "bons scores", o ideal é encontrar o ponto
    # onde a curva de scores ordenados começa a subir mais lentamente.
    # No entanto, o Kneedle é mais robusto para encontrar o ponto de maior
    # curvatura. Vamos testar com 'increasing' e 'convex' (o padrão para knee).
    
    # Para o caso de scores, onde queremos um threshold, podemos tentar
    # 'increasing' e 'concave' para encontrar o "elbow" (ponto onde a curva
    # começa a "achatarr", indicando que os scores subsequentes não são
    # muito melhores que o ponto encontrado).
    
    # Vamos seguir a sugestão do artigo e tentar encontrar o "knee" (cotovelo)
    # que é o ponto de maior curvatura.
    
    try:
        kneedle = KneeLocator(
            x, 
            y, 
            S=1.0, # Sensibilidade, 1.0 é o padrão
            curve=curve, 
            direction=direction,
            interp_method='polynomial' # Método de interpolação
        )
        
        # O knee point é o índice no eixo X
        knee_index = kneedle.knee
        
        if knee_index is not None:
            # O threshold é o valor Y correspondente ao índice X
            threshold = y[knee_index]
            return threshold
        else:
            return None
            
    except Exception as e:
        # print(f"Erro ao calcular o knee point: {e}", file=sys.stderr)
        return None

def calculate_thresholds(json_data):
    """
    Extrai os scores e calcula os thresholds para o score médio e para cada LLM.
    """
    table_analysis = json_data.get("table_analysis", [])
    
    if not table_analysis:
        return {"error": "A chave 'table_analysis' está vazia ou ausente no JSON."}

    # 1. Extrair os scores
    scores = {
        "score_media": [item["score_media"] for item in table_analysis],
        "score_deepseek": [item["score_deepseek"] for item in table_analysis],
        "score_mistral": [item["score_mistral"] for item in table_analysis],
        "score_openai": [item["score_openai"] for item in table_analysis],
    }
    
    results = {}
    
    # 2. Calcular o threshold para cada lista de scores
    for name, score_list in scores.items():
        # Para scores, queremos encontrar o ponto onde o score começa a ser
        # significativamente "bom". Ordenamos e procuramos o "elbow" (ponto
        # onde a curva começa a subir mais lentamente, indicando que os
        # scores subsequentes não são muito melhores).
        # Usaremos 'increasing' e 'concave' para encontrar o elbow, que é
        # um bom indicador de threshold para dados ordenados.
        
        # Se usarmos 'increasing' e 'convex', encontraremos o knee, que é o
        # ponto onde a curva começa a subir mais rapidamente.
        
        # Vamos usar 'increasing' e 'concave' para encontrar o "elbow"
        # que é o ponto onde a curva começa a "achatar", o que é um bom
        # threshold para separar os "melhores" dos "piores" scores.
        
        # O Kneedle é sensível à ordenação. A ordenação é feita dentro da função.
        
        # Tentativa 1: 'increasing' e 'concave' (elbow)
        threshold_elbow = find_knee_point(score_list, curve='concave', direction='increasing')
        
        # Tentativa 2: 'increasing' e 'convex' (knee)
        threshold_knee = find_knee_point(score_list, curve='convex', direction='increasing')
        
        # Tentativa 3: 'decreasing' e 'concave' (elbow)
        threshold_elbow_dec = find_knee_point(score_list, curve='concave', direction='decreasing')
        
        # Tentativa 4: 'decreasing' e 'convex' (knee)
        threshold_knee_dec = find_knee_point(score_list, curve='convex', direction='decreasing')
        
        # Para um threshold de "qualidade", o elbow (concave, increasing) é o mais comum.
        # Se não for encontrado, tentamos o knee (convex, increasing).
        
        final_threshold = threshold_elbow
        if final_threshold is None:
            final_threshold = threshold_knee
        if final_threshold is None:
            final_threshold = threshold_elbow_dec
        if final_threshold is None:
            final_threshold = threshold_knee_dec
            
        results[name] = final_threshold if final_threshold is not None else "Não encontrado"
        
    return results

def main():
    """
    Função principal para executar o script.
    """
    if len(sys.argv) < 2:
        print("Uso: python3 kneedle_threshold_calculator.py <caminho_para_arquivo_json>")
        sys.exit(1)

    json_file_path = sys.argv[1]
    
    try:
        with open(json_file_path, 'r') as f:
            json_data = json.load(f)
    except FileNotFoundError:
        print(f"Erro: Arquivo não encontrado em '{json_file_path}'", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Erro: O arquivo '{json_file_path}' não é um JSON válido.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Erro ao ler o arquivo: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"Calculando thresholds para os scores no arquivo: {json_file_path}\n")
    
    thresholds = calculate_thresholds(json_data)
    
    print("--- Resultados do Threshold Kneedle ---")
    for name, threshold in thresholds.items():
        print(f"Threshold para {name}: {threshold}")
    print("--------------------------------------")

if __name__ == "__main__":
    # Ativa o ambiente virtual para garantir que as bibliotecas estejam disponíveis
    # Isso é feito no shell antes de executar o script, mas é bom ter a nota.
    # O script será executado com `python3 kneedle_threshold_calculator.py ...`
    main()