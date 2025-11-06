import json
import os

# ============================
# (Opcional) CONFIGURAÇÕES INTERNAS DO SISTEMA – definidas por VOCÊ, não pelo usuário
# Preencha/importe isso no seu pipeline; aqui fica só como referência.
# ============================
CONFIG_PADRAO = {
    # "escala_score": "0-100",
    # "limiar_corte": 70,
    # "metodo_consenso": "media>=limiar",
    # "prioridade_desempate": "maior_score_medio",
    # "tamanho_view": 40,
    # "formato_saida": "VIEW_MATERIALIZADA",
    # "restricoes_privacidade": ["anonimizar_CPFS"],
    # "validacao_proxy": {"fonte": "nenhuma", "estrategia": None},
}

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

def obter_lista(pergunta: str, minimo: int = 0):
    """Coleta lista separada por vírgulas, removendo vazios e espaços."""
    while True:
        raw = perguntar_nao_vazio(pergunta)
        itens = [v.strip() for v in raw.split(",") if v.strip()]
        if len(itens) >= minimo:
            return itens
        print(f"Informe pelo menos {minimo} item(ns).")

def obter_respostas():
    """
    Perfil simples, agnóstico de domínio e embasado por 'context enhancement':
    - Contexto do problema/uso (conhecimento/objetivo)
    - Vocabulário e exclusões (guia de relevância)
    - Preferência precisão/recall
    - Requisito mínimo de explicabilidade
    """
    print("=== Perfil do Usuário para Classificação de Tabelas (Agnóstico) ===\n")

    # 1) Contexto do problema/uso
    problema_geral = perguntar_nao_vazio(
        "1) Em uma frase, qual é o problema/tema que você quer investigar no banco? "
    )
    escopo = perguntar_nao_vazio(
        "2) O que você quer fazer com a base? (ex.: triagem de tabelas e geração de uma view resumida) "
    )

    # 2) Vocabulário: termos que traduzem o tema e itens a excluir
    palavras_chave = obter_lista(
        "3) Liste 5–15 termos/sinônimos/entidades que representem o tema (separe por vírgulas): ", minimo=5
    )
    exclusoes = obter_lista(
        "4) Liste termos/tipos de dado que NÃO devem caracterizar relevância (ex.: logs técnicos, tabelas temporárias): ", minimo=0
    )

    # 3) Definição operacional do que é “tabela relevante”
    criterio_texto = perguntar_nao_vazio(
        "5) Em 1–2 frases, descreva o que FAZ uma tabela ser relevante para este problema: "
    )
    campos_desejados = obter_lista(
        "6) Quais campos/indicadores (nomes aproximados) aumentam a chance de relevância? (ex.: id_cliente, data_evento): ", minimo=1
    )

    # 4) Trade-off e explicabilidade mínima
    tolerancia_ruido = perguntar_nao_vazio(
        "7) Você prefere 'alta precisão', 'alto recall' ou 'equilíbrio'? "
    )
    justificativa_minima = perguntar_nao_vazio(
        "8) O que a justificativa da LLM deve obrigatoriamente conter? (ex.: citar colunas/termos exatos e o porquê) "
    )

    return {
        "problema_geral": problema_geral,
        "escopo_uso": escopo,
        "palavras_chave": palavras_chave,
        "exclusoes": exclusoes,
        "criterios_relevancia": {
            "definicao_textual": criterio_texto,
            "campos_desejados": campos_desejados,
            "tolerancia_ruido": tolerancia_ruido,
            "justificativa_minima": justificativa_minima
        }
    }

def gerar_json_perfil(respostas: dict) -> str:
    """Gera o JSON de Perfil e salva em profile_generator/perfil_usuario.json."""
    pasta_destino = os.path.join(os.getcwd(), "profile_generator")
    os.makedirs(pasta_destino, exist_ok=True)
    output_path = os.path.join(pasta_destino, "perfil_usuario.json")

    perfil_json = {"perfil_usuario": respostas}

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
