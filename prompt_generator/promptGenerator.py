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
PROMPT_TEMPLATE_BASE_V5 = Template(
    """
**INSTRUÇÃO DE AVALIAÇÃO DE DADOS:**
Você é um avaliador de dados especializado em **${especialidade}**. Sua tarefa é analisar os metadados da tabela e classificá-la quanto à sua **relevância** para o objetivo de pesquisa do usuário, retornando um score quantitativo e uma justificativa concisa, **seguindo rigorosamente o formato JSON de saída**.

**CONTEXTO DO ESTUDO DO USUÁRIO:**
- **Especialidade:** ${especialidade}
- **Foco de Desfecho:** ${foco_desfecho}
- **Hipótese Central:** ${hipotese_central}
- **Variáveis Chave:** ${variaveis_preditoras_chave}

**CRITÉRIOS DE AVALIAÇÃO DO SCORE DE RELEVÂNCIA (0-100):**
O Score de Relevância é uma medida de **Confiança na Utilidade da Tabela**, com a seguinte composição de pesos:
1. **Relevância Semântica (Peso 60%):** O quanto a tabela está **diretamente ligada** aos termos do estudo.
* **Sub-Critério A (30%):** Palavras-chave do **Foco de Desfecho** e **Variáveis Chave** presentes.
* **Sub-Critério B (30%):** Palavras-chave de **conceitos relacionados** (e.g., fatores de risco, preditores, ou variáveis de controle) presentes.
* **Escala Fina (0-100):** Use a escala de 0 a 100 de forma contínua (e.g., 83, 91, 77), refletindo sua confiança exata na relevância.
2. **Qualidade de Dados e Usabilidade (Peso 40%):** O quão **fácil e confiável** é usar a tabela na análise.
* **Sub-Critério C (20%):** **Completude** (Baixa taxa de dados faltantes/nulos).
* **Sub-Critério D (20%):** **Adequação** (Tipo de dado e quantidade de registros adequados ao contexto do estudo).
* **Diretriz de Penalidade:** Penalize o score se a tabela for de **baixa qualidade** (e.g., alta porcentagem de nulos, baixo row_count para o contexto de big data). Justifique a penalidade com base na **proporção** e no **contexto** da análise de ${foco_desfecho}.

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


# --- FUNÇÕES ---
def carregar_perfil_usuario(file_path):
    """Carrega o JSON de perfil do usuário."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("perfil_usuario", {})
    except FileNotFoundError:
        print(f"Erro: Arquivo de perfil não encontrado em {file_path}")
        print(
            "Por favor, crie o arquivo 'perfil_usuario.json' na mesma pasta do script."
        )
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
    
    # Prompt de sistema para o resumo
    summary_system_prompt = """
    Você é um Analista de Prompt Engineering. Sua tarefa é analisar o histórico de uma conversa entre um usuário e um assistente para refinar um prompt de avaliação de dados.
    Seu objetivo é gerar um resumo estruturado e conciso que capture todos os **ajustes e prioridades** que o usuário deseja aplicar.
    
    O resumo DEVE seguir estritamente o formato Markdown abaixo:

    A conversa indica que o usuário quer que a LLM avaliadora:
    * [Ponto 1 de Ajuste/Prioridade]
    * [Ponto 2 de Ajuste/Prioridade]
    * [Ponto N de Ajuste/Prioridade]

    **Prioridade Final:** [Única frase concisa (máximo 15 palavras) que resume o foco principal do ajuste.]
    
    Analise o histórico e preencha os pontos.
    """

    # Prompt do usuário com o histórico
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
    Simula um loop de conversação interativo com a LLM para refinar o prompt
    até que o usuário confirme que o ajuste de foco está correto.
    Retorna um resumo estruturado da conversa.
    """

    # 1. Configuração da LLM
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Erro: OPENAI_API_KEY não encontrada no arquivo .env")
        return (
            "Ajuste padrão: Priorizar tabelas com dados relevantes e alta completude."
        )

    try:
        client = OpenAI(api_key=api_key)
    except Exception as e:
        print(
            f"Erro ao inicializar o cliente OpenAI. Usando ajuste de foco padrão. Detalhe: {e}"
        )
        return (
            "Ajuste padrão: Priorizar tabelas com dados relevantes e alta completude."
        )

    # 2. Prompt de Sistema para a Interação
    system_prompt = f"""
Você é um assistente de Prompt Engineering. Sua função é ajudar o usuário a refinar o foco de sua pesquisa para um sistema de classificação de tabelas.
O perfil atual do usuário é: {json.dumps(perfil, ensure_ascii=False, indent=2)}.
Seu objetivo é guiar o usuário em uma conversa para definir um "Ajuste de Foco".
Você deve responder ao usuário com sugestões ou perguntas para refinar o foco.
O usuário encerrará a conversa digitando 'FIM' ou 'OK'.
"""

    # 3. Primeira Mensagem da LLM (Sugestão de Foco)
    initial_user_prompt = f"""
Meu foco principal é {perfil['foco_desfecho']} e as variáveis chave são {', '.join(perfil['variaveis_preditoras_chave'])}.
Para refinar o prompt de classificação, o que você sugere que eu peça à LLM para priorizar ou desconsiderar?
"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": initial_user_prompt},
    ]

    print("\n--- Início da Simulação de Conversa com a LLM (OpenAI) ---")
    print("Digite 'FIM' ou 'OK' quando o ajuste de foco estiver pronto.")

    conversation_history = []
    
    # Adiciona a primeira mensagem do usuário ao histórico para análise
    conversation_history.append(f"Você: {initial_user_prompt.strip()}")

    while True:
        try:
            # 4. Envia o histórico de mensagens e recebe a resposta da LLM
            response = client.chat.completions.create(
                model="gpt-4o-mini", messages=messages, temperature=0.5
            )
            llm_response = response.choices[0].message.content.strip()
            
            # Adiciona a resposta da LLM ao histórico da conversa
            conversation_history.append(f"LLM: {llm_response}")
            print(f"\nLLM: {llm_response}")
            messages.append({"role": "assistant", "content": llm_response})

        except Exception as e:
            print(f"\nErro na chamada da API OpenAI. Detalhe: {e}")
            print("Encerrando a interação com ajuste de foco padrão.")
            return (
                "Ajuste padrão: Priorizar tabelas com dados relevantes e alta completude."
            )

        # 5. Recebe a resposta do usuário
        user_input = input("\nVocê: ").strip()

        if user_input.upper() in ["FIM", "OK"]:
            # 6. Usuário encerrou a conversa. Gera o resumo estruturado.
            print("\n--- Fim da Simulação de Conversa ---")
            
            # Adiciona a mensagem final de confirmação ao histórico
            conversation_history.append(f"Você: {user_input}")
            
            # Gera o resumo estruturado
            final_adjustment = gerar_resumo_estruturado(client, conversation_history)
            
            print(f"\n--- Resumo Estruturado Gerado para o Prompt Final ---")
            print(final_adjustment)
            
            return final_adjustment
        
        # Adiciona a resposta do usuário ao histórico de mensagens para a próxima rodada
        messages.append({"role": "user", "content": user_input})
        conversation_history.append(f"Você: {user_input}")


