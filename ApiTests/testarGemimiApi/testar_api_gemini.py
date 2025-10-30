#!/usr/bin/env python3
"""
Script para testar se a API do Google Gemini está configurada corretamente
"""

import os
import sys

print("=" * 80)
print("🔍 TESTE DE CONFIGURAÇÃO DA API GEMINI")
print("=" * 80)

# 1. Verificar se a biblioteca está instalada
print("\n1️⃣  Verificando biblioteca google-generativeai...")
try:
    import google.generativeai as genai
    print("   ✅ Biblioteca google-generativeai instalada")
except ImportError:
    print("   ❌ Biblioteca google-generativeai NÃO instalada")
    print("   Instale com: pip install google-generativeai")
    sys.exit(1)

# 2. Verificar se a variável de ambiente está configurada
print("\n2️⃣  Verificando variável de ambiente GEMINI_API_KEY...")
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("   ❌ GEMINI_API_KEY NÃO configurada")
    print("\n   Configure com:")
    print("   Windows (PowerShell): $env:GEMINI_API_KEY='AIza...'")
    print("   Linux/Mac: export GEMINI_API_KEY='AIza...'")
    print("\n   Obtenha sua chave em: https://aistudio.google.com/app/apikey")
    sys.exit(1)

print(f"   ✅ GEMINI_API_KEY configurada")
print(f"   Chave: {api_key[:10]}...{api_key[-4:]} (oculta por segurança)")

# 3. Verificar formato da chave
print("\n3️⃣  Verificando formato da chave...")
if api_key.startswith("AIza"):
    print("   ✅ Formato correto (começa com AIza)")
else:
    print("   ⚠️  ATENÇÃO: Chave não começa com 'AIza'")
    print("   Chaves do Gemini normalmente começam com 'AIza'")

# 4. Testar conexão com a API
print("\n4️⃣  Testando conexão com a API Gemini...")
try:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    print("   Enviando requisição de teste...")
    
    # Configurar segurança
    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
    ]
    
    response = model.generate_content(
        "Responda apenas: OK",
        generation_config={'temperature': 0.3, 'max_output_tokens': 10},
        safety_settings=safety_settings
    )
    
    # Verificar resposta
    if not response.candidates:
        print("   ❌ Resposta bloqueada por filtros de segurança")
        print("   Isso pode acontecer com dados médicos")
        print("   O script já está configurado para lidar com isso")
    else:
        finish_reason = response.candidates[0].finish_reason
        if finish_reason == 1:  # STOP = sucesso
            resposta = response.text
            print(f"   ✅ Conexão bem-sucedida!")
            print(f"   Resposta da API: {resposta}")
        else:
            print(f"   ⚠️  Resposta incompleta (finish_reason: {finish_reason})")
            print("   Mas a API está funcionando!")
    
