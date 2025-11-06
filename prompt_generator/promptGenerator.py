# promptGenerator.py
import json
import os
import sys
from string import Template
from openai import OpenAI
from dotenv import load_dotenv

# --- CONFIGURAÇÃO E DEFINIÇÕES PADRÃO --- #
# Carrega variáveis do .env na raiz do projeto
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

# O caminho para o arquivo de perfil do usuário (mesma pasta do script)
PROFILE_PATH = "perfil_usuario.json"

# Template de Prompt Base V5 (Universal e Focado em Estrutura)
# (MANTIDO: esquema de scores, pesos e formato de saída)
# (ATUALIZADO: bloco "CONTEXTO DO ESTUDO DO USUÁRIO" agora usa o NOVO PERFIL)
PROMPT_TEMPLATE_BASE_V5 = Template(
    """
**INSTRUÇÃO DE AVALIAÇÃO DE DADOS:**
Você é um avaliador de dados. Sua tarefa é analisar os metadados da tabela e classificá-la quanto à sua **relevância** para o objetivo do usuário, retornando um score quantitativo e uma justificativa concisa, **seguindo rigorosamente o formato JSON de saída**.

**CONTEXTO DO ESTUDO DO USUÁRIO (Perfil Declarado):**
- **Problema Geral:** ${problema_geral}
- **Escopo de Uso:** ${escopo_uso}
- **Palavras-Chave do Tema:** ${palavras_chave}
- **Exclusões Declaradas:** ${exclusoes}

**Critérios Operacionais de Relevância (do usuário):**
- **Definição Textual:** ${definicao_textual}
- **Campos/Indicadores que aumentam relevância:** ${campos_desejados}
- **Preferência (Precisão/Recall):** ${tolerancia_ruido}
- **Requisito Mínimo da Justificativa:** ${justificativa_minima}

**CRITÉRIOS DE AVALIAÇÃO DO SCORE DE RELEVÂNCIA (0-100):**

O Score de Relevância é uma medida de **Confiança na Utilidade da Tabela**, com a seguinte composição de pesos:

1. **RELEVÂNCIA SEMÂNTICA (Peso 80%)**: O quanto a tabela está **diretamente ligada** aos termos do estudo e ao problema específico do usuário.

* **Sub-Critério A (40%):** Palavras-chave do **tema** central e **campos essenciais** diretamente relacionados ao problema do usuário presentes.
* **Sub-Critério B (40%):** Conexão forte com **conceitos específicos do domínio do problema** - sinônimos exatos e termos diretamente aplicáveis à análise pretendida.
* **Diretriz de Avaliação:** Priorize tabelas com alta especificidade temática. Tabelas com informações apenas tangencialmente relacionadas devem ser severamente penalizadas, mesmo que contenham muitos dados.

2. **QUALIDADE DE DADOS E USABILIDADE (Peso 20%):** O quão fácil e confiável é usar a tabela na análise específica.
* **Sub-Critério C (10%):** **Completude contextual** - baixa taxa de nulos apenas nos campos semanticamente relevantes para o problema.
* **Sub-Critério D (10%):** **Adequação prática** - tipo de dado e quantidade de registros adequados para a análise pretendida.
* **Diretriz de Penalidade:** A completude só é valorizada quando associada a dados semanticamente relevantes. Tabelas com muitas colunas irrelevantes devem ser penalizadas, mesmo que tenham alta completude geral.

FOCO PRIMÁRIO: A relevância semântica deve ser o fator determinante. Tabelas com baixa conexão direta com o problema do usuário devem receber scores baixos (abaixo de 30), independentemente de sua completude ou quantidade de dados.

**AJUSTES DE FOCO DO USUÁRIO (Interação/Chat):**
--- RESUMO ESTRUTURADO DA INTERAÇÃO DE REFINAMENTO ---
${ajustes_foco}
--- FIM DO RESUMO ---

**METADADOS DA TABELA A SER AVALIADA (JSON):**
${metadados_tabela_json}

**TAREFA FINAL:**
1. Atribua um **Score de Relevância** de 0 a 100, usando a escala fina.
2. Forneça uma **Justificativa** **CONCISA** (máximo de 4 linhas).
3. **IDENTIFIQUE** as colunas que mais contribuíram para o score alto.

**FORMATO DE SAÍDA OBRIGATÓRIO (JSON):**
json
{
  "tabela": "${nome_tabela}",
  "chave_primaria": "${chave_primaria}",
  "score_relevancia": 83,
  "colunas_contribuintes": ["coluna1", "coluna2"],
  "justificativa": "Score X devido a [razões principais]. A tabela possui [características de qualidade]."
}
"""
)