def gerar_prompt_final(perfil, ajustes_foco, metadados_tabela):
    """Gera o prompt final injetando o perfil, ajustes e metadados no template V5."""

    # 1. Prepara as variáveis do perfil
    variaveis_chave_str = ", ".join(perfil.get("variaveis_preditoras_chave", []))

    # 2. Prepara os metadados da tabela
    metadados_json_str = json.dumps(metadados_tabela, ensure_ascii=False, indent=2)
    nome_tabela = metadados_tabela.get("nome_tabela", "TABELA_DESCONHECIDA")
    chave_primaria = metadados_tabela.get("chave_primaria", "NÃO ENCONTRADA")

    # 3. Mapeia os valores para o template
    template_map = {
        "especialidade": perfil.get("especialidade", "Pesquisador"),
        "foco_desfecho": perfil.get("foco_desfecho", "Resultado de Saúde"),
        "hipotese_central": perfil.get("hipotese_central", "Hipótese de Pesquisa"),
        "variaveis_preditoras_chave": variaveis_chave_str,
        "ajustes_foco": ajustes_foco,
        "metadados_tabela_json": metadados_json_str,
        "nome_tabela": nome_tabela,
        "chave_primaria": chave_primaria,
    }

    # 4. Gera o prompt final
    prompt_final = PROMPT_TEMPLATE_BASE_V5.safe_substitute(template_map)

    return prompt_final


def main():
    # 1. Carregar o perfil do usuário
    perfil = carregar_perfil_usuario(PROFILE_PATH)

    # 2. Carregar exemplo de metadados
    # Nota: O arquivo 'table_sample.json' precisa ser criado para o script rodar.
    # Para demonstração, vou criar um placeholder.
    try:
        metadados_tabela = carregar_exemplo_metadados()
    except SystemExit:
        # Cria um placeholder se o arquivo não existir para permitir a demonstração da LLM
        placeholder_metadata = {
            "nome_tabela": "tabela_placeholder",
            "chave_primaria": "id_registro",
            "colunas": [
                {"nome": "id_registro", "tipo": "int", "descricao": "ID do registro"},
                {"nome": "idade", "tipo": "int", "descricao": "Idade do paciente"},
                {"nome": "diagnostico", "tipo": "string", "descricao": "Diagnóstico principal"},
            ],
        }
        with open("table_sample.json", "w", encoding="utf-8") as f:
            json.dump(placeholder_metadata, f, ensure_ascii=False, indent=2)
        print("Criado 'table_sample.json' para demonstração.")
        metadados_tabela = placeholder_metadata


    # 3. Coletar ajustes de foco (Simulação da Interação/Chat com LLM)
    ajustes_foco = interagir_e_refinar_prompt(perfil)

    # 4. Gerar o prompt final para a tabela de exemplo
    prompt_final = gerar_prompt_final(perfil, ajustes_foco, metadados_tabela)

    # 5. Salvar o prompt final em um arquivo para visualização
    output_path = "prompt_final_universal.txt"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(prompt_final)

    print("\n--- Sucesso! Prompt Final Gerado (Versão Universal) ---")
    print(f"Prompt final salvo em: {output_path}")
    print("\n--- Conteúdo do Prompt Final ---")
    print(prompt_final)


if __name__ == "__main__":
    main()