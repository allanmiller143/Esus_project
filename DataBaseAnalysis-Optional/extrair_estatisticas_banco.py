#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para Extrair Estatísticas do Banco de Dados e-SUS
Extrai: número de tabelas, colunas totais, número de pacientes
"""

import os
import sys
from pathlib import Path
import json
from datetime import datetime

try:
    from sqlalchemy import create_engine, text
    from sqlalchemy.exc import SQLAlchemyError
except ImportError:
    print("❌ ERRO: sqlalchemy não encontrada")
    print("Instale com: pip install sqlalchemy psycopg2-binary")
    sys.exit(1)

try:
    from dotenv import load_dotenv
except ImportError:
    print("❌ ERRO: python-dotenv não encontrada")
    print("Instale com: pip install python-dotenv")
    sys.exit(1)


class ExtratorEstatisticas:
    """Extrai estatísticas do banco de dados e-SUS"""
    
    def __init__(self):
        # Carregar variáveis de ambiente
        load_dotenv()
        
        # Configurações do banco
        self.pg_user = os.getenv("PG_USER")
        self.pg_pass = os.getenv("PG_PASS")
        self.pg_host = os.getenv("PG_HOST", "localhost")
        self.pg_port = os.getenv("PG_PORT", "5433")
        self.pg_db = os.getenv("PG_DB")
        
        if not all([self.pg_user, self.pg_pass, self.pg_db]):
            print("❌ ERRO: Variáveis de ambiente não configuradas")
            print("\nConfigure no arquivo .env:")
            print("  PG_USER=seu_usuario")
            print("  PG_PASS=sua_senha")
            print("  PG_HOST=localhost")
            print("  PG_PORT=5433")
            print("  PG_DB=nome_do_banco")
            sys.exit(1)
        
        # String de conexão
        import urllib.parse
        pg_pass_enc = urllib.parse.quote_plus(self.pg_pass)
        self.conn_string = f"postgresql://{self.pg_user}:{pg_pass_enc}@{self.pg_host}:{self.pg_port}/{self.pg_db}"
        
        self.engine = None
        self.conn = None
        self.estatisticas = {}
    
    def conectar(self):
        """Conecta ao banco de dados"""
        print("🔌 Conectando ao banco de dados...")
        print(f"   Host: {self.pg_host}:{self.pg_port}")
        print(f"   Database: {self.pg_db}")
        print(f"   User: {self.pg_user}\n")
        
        try:
            self.engine = create_engine(self.conn_string)
            self.conn = self.engine.connect()
            print("✅ Conexão estabelecida!\n")
        except SQLAlchemyError as e:
            print(f"❌ ERRO ao conectar: {e}")
            sys.exit(1)
    
    def contar_tabelas(self):
        """Conta número total de tabelas (excluindo schemas de sistema)"""
        print("📊 Contando tabelas...")
        
        query = text("""
            SELECT 
                schemaname,
                COUNT(*) as n_tabelas
            FROM pg_tables
            WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
            GROUP BY schemaname
            ORDER BY schemaname
        """)
        
        resultado = self.conn.execute(query).fetchall()
        
        schemas = {}
        total = 0
        
        for row in resultado:
            schema = row[0]
            n_tabelas = row[1]
            schemas[schema] = n_tabelas
            total += n_tabelas
            print(f"   Schema '{schema}': {n_tabelas} tabelas")
        
        print(f"\n✅ Total: {total} tabelas\n")
        
        self.estatisticas['n_tabelas'] = total
        self.estatisticas['tabelas_por_schema'] = schemas
        
        return total
    
    def contar_colunas(self):
        """Conta número total de colunas em todas as tabelas"""
        print("📊 Contando colunas...")
        
        query = text("""
            SELECT 
                COUNT(*) as total_colunas
            FROM information_schema.columns
            WHERE table_schema NOT IN ('pg_catalog', 'information_schema')
        """)
        
        resultado = self.conn.execute(query).fetchone()
        total_colunas = resultado[0]
        
        print(f"✅ Total: {total_colunas:,} colunas\n")
        
        self.estatisticas['n_colunas'] = total_colunas
        
        return total_colunas
    
    def contar_pacientes(self):
        """Tenta contar número de pacientes únicos"""
        print("👥 Contando pacientes...")
        
        # Tentar diferentes tabelas comuns de pacientes/cidadãos
        tabelas_candidatas = [
            ('public', 'tb_cidadao', 'co_seq_cidadao'),
            ('public', 'tb_cidadao', 'co_cidadao'),
            ('public', 'tb_fat_cidadao_pec', 'co_fat_cidadao_pec'),
            ('public', 'ta_cidadao', 'co_cidadao'),
            ('public', 'tb_dim_cidadao', 'co_dim_cidadao'),
        ]
        
        pacientes_info = {}
        
        for schema, tabela, coluna_id in tabelas_candidatas:
            try:
                # Verificar se tabela existe
                query_existe = text(f"""
                    SELECT EXISTS (
                        SELECT 1 
                        FROM information_schema.tables 
                        WHERE table_schema = '{schema}' 
                        AND table_name = '{tabela}'
                    )
                """)
                
                existe = self.conn.execute(query_existe).fetchone()[0]
                
                if not existe:
                    continue
                
                # Contar registros
                query_count = text(f"""
                    SELECT COUNT(DISTINCT "{coluna_id}") as n_pacientes
                    FROM "{schema}"."{tabela}"
                """)
                
                resultado = self.conn.execute(query_count).fetchone()
                n_pacientes = resultado[0]
                
                pacientes_info[f"{schema}.{tabela}"] = {
                    "coluna_id": coluna_id,
                    "n_pacientes": n_pacientes
                }
                
                print(f"   {schema}.{tabela} ({coluna_id}): {n_pacientes:,} pacientes")
                
            except Exception as e:
                continue
        
        if pacientes_info:
            # Pegar a tabela com mais registros (provavelmente a principal)
            tabela_principal = max(pacientes_info.items(), key=lambda x: x[1]['n_pacientes'])
            n_pacientes_principal = tabela_principal[1]['n_pacientes']
            
            print(f"\n✅ Estimativa: {n_pacientes_principal:,} pacientes únicos")
            print(f"   (baseado em: {tabela_principal[0]})\n")
            
            self.estatisticas['n_pacientes'] = n_pacientes_principal
            self.estatisticas['fonte_pacientes'] = tabela_principal[0]
            self.estatisticas['todas_fontes_pacientes'] = pacientes_info
        else:
            print("⚠️  Não foi possível identificar tabela de pacientes\n")
            self.estatisticas['n_pacientes'] = None
    
    def contar_gestantes(self):
        """Tenta contar número de gestantes"""
        print("🤰 Contando gestantes...")
        
        # Tentar diferentes tabelas de gestação
        tabelas_candidatas = [
            ('public', 'tb_fat_rel_op_gestante', 'co_fat_cidadao_pec'),
            ('public', 'tb_gestante', 'co_cidadao'),
            ('public', 'ta_gestante', 'co_cidadao'),
            ('public', 'tb_dim_gestante', 'co_dim_gestante'),
        ]
        
        gestantes_info = {}
        
        for schema, tabela, coluna_id in tabelas_candidatas:
            try:
                # Verificar se tabela existe
                query_existe = text(f"""
                    SELECT EXISTS (
                        SELECT 1 
                        FROM information_schema.tables 
                        WHERE table_schema = '{schema}' 
                        AND table_name = '{tabela}'
                    )
                """)
                
                existe = self.conn.execute(query_existe).fetchone()[0]
                
                if not existe:
                    continue
                
                # Contar registros
                query_count = text(f"""
                    SELECT 
                        COUNT(*) as n_registros,
                        COUNT(DISTINCT "{coluna_id}") as n_gestantes_unicas
                    FROM "{schema}"."{tabela}"
                """)
                
                resultado = self.conn.execute(query_count).fetchone()
                n_registros = resultado[0]
                n_gestantes = resultado[1]
                
                gestantes_info[f"{schema}.{tabela}"] = {
                    "coluna_id": coluna_id,
                    "n_registros": n_registros,
                    "n_gestantes_unicas": n_gestantes
                }
                
                print(f"   {schema}.{tabela}:")
                print(f"      Registros: {n_registros:,}")
                print(f"      Gestantes únicas: {n_gestantes:,}")
                
            except Exception as e:
                continue
        
        if gestantes_info:
            # Pegar a tabela com mais registros
            tabela_principal = max(gestantes_info.items(), key=lambda x: x[1]['n_gestantes_unicas'])
            n_gestantes_principal = tabela_principal[1]['n_gestantes_unicas']
            
            print(f"\n✅ Estimativa: {n_gestantes_principal:,} gestantes únicas")
            print(f"   (baseado em: {tabela_principal[0]})\n")
            
            self.estatisticas['n_gestantes'] = n_gestantes_principal
            self.estatisticas['fonte_gestantes'] = tabela_principal[0]
            self.estatisticas['todas_fontes_gestantes'] = gestantes_info
        else:
            print("⚠️  Não foi possível identificar tabela de gestantes\n")
            self.estatisticas['n_gestantes'] = None
    
    def calcular_media_colunas_por_tabela(self):
        """Calcula média de colunas por tabela"""
        if 'n_tabelas' in self.estatisticas and 'n_colunas' in self.estatisticas:
            media = self.estatisticas['n_colunas'] / self.estatisticas['n_tabelas']
            self.estatisticas['media_colunas_por_tabela'] = round(media, 2)
            print(f"📊 Média de colunas por tabela: {media:.2f}\n")
    
    def gerar_relatorio(self):
        """Gera relatório em TXT e JSON"""
        print("📄 Gerando relatórios...")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Diretório de saída
        output_dir = Path("estatisticas_banco")
        output_dir.mkdir(exist_ok=True)
        
        # 1. JSON
        json_file = output_dir / f"estatisticas_{timestamp}.json"
        
        dados_json = {
            "metadata": {
                "data_extracao": datetime.now().isoformat(),
                "banco": self.pg_db,
                "host": self.pg_host
            },
            "estatisticas": self.estatisticas
        }
        
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(dados_json, f, indent=2, ensure_ascii=False)
        
        print(f"   ✅ JSON: {json_file}")
        
        # 2. TXT
        txt_file = output_dir / f"estatisticas_{timestamp}.txt"
        
        with open(txt_file, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("ESTATÍSTICAS DO BANCO DE DADOS E-SUS\n")
            f.write("=" * 80 + "\n\n")
            
            f.write(f"Data da Extração: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
            f.write(f"Banco de Dados: {self.pg_db}\n")
            f.write(f"Host: {self.pg_host}:{self.pg_port}\n\n")
            
            f.write("-" * 80 + "\n")
            f.write("RESUMO GERAL\n")
            f.write("-" * 80 + "\n\n")
            
            f.write(f"📊 Total de Tabelas: {self.estatisticas.get('n_tabelas', 'N/A'):,}\n")
            f.write(f"📊 Total de Colunas: {self.estatisticas.get('n_colunas', 'N/A'):,}\n")
            f.write(f"📊 Média de Colunas por Tabela: {self.estatisticas.get('media_colunas_por_tabela', 'N/A')}\n\n")
            
            if self.estatisticas.get('n_pacientes'):
                f.write(f"👥 Pacientes Únicos: {self.estatisticas['n_pacientes']:,}\n")
                f.write(f"   Fonte: {self.estatisticas['fonte_pacientes']}\n\n")
            
            if self.estatisticas.get('n_gestantes'):
                f.write(f"🤰 Gestantes Únicas: {self.estatisticas['n_gestantes']:,}\n")
                f.write(f"   Fonte: {self.estatisticas['fonte_gestantes']}\n\n")
            
            f.write("-" * 80 + "\n")
            f.write("TABELAS POR SCHEMA\n")
            f.write("-" * 80 + "\n\n")
            
            for schema, n_tabelas in self.estatisticas.get('tabelas_por_schema', {}).items():
                f.write(f"   {schema}: {n_tabelas} tabelas\n")
            
            f.write("\n" + "-" * 80 + "\n")
            f.write("PARA O ARTIGO\n")
            f.write("-" * 80 + "\n\n")
            
            f.write("A base de dados do e-SUS do município de Teixeira (PB) contém:\n\n")
            f.write(f"- {self.estatisticas.get('n_tabelas', 'N/A')} tabelas\n")
            f.write(f"- {self.estatisticas.get('n_colunas', 'N/A')} colunas totais\n")
            f.write(f"- Média de {self.estatisticas.get('media_colunas_por_tabela', 'N/A')} colunas por tabela\n")
            
            if self.estatisticas.get('n_pacientes'):
                f.write(f"- {self.estatisticas['n_pacientes']:,} pacientes cadastrados\n")
            
            if self.estatisticas.get('n_gestantes'):
                f.write(f"- {self.estatisticas['n_gestantes']:,} gestantes registradas\n")
            
            f.write("\n" + "=" * 80 + "\n")
        
        print(f"   ✅ TXT: {txt_file}")
        print(f"\n📁 Relatórios salvos em: {output_dir}\n")
        
        return txt_file, json_file
    
    def executar(self):
        """Executa extração completa"""
        print("=" * 80)
        print("📊 EXTRAÇÃO DE ESTATÍSTICAS DO BANCO DE DADOS")
        print("=" * 80)
        print()
        
        self.conectar()
        self.contar_tabelas()
        self.contar_colunas()
        self.calcular_media_colunas_por_tabela()
        self.contar_pacientes()
        self.contar_gestantes()
        
        txt_file, json_file = self.gerar_relatorio()
        
        print("=" * 80)
        print("✅ EXTRAÇÃO CONCLUÍDA!")
        print("=" * 80)
        print()
        print("📊 RESUMO:")
        print(f"   Tabelas: {self.estatisticas.get('n_tabelas', 'N/A')}")
        print(f"   Colunas: {self.estatisticas.get('n_colunas', 'N/A'):,}")
        if self.estatisticas.get('n_pacientes'):
            print(f"   Pacientes: {self.estatisticas['n_pacientes']:,}")
        if self.estatisticas.get('n_gestantes'):
            print(f"   Gestantes: {self.estatisticas['n_gestantes']:,}")
        
        # Fechar conexão
        if self.conn:
            self.conn.close()


def main():
    try:
        extrator = ExtratorEstatisticas()
        extrator.executar()
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrompido")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
