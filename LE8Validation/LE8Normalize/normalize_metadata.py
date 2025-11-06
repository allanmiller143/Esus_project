# normalize_metadata.py
import json
import unidecode
import re
from pathlib import Path

def normalize_text(text):
    """Normaliza o texto: minúsculas, sem acentos, sem caracteres especiais."""
    if not text:
        return ""
    text = text.lower()
    text = unidecode.unidecode(text)
    # Remove caracteres que não são letras, números ou underscore
    text = re.sub(r'[^a-z0-9_]', '', text)
    return text.strip()

def normalize_metadata_name(name):
    """
    Normaliza nomes de tabelas/colunas:
    - remove prefixos comuns (case-insensitive)
    - tokeniza por underscore e normaliza cada token
    Retorna (joined_string, tokens_list)
    """
    if not name:
        return "", []

    # Trabalhar com uma cópia para checagem de prefixo case-insensitive
    name_for_prefix = name.lower()

    # Prefixos que vamos remover (em lowercase)
    prefixes = ['tb_', 'co_', 'nu_', 'cd_', 'ds_', 'fk_', 'pk_', 'tp_', 'sg_']

    # Se tiver prefixo, remove só uma vez (o comportamento original)
    for prefix in prefixes:
        if name_for_prefix.startswith(prefix):
            # remove prefixo do nome original mantendo case para o restante
            name = name[len(prefix):]
            name_for_prefix = name_for_prefix[len(prefix):]
            break

    # Tokeniza por underscore (se houver) e normaliza tokens
    tokens = []
    for part in name.split('_'):
        if part:
            tokens.append(normalize_text(part))

    # joined string com espaços (mais legível)
    return " ".join([t for t in tokens if t]), [t for t in tokens if t]

def process_metadata(input_path, output_path):
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
    except FileNotFoundError:
        print(f"Erro: Arquivo não encontrado em {input_path}")
        return
    except json.JSONDecodeError:
        print(f"Erro: O arquivo {input_path} não é um JSON válido.")
        return

    processed = []

    for table in metadata:
        # reconstrói o dict da tabela para controlar a ordem
        new_table = {}
        for k, v in table.items():
            # copia a entrada original
            new_table[k] = v

            # se for o nome da tabela, insere os campos normalizados logo em seguida
            if k == "table_name":
                normalized_str, normalized_tokens = normalize_metadata_name(v)
                new_table["table_name_normalized"] = normalized_str
                new_table["table_name_tokens"] = normalized_tokens

            # se encontrarmos a lista de columns, vamos processar cada coluna
            if k == "columns" and isinstance(v, list):
                new_columns = []
                for col in v:
                    new_col = {}
                    # processa cada key na coluna e insere normalized logo após o nome
                    # aceitar chave 'name' e 'column_name'
                    col_name_key = None
                    if "column_name" in col:
                        col_name_key = "column_name"
                    elif "name" in col:
                        col_name_key = "name"

                    for ck, cv in col.items():
                        new_col[ck] = cv
                        # se essa chave for o nome da coluna, insere os normalized
                        if ck == col_name_key:
                            normalized_str, normalized_tokens = normalize_metadata_name(str(cv))
                            # nomes que você pediu: column_name_normalized diretamente abaixo de column_name/name
                            new_col["column_name_normalized"] = normalized_str
                            new_col["column_name_tokens"] = normalized_tokens

                    new_columns.append(new_col)
                # substitui a lista de colunas pelo novo formato ordenado
                new_table["columns"] = new_columns

        processed.append(new_table)

    # salva com ensure_ascii=False para manter acentos em outros campos
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(processed, f, indent=2, ensure_ascii=False)

    print(f"Processamento concluído. Arquivo salvo em: {output_path}")

if __name__ == "__main__":
    # usa caminho relativo (mesma pasta do script)
    base = Path(__file__).parent
    input_file = base / "metadata_advanced_consolidated_filtered.json"
    output_file = base / "metadata_normalized.json"
    process_metadata(str(input_file), str(output_file))