# --- FUNÇÕES AUXILIARES PARA O NOVO PERFIL ---
def _join_list(lst, sep=", "):
    if not isinstance(lst, list):
        return ""
    return sep.join(str(x) for x in lst)

def carregar_perfil_usuario(file_path):
    """Carrega o JSON de perfil do usuário (NOVO MODELO). Espera a chave raiz 'perfil_usuario'."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        perfil = data.get("perfil_usuario", {})
        # Garantir presença das chaves esperadas do novo perfil
        criterios = perfil.get("criterios_relevancia", {})
        perfil_normalizado = {
            "problema_geral": perfil.get("problema_geral", ""),
            "escopo_uso": perfil.get("escopo_uso", ""),
            "palavras_chave": perfil.get("palavras_chave", []),
            "exclusoes": perfil.get("exclusoes", []),
            "criterios_relevancia": {
                "definicao_textual": criterios.get("definicao_textual", ""),
                "campos_desejados": criterios.get("campos_desejados", []),
                "tolerancia_ruido": criterios.get("tolerancia_ruido", ""),
                "justificativa_minima": criterios.get("justificativa_minima", "")
            }
        }
        return perfil_normalizado
    except FileNotFoundError:
        print(f"Erro: Arquivo de perfil não encontrado em {file_path}")
        print("Por favor, crie o arquivo 'perfil_usuario.json' na mesma pasta do script.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Erro: O arquivo {file_path} não é um JSON válido.")
        sys.exit(1)

def carregar_exemplo_metadados():
    """Carrega o exemplo de metadados do arquivo JSON."""
    try:
        with open("table_sample.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print("Erro: Arquivo 'table_sample.json' não encontrado.")
        print("O arquivo deve estar na mesma pasta do script.")
        sys.exit(1)
    except json.JSONDecodeError:
        print("Erro: O arquivo 'table_sample.json' não é um JSON válido.")
        sys.exit(1)

def gerar_resumo_estruturado(client, conversation_history):
    """Gera um resumo estruturado da conversa para o prompt final."""
    history_str = "\n".join(conversation_history)
    summary_system_prompt = """
    Você é um Analista de Prompt Engineering. Sua tarefa é analisar o histórico de uma conversa entre um usuário e um assistente para refinar um prompt de avaliação de dados.
    Seu objetivo é gerar um resumo estruturado e conciso que capture todos os **ajustes e prioridades** que o usuário deseja aplicar.
    O resumo DEVE seguir estritamente o formato Markdown abaixo:

    A conversa indica que o usuário quer que a LLM avaliadora:
    * [Ponto 1 de Ajuste/Prioridade]
    * [Ponto 2 de Ajuste/Prioridade]
    * [Ponto N de Ajuste/Prioridade]

    **Prioridade Final:** [Única frase concisa (máximo 15 palavras) que resume o foco principal do ajuste.]
    """
    summary_user_prompt = f"""
    **Histórico da Conversa para Análise:**
    {history_str}

    Gere o resumo estruturado.
    """
    summary_messages = [
        {"role": "system", "content": summary_system_prompt},
        {"role": "user", "content": summary_user_prompt},
    ]
    try:
        summary_response = client.chat.completions.create(
            model="gpt-4o-mini", messages=summary_messages, temperature=0.1
        )
        return summary_response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Erro ao gerar o resumo estruturado. Detalhe: {e}")
        return "Ajuste final: Não foi possível gerar o resumo estruturado. O usuário confirmou que o foco está correto."

def interagir_e_refinar_prompt(perfil):
    """
    Conversa interativa com a LLM para refinar o foco.
    AGORA: a LLM lê o PERFIL (NOVO MODELO) antes da primeira interação do usuário e já começa propondo sugestões.
    Retorna um resumo estruturado da conversa.
    """
    # 1) Configuração da LLM
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Erro: OPENAI_API_KEY não encontrada no arquivo .env")
        return "Ajuste padrão: Priorizar tabelas com dados relevantes e alta completude."
    try:
        client = OpenAI(api_key=api_key)
    except Exception as e:
        print(f"Erro ao inicializar o cliente OpenAI. Usando ajuste de foco padrão. Detalhe: {e}")
        return "Ajuste padrão: Priorizar tabelas com dados relevantes e alta completude."

    # 2) Prompt de Sistema com o PERFIL (novo) para contextualizar ANTES do primeiro input
    system_prompt = f"""
