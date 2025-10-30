#!/usr/bin/env python3
"""
Script para testar se a API da OpenAI está configurada corretamente
"""

import os
import sys

print("=" * 80)
print("🔍 TESTE DE CONFIGURAÇÃO DA API OPENAI")
print("=" * 80)

# 1. Verificar se a biblioteca está instalada
print("\n1️⃣  Verificando biblioteca openai...")
try:
    from openai import OpenAI
    print("   ✅ Biblioteca openai instalada")
except ImportError:
    print("   ❌ Biblioteca openai NÃO instalada")
    print("   Instale com: pip install openai")
    sys.exit(1)

# 2. Verificar se a variável de ambiente está configurada
print("\n2️⃣  Verificando variável de ambiente OPENAI_API_KEY...")
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("   ❌ OPENAI_API_KEY NÃO configurada")
    print("\n   Configure com:")
    print("   Windows (PowerShell): $env:OPENAI_API_KEY='sk-proj-...'")
    print("   Linux/Mac: export OPENAI_API_KEY='sk-proj-...'")
    sys.exit(1)

print(f"   ✅ OPENAI_API_KEY configurada")
print(f"   Chave: {api_key[:15]}...{api_key[-4:]} (oculta por segurança)")

# 3. Verificar formato da chave
print("\n3️⃣  Verificando formato da chave...")
if api_key.startswith("sk-"):
    print("   ✅ Formato correto (começa com sk-)")
else:
    print("   ⚠️  ATENÇÃO: Chave não começa com 'sk-'")
    print("   Chaves da OpenAI normalmente começam com 'sk-proj-' ou 'sk-'")

# 4. Testar conexão com a API
print("\n4️⃣  Testando conexão com a API OpenAI...")
try:
    client = OpenAI()
    
    print("   Enviando requisição de teste...")
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "user", "content": "Responda apenas: OK"}
        ],
        max_tokens=10
    )
    
    resposta = response.choices[0].message.content
    print(f"   ✅ Conexão bem-sucedida!")
    print(f"   Resposta da API: {resposta}")
    
except Exception as e:
    erro = str(e)
    print(f"   ❌ ERRO ao conectar: {erro}")
    
    # Diagnóstico
    print("\n" + "=" * 80)
    print("📋 DIAGNÓSTICO DO ERRO:")
    print("=" * 80)
    
    if "authentication" in erro.lower() or "api key" in erro.lower() or "401" in erro:
        print("\n❌ PROBLEMA: Chave de API inválida")
        print("\nSOLUÇÕES:")
        print("1. Verifique se você copiou a chave completa")
        print("2. Crie uma nova chave em: https://platform.openai.com/api-keys")
        print("3. Configure novamente a variável de ambiente")
        
    elif "insufficient_quota" in erro.lower() or "quota" in erro.lower() or "429" in erro:
        print("\n❌ PROBLEMA: Sem créditos na conta")
        print("\nSOLUÇÕES:")
        print("1. Adicione créditos em: https://platform.openai.com/account/billing")
        print("2. Adicione um método de pagamento")
        print("3. Verifique se você tem saldo disponível")
        
    elif "rate_limit" in erro.lower():
        print("\n⚠️  PROBLEMA: Muitas requisições")
        print("\nSOLUÇÕES:")
        print("1. Aguarde alguns minutos")
        print("2. Use o modo --teste para fazer menos requisições")
        
    elif "model" in erro.lower() or "not found" in erro.lower():
        print("\n⚠️  PROBLEMA: Modelo não disponível")
        print("\nSOLUÇÕES:")
        print("1. Verifique se você tem acesso ao modelo gpt-4.1-mini")
        print("2. Tente usar outro modelo (ex: gpt-3.5-turbo)")
        
    else:
        print(f"\n❓ ERRO DESCONHECIDO:")
        print(f"   {erro}")
        print("\nVerifique:")
        print("1. Sua conexão com a internet")
        print("2. Se a OpenAI está funcionando: https://status.openai.com/")
    
    print("=" * 80)
    sys.exit(1)

# 5. Resumo final
print("\n" + "=" * 80)
print("✅ TUDO CERTO! Você pode usar o script principal agora:")
print("=" * 80)
print("\nComandos:")
print("  python analyze_metadata_with_llm.py --teste    # Teste (10 tabelas)")
print("  python analyze_metadata_with_llm.py -n 35      # Completo (35 tabelas)")
print("=" * 80)
