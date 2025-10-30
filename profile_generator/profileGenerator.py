import json
import os

def perguntar_nao_vazio(pergunta: str) -> str:
    """Pergunta até o usuário digitar algo não vazio."""
    while True:
        try:
            valor = input(pergunta).strip()
        except KeyboardInterrupt:
            print("\nOperação cancelada pelo usuário.")
            raise SystemExit(1)
        if valor:
            return valor
        print("Por favor, preencha este campo.")

def obter_respostas():
    """Coleta as respostas do usuário de forma interativa no terminal."""
    print("=== Gerador de Perfil do Usuário ===\nResponda às perguntas abaixo:\n")

    area_estudo = perguntar_nao_vazio("1) Área de estudo principal (ex: Cardiologia): ")
    resultado_saude = perguntar_nao_vazio("2) Resultado de saúde investigado (ex: Incidência de infarto): ")
    pergunta_pesquisa = perguntar_nao_vazio("3) Principal pergunta de pesquisa (ex: 'O tabagismo afeta o colesterol?'): ")
    
    print("\n4) Informe as 3 variáveis mais importantes separadas por vírgulas")
    print("   (ex: Tabagismo, Idade, Renda)")
    variaveis_chave_raw = perguntar_nao_vazio("   Variáveis: ")
    
    # Normaliza e filtra vazios
    variaveis_chave = [v.strip() for v in variaveis_chave_raw.split(",") if v.strip()]

    return {
        "area_estudo": area_estudo,
        "resultado_saude": resultado_saude,
        "pergunta_pesquisa": pergunta_pesquisa,
        "variaveis_chave": variaveis_chave,
    }

def gerar_json_perfil(respostas: dict) -> str:
    """Gera o JSON de Perfil do Usuário e salva em arquivo na pasta específica."""
    
    # Caminho para a pasta onde o arquivo será salvo
    pasta_destino = os.path.join(os.getcwd(), "profile_generator")  # Substitua "minha_pasta" pelo nome da sua pasta
    os.makedirs(pasta_destino, exist_ok=True)  # Cria a pasta caso não exista
    
    # Caminho do arquivo de saída
    output_path = os.path.join(pasta_destino, "perfil_usuario.json")
    
    # Gera o JSON
    perfil_json = {
        "perfil_usuario": {
            "especialidade": respostas["area_estudo"],
            "foco_desfecho": respostas["resultado_saude"],
            "hipotese_central": respostas["pergunta_pesquisa"],
            "variaveis_preditoras_chave": respostas["variaveis_chave"],
        }
    }
    
    # Salva o JSON no arquivo
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(perfil_json, f, ensure_ascii=False, indent=2)

    print("\n--- Sucesso! ---")
    print(f"JSON de Perfil do Usuário gerado e salvo em: {output_path}")
    print("\nConteúdo do JSON:")
    print(json.dumps(perfil_json, ensure_ascii=False, indent=2))
    
    return output_path

if __name__ == "__main__":
    respostas = obter_respostas()
    gerar_json_perfil(respostas)