Você é um assistente de Prompt Engineering. Sua função é ajudar o usuário a refinar o foco de sua pesquisa para um sistema de classificação de tabelas.

Perfil do usuário (novo modelo):
{json.dumps(perfil, ensure_ascii=False, indent=2)}

Objetivo: conduza o usuário até um "Ajuste de Foco" claro, propondo prioridades e exclusões iniciais
com base APENAS no perfil acima.
- Apresente de forma proativa 3–5 sugestões (prioridades, exclusões, sinais fortes).
- Faça 1–2 perguntas objetivas para confirmar/ajustar.
O usuário encerrará a conversa digitando 'FIM' ou 'OK'.
"""

    # 3) Dispara a PRIMEIRA RESPOSTA da LLM (sem input prévio do usuário)
    messages = [{"role": "system", "content": system_prompt}]
    conversation_history = []

    print("\n--- Início da Simulação de Conversa com a LLM (OpenAI) ---")
    print("Dica: Digite 'FIM' ou 'OK' quando o ajuste de foco estiver pronto.")

    try:
        first_response = client.chat.completions.create(
            model="gpt-4o-mini", messages=messages, temperature=0.5
        )
        first_llm_msg = first_response.choices[0].message.content.strip()
        print(f"\nLLM: {first_llm_msg}")
        messages.append({"role": "assistant", "content": first_llm_msg})
        conversation_history.append(f"LLM: {first_llm_msg}")
    except Exception as e:
        print(f"\nErro na chamada inicial da API OpenAI. Detalhe: {e}")
        print("Encerrando a interação com ajuste de foco padrão.")
        return "Ajuste padrão: Priorizar tabelas com dados relevantes e alta completude."

    # 4) Loop de iteração com o usuário
    while True:
        user_input = input("\nVocê: ").strip()
        conversation_history.append(f"Você: {user_input}")

        if user_input.upper() in ["FIM", "OK"]:
            print("\n--- Fim da Simulação de Conversa ---")
            # 5) Gera o resumo estruturado final
            try:
                final_adjustment = gerar_resumo_estruturado(client, conversation_history)
            except Exception:
                final_adjustment = "Ajuste final: O usuário confirmou que o foco está correto."
            print(f"\n--- Resumo Estruturado Gerado para o Prompt Final ---")
            print(final_adjustment)
            return final_adjustment

        messages.append({"role": "user", "content": user_input})
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini", messages=messages, temperature=0.5
            )
            llm_response = response.choices[0].message.content.strip()
            print(f"\nLLM: {llm_response}")
            messages.append({"role": "assistant", "content": llm_response})
            conversation_history.append(f"LLM: {llm_response}")
        except Exception as e:
            print(f"\nErro na chamada da API OpenAI. Detalhe: {e}")
            print("Encerrando a interação com ajuste de foco padrão.")
            return "Ajuste padrão: Priorizar tabelas com dados relevantes e alta completude."

def gerar_prompt_final(perfil, ajustes_foco, metadados_tabela):
    """Gera o prompt final injetando o perfil (novo), ajustes e metadados no template V5 (SAÍDA MANTIDA)."""
    # Extrai campos do NOVO PERFIL
    problema_geral = perfil.get("problema_geral", "")
    escopo_uso = perfil.get("escopo_uso", "")
    palavras_chave = _join_list(perfil.get("palavras_chave", []))
    exclusoes = _join_list(perfil.get("exclusoes", []))
    criterios = perfil.get("criterios_relevancia", {})
    definicao_textual = criterios.get("definicao_textual", "")
    campos_desejados = _join_list(criterios.get("campos_desejados", []))
    tolerancia_ruido = criterios.get("tolerancia_ruido", "")
    justificativa_minima = criterios.get("justificativa_minima", "")

    # Metadados da tabela
    metadados_json_str = json.dumps(metadados_tabela, ensure_ascii=False, indent=2)
    nome_tabela = metadados_tabela.get("nome_tabela", "TABELA_DESCONHECIDA")
    chave_primaria = metadados_tabela.get("chave_primaria", "NÃO ENCONTRADA")

    # Mapeamento para o template
    template_map = {
        "problema_geral": problema_geral,
        "escopo_uso": escopo_uso,
        "palavras_chave": palavras_chave,
        "exclusoes": exclusoes,
        "definicao_textual": definicao_textual,
        "campos_desejados": campos_desejados,
        "tolerancia_ruido": tolerancia_ruido,
        "justificativa_minima": justificativa_minima,
        "ajustes_foco": ajustes_foco,
        "metadados_tabela_json": metadados_json_str,
        "nome_tabela": nome_tabela,
        "chave_primaria": chave_primaria,
    }

    prompt_final = PROMPT_TEMPLATE_BASE_V5.safe_substitute(template_map)
    return prompt_final

def main():
    # 1) Carrega o perfil do usuário (NOVO MODELO)
    perfil = carregar_perfil_usuario(PROFILE_PATH)

    # 2) Carrega metadados. Se não houver, cria placeholder para demo.
    try:
        metadados_tabela = carregar_exemplo_metadados()
    except SystemExit:
        placeholder_metadata = {
            "nome_tabela": "tabela_placeholder",
            "chave_primaria": "id_registro",
            "colunas": [
                {"nome": "id_registro", "tipo": "int", "descricao": "ID do registro"},
                {"nome": "idade", "tipo": "int", "descricao": "Idade do indivíduo"},
                {"nome": "pressao_arterial", "tipo": "float", "descricao": "Pressão arterial sistólica"},
            ],
            "row_count": 125000
        }
        with open("table_sample.json", "w", encoding="utf-8") as f:
            json.dump(placeholder_metadata, f, ensure_ascii=False, indent=2)
        print("Criado 'table_sample.json' para demonstração.")
        metadados_tabela = placeholder_metadata

    # 3) Conversa com a LLM: ela começa sugerindo com base no PERFIL (sem input inicial do usuário)
    ajustes_foco = interagir_e_refinar_prompt(perfil)

    # 4) Gera o prompt final (estrutura/saída mantidas)
    prompt_final = gerar_prompt_final(perfil, ajustes_foco, metadados_tabela)

    # 5) Salva o prompt final (mesmo arquivo de saída)
    output_path = "prompt_final_universal.txt"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(prompt_final)

    print("\n--- Sucesso! Prompt Final Gerado (Versão Universal) ---")
    print(f"Prompt final salvo em: {output_path}")
    print("\n--- Conteúdo do Prompt Final ---")
    print(prompt_final)

if __name__ == "__main__":
    main()
