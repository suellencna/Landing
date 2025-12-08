"""
Script de teste para verificar conexão SMTP com Gmail
Execute: python test_smtp.py
"""

import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
SMTP_USER = os.getenv('SMTP_USER', '')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', '').replace(' ', '')

print("=" * 50)
print("TESTE DE CONEXÃO SMTP COM GMAIL")
print("=" * 50)
print(f"Servidor: {SMTP_SERVER}")
print(f"Porta: {SMTP_PORT}")
print(f"Usuário: {SMTP_USER}")
print(f"Senha: {'Configurada' if SMTP_PASSWORD else 'NÃO configurada'}")
print("=" * 50)

if not SMTP_USER or not SMTP_PASSWORD:
    print("❌ ERRO: SMTP_USER ou SMTP_PASSWORD não configurados!")
    print("Configure no arquivo .env")
    exit(1)

# Teste 1: Porta 587 com TLS
print("\n[TESTE 1] Tentando porta 587 com TLS...")
try:
    server = smtplib.SMTP(SMTP_SERVER, 587, timeout=30)
    print("✅ Conexão estabelecida na porta 587")
    
    server.starttls()
    print("✅ TLS iniciado")
    
    server.login(SMTP_USER, SMTP_PASSWORD)
    print("✅ Login bem-sucedido!")
    
    # Enviar e-mail de teste
    msg = MIMEMultipart()
    msg['From'] = SMTP_USER
    msg['To'] = SMTP_USER  # Enviar para si mesmo
    msg['Subject'] = 'Teste SMTP - Porta 587'
    msg.attach(MIMEText('Este é um e-mail de teste da porta 587.', 'plain', 'utf-8'))
    
    server.send_message(msg)
    print("✅ E-mail de teste enviado com sucesso!")
    server.quit()
    print("\n✅ TESTE 1: SUCESSO - Porta 587 funciona!")
    
except Exception as e:
    print(f"❌ ERRO na porta 587: {type(e).__name__}: {str(e)}")
    
    # Teste 2: Porta 465 com SSL
    print("\n[TESTE 2] Tentando porta 465 com SSL...")
    try:
        server = smtplib.SMTP_SSL(SMTP_SERVER, 465, timeout=30)
        print("✅ Conexão SSL estabelecida na porta 465")
        
        server.login(SMTP_USER, SMTP_PASSWORD)
        print("✅ Login bem-sucedido!")
        
        # Enviar e-mail de teste
        msg = MIMEMultipart()
        msg['From'] = SMTP_USER
        msg['To'] = SMTP_USER
        msg['Subject'] = 'Teste SMTP - Porta 465'
        msg.attach(MIMEText('Este é um e-mail de teste da porta 465.', 'plain', 'utf-8'))
        
        server.send_message(msg)
        print("✅ E-mail de teste enviado com sucesso!")
        server.quit()
        print("\n✅ TESTE 2: SUCESSO - Porta 465 funciona!")
        
    except Exception as e2:
        print(f"❌ ERRO na porta 465: {type(e2).__name__}: {str(e2)}")
        print("\n❌ AMBOS OS TESTES FALHARAM")
        print("\nPossíveis causas:")
        print("1. Senha de app incorreta")
        print("2. Verificação em duas etapas não ativada")
        print("3. Bloqueio de rede (Railway pode estar bloqueando)")
        print("4. Firewall bloqueando conexões SMTP")
        exit(1)

print("\n" + "=" * 50)
print("TESTE CONCLUÍDO")
print("=" * 50)
print("Verifique sua caixa de entrada para o e-mail de teste!")