except Exception as e:
    erro = str(e)
    print(f"   ❌ ERRO ao conectar: {erro}")
    
    # Diagnóstico
    print("\n" + "=" * 80)
    print("📋 DIAGNÓSTICO DO ERRO:")
    print("=" * 80)
    
    if "api key" in erro.lower() or "invalid" in erro.lower() or "401" in erro or "403" in erro:
        print("\n❌ PROBLEMA: Chave de API inválida")
        print("\nSOLUÇÕES:")
        print("1. Verifique se você copiou a chave completa")
        print("2. Crie uma nova chave em: https://aistudio.google.com/app/apikey")
        print("3. Configure novamente a variável de ambiente")
        print("4. Verifique se a chave está ativa (não expirada)")
        
    elif "quota" in erro.lower() or "limit" in erro.lower() or "429" in erro:
        print("\n❌ PROBLEMA: Limite de requisições atingido")
        print("\nINFORMAÇÕES:")
        print("Cota gratuita do Gemini:")
        print("  - 15 requisições por minuto")
        print("  - 1 milhão de tokens por dia")
        print("  - 1.500 requisições por dia")
        print("\nSOLUÇÕES:")
        print("1. Aguarde alguns minutos")
        print("2. Use o modo --teste para fazer menos requisições")
        print("3. Verifique seu uso em: https://aistudio.google.com/")
        
    elif "model" in erro.lower() or "not found" in erro.lower():
        print("\n⚠️  PROBLEMA: Modelo não disponível")
        print("\nSOLUÇÕES:")
        print("1. Verifique se você tem acesso ao gemini-2.5-flash")
        print("2. Tente usar outro modelo (ex: gemini-1.0-pro)")
        print("3. Verifique modelos disponíveis em: https://ai.google.dev/models/gemini")
        
    elif "safety" in erro.lower() or "blocked" in erro.lower():
        print("\n⚠️  PROBLEMA: Bloqueado por filtros de segurança")
        print("\nINFORMAÇÕES:")
        print("O Gemini tem filtros de segurança mais rigorosos que o GPT")
        print("Isso pode acontecer com dados médicos")
        print("\nSOLUÇÕES:")
        print("1. O script já está configurado para desabilitar filtros")
        print("2. Se continuar bloqueando, use o script OpenAI")
        print("3. Ou reduza o tamanho do JSON enviado")
        
    else:
        print(f"\n❓ ERRO DESCONHECIDO:")
        print(f"   {erro}")
        print("\nVerifique:")
        print("1. Sua conexão com a internet")
        print("2. Se o Gemini está funcionando: https://status.cloud.google.com/")
    
    print("=" * 80)
    sys.exit(1)

# 5. Testar com dados médicos (simular tabela)
print("\n5️⃣  Testando com dados médicos simulados...")
try:
    test_data = {
        "table_name": "tb_teste",
        "row_count": 100,
        "columns": [
            {"name": "co_paciente", "type": "INTEGER"},
            {"name": "dt_nascimento", "type": "DATE"}
        ]
    }
    
    response = model.generate_content(
        f"Analise esta tabela médica e responda apenas 'OK': {test_data}",
        generation_config={'temperature': 0.3, 'max_output_tokens': 10},
        safety_settings=safety_settings
    )
    
    if not response.candidates:
        print("   ⚠️  Bloqueado por filtros de segurança")
        print("   RECOMENDAÇÃO: Use o script OpenAI para dados médicos")
        print("   O Gemini pode bloquear dados de saúde mesmo com filtros desabilitados")
    else:
        finish_reason = response.candidates[0].finish_reason
        if finish_reason == 1:
            print("   ✅ Dados médicos processados com sucesso!")
        else:
            print("   ⚠️  Dados médicos podem ser bloqueados")
            print("   RECOMENDAÇÃO: Use o script OpenAI para maior confiabilidade")

except Exception as e:
    print(f"   ⚠️  Erro com dados médicos: {str(e)[:60]}")
    print("   RECOMENDAÇÃO: Use o script OpenAI para dados médicos")

# 6. Resumo final
print("\n" + "=" * 80)
print("📊 RESUMO:")
print("=" * 80)

print("\n✅ API Gemini está configurada")
print("\n⚠️  ATENÇÃO IMPORTANTE:")
print("   O Gemini pode bloquear dados médicos mesmo com filtros desabilitados")
print("   Isso é uma limitação do modelo, não do seu código")

print("\n💡 RECOMENDAÇÕES:")
print("   1. Use Gemini para testes rápidos (grátis)")
print("   2. Use OpenAI para análise final (mais confiável com dados médicos)")
print("   3. Se Gemini bloquear muito, use apenas OpenAI")

print("\n🚀 Comandos para testar:")
print("   python analyze_metadata_with_gemini.py --teste    # Teste (10 tabelas)")
print("   python analyze_metadata_with_gemini.py            # Completo")

print("\n💰 Custos:")
print("   Gemini: ~R$ 0-5 (grátis até limite)")
print("   OpenAI: ~R$ 30 (pago, mas mais confiável)")

print("=" * 80)
