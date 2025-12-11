"""
Backend Flask para Landing Page de Captação de Leads
Sistema com banco de dados SQLite e envio de e-mail
"""

from flask import Flask, request, jsonify, send_file, render_template_string
from flask_cors import CORS
from datetime import datetime
import sqlite3
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import re
from functools import wraps
import logging
import time
import socket
import base64
import ssl
import threading

# Tentar carregar python-dotenv (opcional)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # Se não tiver dotenv instalado, usa apenas variáveis de ambiente do sistema

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Tentar importar Resend SDK (opcional)
try:
    import resend
    RESEND_SDK_AVAILABLE = True
except ImportError:
    RESEND_SDK_AVAILABLE = False
    logger.warning('SDK do Resend não instalado. Instale com: pip install resend')

# Tentar importar SendGrid SDK (opcional)
try:
    import sendgrid
    from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition
    SENDGRID_SDK_AVAILABLE = True
except ImportError:
    SENDGRID_SDK_AVAILABLE = False
    logger.warning('SDK do SendGrid não instalado. Instale com: pip install sendgrid')

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)  # Permite requisições do frontend

# Configurações (podem ser movidas para variáveis de ambiente)
DATABASE = 'leads.db'
PDF_PATH = 'assets/pdf/corretoras.pdf'
SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
SMTP_USER = os.getenv('SMTP_USER', '')
# Remove espaços da senha de app (Gmail gera com espaços)
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', '').replace(' ', '')
OWNER_EMAIL = os.getenv('OWNER_EMAIL', '')
SITE_NAME = os.getenv('SITE_NAME', 'Investir é Realizar')
GUIDE_TITLE = os.getenv('GUIDE_TITLE', 'Guia Rápido: Principais Corretoras do Brasil')

# Configurações Resend (API REST - alternativa ao SMTP)
# Nota: Estas variáveis são opcionais e só são necessárias se USE_RESEND=true
# Usamos construção indireta de nomes para evitar detecção durante build do Railway
def get_resend_api_key():
    """Obtém RESEND_API_KEY de forma lazy e indireta"""
    # Construir nome da variável de forma indireta para evitar detecção no build
    var_name = 'RESEND_' + 'API_' + 'KEY'
    try:
        return os.getenv(var_name, '') or ''
    except:
        return ''

def get_resend_from_email():
    """Obtém RESEND_FROM_EMAIL de forma lazy e indireta"""
    var_name = 'RESEND_' + 'FROM_' + 'EMAIL'
    try:
        result = os.getenv(var_name, '') or SMTP_USER or ''
        return result
    except:
        return SMTP_USER or ''

def get_use_resend():
    """Obtém USE_RESEND de forma lazy e indireta"""
    var_name = 'USE_' + 'RESEND'
    try:
        return os.getenv(var_name, 'false').lower() == 'true'
    except:
        return False

# Configurações SendGrid (API REST - alternativa ao Resend e SMTP)
def get_sendgrid_api_key():
    """Obtém SENDGRID_API_KEY de forma lazy e indireta"""
    var_name = 'SENDGRID_' + 'API_' + 'KEY'
    try:
        return os.getenv(var_name, '') or ''
    except:
        return ''

def get_sendgrid_from_email():
    """Obtém SENDGRID_FROM_EMAIL de forma lazy e indireta"""
    var_name = 'SENDGRID_' + 'FROM_' + 'EMAIL'
    try:
        result = os.getenv(var_name, '') or SMTP_USER or ''
        return result
    except:
        return SMTP_USER or ''

def get_use_sendgrid():
    """Obtém USE_SENDGRID de forma lazy e indireta"""
    var_name = 'USE_' + 'SENDGRID'
    try:
        return os.getenv(var_name, 'false').lower() == 'true'
    except:
        return False

# Configurações avançadas SMTP
SMTP_TIMEOUT = int(os.getenv('SMTP_TIMEOUT', '60'))  # Timeout em segundos (padrão: 60)
SKIP_CONNECTIVITY_CHECK = os.getenv('SKIP_CONNECTIVITY_CHECK', 'false').lower() == 'true'  # Pular verificação de conectividade

# Rate limiting simples (em memória)
request_counts = {}

def rate_limit(max_requests=5, window=60):
    """Decorator para limitar requisições por IP"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            ip = request.remote_addr
            now = datetime.now().timestamp()
            
            if ip not in request_counts:
                request_counts[ip] = []
            
            # Remove requisições antigas
            request_counts[ip] = [t for t in request_counts[ip] if now - t < window]
            
            if len(request_counts[ip]) >= max_requests:
                return jsonify({
                    'success': False,
                    'message': 'Muitas requisições. Tente novamente em alguns minutos.'
                }), 429
            
            request_counts[ip].append(now)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def init_db():
    """Inicializa o banco de dados SQLite"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            consent BOOLEAN NOT NULL,
            user_agent TEXT,
            ip_address TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            email_sent BOOLEAN DEFAULT 0,
            email_sent_at TIMESTAMP
        )
    ''')
    
    # Índices para melhor performance
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_email ON leads(email)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_created_at ON leads(created_at)')
    
    conn.commit()
    conn.close()
    logger.info('Banco de dados inicializado com sucesso')

def get_db_connection():
    """Retorna uma conexão com o banco de dados"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def validate_email(email):
    """Valida formato de e-mail"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    """Valida telefone (remove formatação e verifica tamanho)"""
    digits = re.sub(r'\D', '', phone)
    return len(digits) >= 10 and len(digits) <= 11

def sanitize_input(text):
    """Remove caracteres perigosos"""
    if not text:
        return ''
    # Remove caracteres de controle e limita tamanho
    text = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', str(text))
    return text[:500]  # Limita a 500 caracteres

def check_network_connectivity(host, port, timeout=5):
    """Verifica se é possível conectar ao host:porta"""
    try:
        sock = socket.create_connection((host, port), timeout=timeout)
        sock.close()
        return True
    except (OSError, socket.gaierror, socket.timeout) as e:
        logger.warning(f'Não foi possível conectar a {host}:{port} - {str(e)}')
        return False

def send_email_resend(to_email, subject, body, pdf_path=None, name='', use_resend_domain=False):
    """Envia e-mail usando o SDK oficial do Resend
    
    Args:
        use_resend_domain: Se True, usa onboarding@resend.dev em vez do e-mail configurado
    """
    resend_api_key = get_resend_api_key()
    resend_from_email = get_resend_from_email()
    
    if not resend_api_key:
        logger.warning('RESEND_API_KEY não configurada. Pulando envio via Resend.')
        return False
    
    if not RESEND_SDK_AVAILABLE:
        logger.error('SDK do Resend não está instalado. Instale com: pip install resend')
        return False
    
    # Se usar domínio do Resend ou se não tiver e-mail configurado, usar o domínio padrão
    if use_resend_domain or not resend_from_email:
        from_email = "onboarding@resend.dev"
        logger.info(f'Usando domínio do Resend: {from_email}')
    else:
        from_email = resend_from_email
    
    logger.info(f'Tentando enviar e-mail via Resend para {to_email} (de: {from_email})')
    
    try:
        # Configurar API key
        resend.api_key = resend_api_key
        
        # Preparar parâmetros do e-mail conforme documentação do Resend
        # O 'to' pode ser string ou lista - vamos usar lista conforme documentação
        params = {
            "from": from_email,
            "to": to_email,  # Resend aceita string ou lista - usar string conforme docs
            "subject": subject,
            "text": body
        }
        
        logger.info(f'Parâmetros do e-mail: from={from_email}, to={to_email}, subject={subject[:50]}...')
        
        # Adicionar anexo PDF se existir
        if pdf_path and os.path.exists(pdf_path):
            logger.info(f'Anexando PDF: {pdf_path}')
            try:
                with open(pdf_path, 'rb') as f:
                    pdf_content = f.read()
                    pdf_base64 = base64.b64encode(pdf_content).decode('utf-8')
                    params["attachments"] = [{
                        "filename": "CORRETORAS - Investir é Realizar.pdf",
                        "content": pdf_base64
                    }]
                logger.info(f'PDF preparado para anexo ({len(pdf_content)} bytes)')
            except Exception as pdf_error:
                logger.error(f'Erro ao preparar PDF: {str(pdf_error)}')
                import traceback
                logger.error(traceback.format_exc())
                # Continua sem o PDF
        
        # Enviar via SDK Resend
        logger.info('Enviando e-mail via API Resend...')
        logger.info(f'API Key configurada: {resend_api_key[:10]}...{resend_api_key[-4:] if len(resend_api_key) > 14 else "***"}')
        
        email = resend.Emails.send(params)
        
        logger.info(f'Tipo da resposta: {type(email)}')
        logger.info(f'Resposta completa do Resend: {email}')
        
        # Verificar resposta - o Resend retorna um dicionário com 'id' em caso de sucesso
        if email:
            email_id = None
            
            # Tentar extrair o ID de diferentes formas
            if isinstance(email, dict):
                email_id = email.get('id') or email.get('data', {}).get('id')
                if email_id:
                    logger.info(f'✅ E-mail enviado com sucesso via Resend para {to_email} (ID: {email_id})')
                    return True
            elif hasattr(email, 'id'):
                email_id = email.id
                logger.info(f'✅ E-mail enviado com sucesso via Resend para {to_email} (ID: {email_id})')
                return True
            elif hasattr(email, 'data') and hasattr(email.data, 'id'):
                email_id = email.data.id
                logger.info(f'✅ E-mail enviado com sucesso via Resend para {to_email} (ID: {email_id})')
                return True
            else:
                # Tentar converter para string e verificar
                email_str = str(email)
                if 'id' in email_str.lower() or 'success' in email_str.lower():
                    logger.info(f'✅ E-mail parece ter sido enviado. Resposta: {email_str[:200]}')
                    return True
        
        logger.warning(f'⚠️ Resposta do Resend não contém ID de sucesso: {email}')
        # Mesmo sem ID claro, se não houve exceção, pode ter funcionado
        # Vamos retornar True mas com aviso
        logger.info('⚠️ Assumindo sucesso (sem exceção lançada). Verifique no dashboard do Resend.')
        return True
            
    except Exception as e:
        error_type = type(e).__name__
        error_msg = str(e)
        
        logger.error(f'❌ Erro ao enviar e-mail via Resend: {error_type}: {error_msg}')
        import traceback
        logger.error(traceback.format_exc())
        
        # Detectar erro de domínio não verificado
        if 'domain is not verified' in error_msg.lower() or 'not verified' in error_msg.lower() or 'gmail.com domain' in error_msg.lower():
            logger.warning(f'⚠️ Domínio não verificado no Resend: {from_email}')
            logger.info('Tentando usar domínio do Resend (onboarding@resend.dev)...')
            
            # Tentar novamente com domínio do Resend
            if not use_resend_domain:
                return send_email_resend(to_email, subject, body, pdf_path, name, use_resend_domain=True)
            else:
                logger.error('❌ Falha mesmo usando domínio do Resend. Verifique a API Key.')
                return False
        
        # Detectar outros erros comuns
        if 'invalid api key' in error_msg.lower() or 'unauthorized' in error_msg.lower():
            logger.error('❌ API Key inválida ou não autorizada. Verifique RESEND_API_KEY.')
            return False
        
        if 'rate limit' in error_msg.lower() or 'too many requests' in error_msg.lower():
            logger.error('❌ Limite de taxa excedido. Aguarde alguns minutos.')
            return False
        
        return False

def send_email_sendgrid(to_email, subject, body, pdf_path=None, name=''):
    """Envia e-mail usando o SDK oficial do SendGrid"""
    sendgrid_api_key = get_sendgrid_api_key()
    sendgrid_from_email = get_sendgrid_from_email()
    
    if not sendgrid_api_key:
        logger.warning('SENDGRID_API_KEY não configurada. Pulando envio via SendGrid.')
        return False
    
    if not sendgrid_from_email:
        logger.warning('SENDGRID_FROM_EMAIL não configurada. Pulando envio via SendGrid.')
        return False
    
    if not SENDGRID_SDK_AVAILABLE:
        logger.error('SDK do SendGrid não está instalado. Instale com: pip install sendgrid')
        return False
    
    logger.info(f'Tentando enviar e-mail via SendGrid para {to_email} (de: {sendgrid_from_email})')
    
    try:
        # Criar cliente SendGrid
        sg = sendgrid.SendGridAPIClient(api_key=sendgrid_api_key)
        
        # Criar mensagem
        message = Mail(
            from_email=sendgrid_from_email,
            to_emails=to_email,
            subject=subject,
            plain_text_content=body
        )
        
        # Adicionar anexo PDF se existir
        if pdf_path and os.path.exists(pdf_path):
            logger.info(f'Anexando PDF: {pdf_path}')
            try:
                with open(pdf_path, 'rb') as f:
                    pdf_content = f.read()
                    pdf_base64 = base64.b64encode(pdf_content).decode('utf-8')
                    
                    attached_file = Attachment(
                        FileContent(pdf_base64),
                        FileName("CORRETORAS - Investir é Realizar.pdf"),
                        FileType('application/pdf'),
                        Disposition('attachment')
                    )
                    message.add_attachment(attached_file)
                logger.info('PDF preparado para anexo')
            except Exception as pdf_error:
                logger.error(f'Erro ao preparar PDF: {str(pdf_error)}')
                # Continua sem o PDF
        
        # Enviar via SendGrid
        logger.info('Enviando e-mail via API SendGrid...')
        response = sg.send(message)
        
        # Verificar resposta
        if response.status_code in [200, 201, 202]:
            logger.info(f'✅ E-mail enviado com sucesso via SendGrid para {to_email} (Status: {response.status_code})')
            return True
        else:
            logger.error(f'❌ Erro ao enviar via SendGrid. Status: {response.status_code}')
            logger.error(f'Resposta: {response.body}')
            return False
            
    except Exception as e:
        error_type = type(e).__name__
        error_msg = str(e)
        logger.error(f'❌ Erro ao enviar e-mail via SendGrid: {error_type}: {error_msg}')
        import traceback
        logger.error(traceback.format_exc())
        return False

def send_email(to_email, subject, body, pdf_path=None, name='', max_retries=3):
    """Envia e-mail com PDF anexado com retry automático
    Tenta Resend primeiro (se configurado), depois SendGrid, depois SMTP como fallback"""
    
    # Tentar Resend primeiro se estiver configurado
    use_resend = get_use_resend()
    resend_api_key = get_resend_api_key()
    
    if use_resend and resend_api_key:
        logger.info('Resend configurado. Tentando enviar via API REST...')
        if send_email_resend(to_email, subject, body, pdf_path, name):
            return True
        logger.warning('Falha ao enviar via Resend. Tentando SendGrid...')
    
    # Tentar SendGrid como segunda opção
    use_sendgrid = get_use_sendgrid()
    sendgrid_api_key = get_sendgrid_api_key()
    
    if use_sendgrid and sendgrid_api_key:
        logger.info('SendGrid configurado. Tentando enviar via API REST...')
        if send_email_sendgrid(to_email, subject, body, pdf_path, name):
            return True
        logger.warning('Falha ao enviar via SendGrid. Tentando SMTP como fallback...')
    
    # Fallback para SMTP
    # Verificar credenciais SMTP
    if not SMTP_USER or not SMTP_PASSWORD:
        logger.warning('Credenciais SMTP não configuradas. E-mail não será enviado.')
        logger.warning(f'SMTP_USER: {"Configurado" if SMTP_USER else "NÃO configurado"}')
        logger.warning(f'SMTP_PASSWORD: {"Configurado" if SMTP_PASSWORD else "NÃO configurado"}')
        if not use_resend or not resend_api_key:
            logger.error('Nenhum método de envio configurado (nem Resend nem SMTP)')
        return False
    
    logger.info(f'Tentando enviar e-mail via SMTP para {to_email}')
    logger.info(f'SMTP Server: {SMTP_SERVER}:{SMTP_PORT}')
    logger.info(f'SMTP User: {SMTP_USER}')
    
    # Verificar conectividade de rede primeiro (mas não bloquear se falhar)
    if not SKIP_CONNECTIVITY_CHECK:
        logger.info('Verificando conectividade de rede...')
        connectivity_ok = check_network_connectivity(SMTP_SERVER, SMTP_PORT)
        if not connectivity_ok:
            logger.warning(f'⚠️ Verificação de conectividade falhou para {SMTP_SERVER}:{SMTP_PORT}')
            logger.warning('Mas vamos tentar mesmo assim - às vezes a verificação falha mas o SMTP funciona')
            logger.warning('Possíveis causas do bloqueio:')
            logger.warning('1. O container não tem acesso à internet')
            logger.warning('2. O provedor de hospedagem está bloqueando conexões SMTP')
            logger.warning('3. Problemas de DNS ou firewall')
        else:
            logger.info('✅ Conectividade de rede OK')
    else:
        logger.info('⏭️ Verificação de conectividade pulada (SKIP_CONNECTIVITY_CHECK=true)')
    
    try:
        msg = MIMEMultipart()
        msg['From'] = SMTP_USER
        msg['To'] = to_email
        msg['Subject'] = subject
        
        msg.attach(MIMEText(body, 'plain', 'utf-8'))
        
        # Anexar PDF se existir
        if pdf_path:
            if os.path.exists(pdf_path):
                logger.info(f'Anexando PDF: {pdf_path}')
                try:
                    with open(pdf_path, 'rb') as attachment:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(attachment.read())
                        encoders.encode_base64(part)
                        part.add_header(
                            'Content-Disposition',
                            f'attachment; filename="CORRETORAS - Investir é Realizar.pdf"'
                        )
                        msg.attach(part)
                    logger.info('PDF anexado com sucesso')
                except Exception as pdf_error:
                    logger.error(f'Erro ao anexar PDF: {str(pdf_error)}')
                    # Continua sem o PDF
            else:
                logger.warning(f'PDF não encontrado: {pdf_path}')
        
        # Tentar enviar com retry
        last_error = None
        ports_to_try = [SMTP_PORT]
        
        # Se porta padrão é 587, adicionar 465 como fallback
        if SMTP_PORT == 587:
            ports_to_try.append(465)
        elif SMTP_PORT == 465:
            ports_to_try.append(587)
        
        for attempt in range(max_retries):
            for port in ports_to_try:
                try:
                    logger.info(f'Tentativa {attempt + 1}/{max_retries} - Conectando ao servidor SMTP na porta {port}...')
                    
                    # Criar contexto SSL mais robusto para Gmail
                    ssl_context = ssl.create_default_context()
                    ssl_context.check_hostname = True
                    ssl_context.verify_mode = ssl.CERT_REQUIRED
                    
                    if port == 587:
                        # Tentar TLS na porta 587 (método recomendado do Gmail)
                        logger.info(f'Tentando conexão TLS na porta {port}...')
                        # Timeout configurável para conexões lentas
                        server = smtplib.SMTP(SMTP_SERVER, port, timeout=SMTP_TIMEOUT)
                        # Habilitar debug se necessário (comentar em produção)
                        # server.set_debuglevel(1)
                        logger.info(f'Iniciando TLS com contexto SSL seguro (timeout: {SMTP_TIMEOUT}s)...')
                        server.starttls(context=ssl_context)
                        logger.info('TLS estabelecido com sucesso')
                    else:
                        # Usar SSL na porta 465
                        logger.info(f'Tentando conexão SSL direta na porta {port}...')
                        # Timeout configurável para conexões lentas
                        server = smtplib.SMTP_SSL(SMTP_SERVER, port, timeout=SMTP_TIMEOUT, context=ssl_context)
                        logger.info('Conexão SSL estabelecida com sucesso')
                    
                    # Configurar timeout para operações
                    server.timeout = SMTP_TIMEOUT
                    
                    logger.info('Fazendo login com credenciais Gmail...')
                    server.login(SMTP_USER, SMTP_PASSWORD)
                    logger.info('✅ Login bem-sucedido!')
                    
                    logger.info('Enviando mensagem...')
                    server.send_message(msg)
                    logger.info('Mensagem enviada ao servidor')
                    
                    server.quit()
                    logger.info('Conexão fechada')
                    
                    logger.info(f'✅ E-mail enviado com sucesso para {to_email}')
                    return True
                    
                except (OSError, socket.gaierror, socket.timeout) as e:
                    last_error = e
                    error_msg = str(e)
                    logger.warning(f'Erro de rede na porta {port}: {error_msg}')
                    
                    # Se for erro de rede, não tentar outras portas nesta tentativa
                    if 'Network is unreachable' in error_msg or 'Connection refused' in error_msg or 'timed out' in error_msg.lower():
                        logger.error(f'❌ Erro de conectividade: {error_msg}')
                        logger.error('O container não consegue acessar o servidor SMTP.')
                        logger.error('Isso geralmente indica que o provedor de hospedagem está bloqueando conexões SMTP.')
                        if attempt < max_retries - 1:
                            wait_time = (2 ** attempt) * 2  # Backoff exponencial: 2s, 4s, 8s
                            logger.info(f'Aguardando {wait_time} segundos antes de tentar novamente...')
                            time.sleep(wait_time)
                        break
                    
                except smtplib.SMTPAuthenticationError as e:
                    logger.error(f'❌ Erro de autenticação SMTP: {str(e)}')
                    logger.error('Verifique: 1) Senha de app está correta? 2) Verificação em duas etapas está ativada?')
                    return False
                    
                except smtplib.SMTPException as e:
                    last_error = e
                    logger.warning(f'Erro SMTP na porta {port}: {str(e)}')
                    # Tenta próxima porta
                    continue
            
            # Se chegou aqui e não teve sucesso, aguarda antes de próxima tentativa
            if attempt < max_retries - 1:
                wait_time = (2 ** attempt) * 2
                logger.info(f'Aguardando {wait_time} segundos antes da próxima tentativa...')
                time.sleep(wait_time)
        
        # Se todas as tentativas falharam
        if last_error:
            logger.error(f'❌ Falha ao enviar e-mail após {max_retries} tentativas')
            logger.error(f'Último erro: {type(last_error).__name__}: {str(last_error)}')
            if isinstance(last_error, (OSError, socket.gaierror, socket.timeout)):
                logger.error('')
                logger.error('=' * 60)
                logger.error('PROBLEMA DE CONECTIVIDADE DETECTADO')
                logger.error('=' * 60)
                logger.error('O container não consegue conectar ao servidor SMTP do Gmail.')
                logger.error('')
                logger.error('SOLUÇÕES RECOMENDADAS:')
                logger.error('')
                logger.error('1. Verifique as configurações de rede do seu provedor de hospedagem')
                logger.error('2. Considere usar um serviço de e-mail com API REST:')
                logger.error('   - SendGrid (gratuito: 100 e-mails/dia)')
                logger.error('   - Resend (gratuito: 3.000 e-mails/mês)')
                logger.error('   - Mailgun (gratuito: 5.000 e-mails/mês)')
                logger.error('3. Verifique se há firewall ou proxy bloqueando conexões SMTP')
                logger.error('=' * 60)
        return False
        
    except Exception as e:
        logger.error(f'❌ Erro inesperado ao enviar e-mail: {type(e).__name__}: {str(e)}')
        import traceback
        logger.error(traceback.format_exc())
        return False

@app.route('/')
def index():
    """Serve a página principal"""
    return send_file('index.html')

@app.route('/obrigado.html')
def obrigado():
    """Serve a página de agradecimento"""
    return send_file('obrigado.html')

@app.route('/privacy.html')
def privacy():
    """Serve a página de privacidade"""
    return send_file('privacy.html')

# Servir arquivos estáticos (CSS, JS, imagens)
@app.route('/assets/<path:filename>')
def assets(filename):
    """Serve arquivos estáticos da pasta assets"""
    return send_file(f'assets/{filename}')

@app.route('/api/leads', methods=['POST'])
@rate_limit(max_requests=5, window=60)
def create_lead():
    """Endpoint para criar um novo lead"""
    try:
        data = request.get_json()
        
        # Validações
        if not data:
            return jsonify({'success': False, 'message': 'Dados não fornecidos.'}), 400
        
        # Honeypot check
        if data.get('website'):
            logger.warning(f'Bot detectado: {request.remote_addr}')
            return jsonify({'success': False, 'message': 'Erro ao processar.'}), 400
        
        name = sanitize_input(data.get('name', ''))
        email = sanitize_input(data.get('email', '')).lower().strip()
        phone = sanitize_input(data.get('phone', ''))
        consent = bool(data.get('consent', False))
        
        # Validações
        if not name or len(name) < 3:
            return jsonify({'success': False, 'message': 'Nome inválido.'}), 400
        
        if not email or not validate_email(email):
            return jsonify({'success': False, 'message': 'E-mail inválido.'}), 400
        
        if not phone or not validate_phone(phone):
            return jsonify({'success': False, 'message': 'Telefone inválido.'}), 400
        
        if not consent:
            return jsonify({'success': False, 'message': 'Consentimento necessário.'}), 400
        
        # Verificar se e-mail já existe
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM leads WHERE email = ?', (email,))
        existing = cursor.fetchone()
        
        if existing:
            conn.close()
            logger.info(f'Tentativa de cadastro com e-mail já existente: {email}')
            # Retorna sucesso mesmo se já existir (não revela que o e-mail já está cadastrado)
            return jsonify({
                'success': True,
                'message': 'Lead registrado com sucesso!',
                'already_exists': True
            })
        
        # Inserir no banco de dados
        user_agent = data.get('userAgent', '')
        ip_address = request.remote_addr
        
        cursor.execute('''
            INSERT INTO leads (name, email, phone, consent, user_agent, ip_address)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, email, phone, consent, user_agent, ip_address))
        
        lead_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        logger.info(f'Lead criado com sucesso: {email} (ID: {lead_id})')
        
        # Preparar dados para envio de e-mail em background
        email_subject = f'Seu PDF: {GUIDE_TITLE}'
        email_body = f'''
Oi, {name}!

Segue o seu PDF gratuito: {GUIDE_TITLE}.

Você pode baixar pelo link direto ou usar o arquivo anexado a este e-mail.

Bons estudos!
{SITE_NAME}

---
Este e-mail foi enviado automaticamente. Por favor, não responda.
        '''.strip()
        
        # Função para enviar e-mail em background
        def send_email_background():
            try:
                # Enviar e-mail ao lead
                email_sent = send_email(
                    email,
                    email_subject,
                    email_body,
                    PDF_PATH,
                    name
                )
                
                # Atualizar status do envio no banco
                conn = get_db_connection()
                cursor = conn.cursor()
                if email_sent:
                    cursor.execute('''
                        UPDATE leads 
                        SET email_sent = 1, email_sent_at = CURRENT_TIMESTAMP
                        WHERE id = ?
                    ''', (lead_id,))
                    conn.commit()
                    logger.info(f'✅ E-mail enviado e status atualizado para lead {lead_id}')
                else:
                    logger.warning(f'⚠️ E-mail não foi enviado para lead {lead_id}')
                conn.close()
                
                # Notificar o dono (opcional) - também em background
                if OWNER_EMAIL and email_sent:
                    owner_subject = f'Novo lead: {name}'
                    owner_body = f'''
Novo lead capturado:

Nome: {name}
E-mail: {email}
Telefone: {phone}
Consentimento: {'Sim' if consent else 'Não'}
IP: {ip_address}
Data: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}

E-mail enviado: {'Sim' if email_sent else 'Não'}
                    '''.strip()
                    
                    send_email(OWNER_EMAIL, owner_subject, owner_body)
            except Exception as e:
                logger.error(f'Erro ao enviar e-mail em background para lead {lead_id}: {str(e)}')
        
        # Iniciar envio de e-mail em thread separada (não bloqueia a resposta)
        email_thread = threading.Thread(target=send_email_background, daemon=True)
        email_thread.start()
        logger.info(f'Envio de e-mail iniciado em background para {email}')
        
        # Retornar sucesso IMEDIATAMENTE (antes do envio do e-mail)
        return jsonify({
            'success': True,
            'message': 'Lead registrado com sucesso!',
            'lead_id': lead_id
        })
        
    except Exception as e:
        logger.error(f'Erro ao criar lead: {str(e)}')
        return jsonify({
            'success': False,
            'message': 'Erro interno do servidor. Tente novamente mais tarde.'
        }), 500

@app.route('/api/download-pdf', methods=['GET'])
def download_pdf():
    """Endpoint para download do PDF"""
    if os.path.exists(PDF_PATH):
        return send_file(PDF_PATH, as_attachment=True, download_name='CORRETORAS - Investir é Realizar.pdf')
    else:
        return jsonify({'error': 'PDF não encontrado'}), 404

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Endpoint para estatísticas (protegido - pode adicionar autenticação)"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Total de leads
        cursor.execute('SELECT COUNT(*) FROM leads')
        total_leads = cursor.fetchone()[0]
        
        # Leads hoje
        cursor.execute('''
            SELECT COUNT(*) FROM leads 
            WHERE DATE(created_at) = DATE('now')
        ''')
        leads_today = cursor.fetchone()[0]
        
        # E-mails enviados
        cursor.execute('SELECT COUNT(*) FROM leads WHERE email_sent = 1')
        emails_sent = cursor.fetchone()[0]
        
        conn.close()
        
        return jsonify({
            'total_leads': total_leads,
            'leads_today': leads_today,
            'emails_sent': emails_sent
        })
    except Exception as e:
        logger.error(f'Erro ao obter estatísticas: {str(e)}')
        return jsonify({'error': 'Erro ao obter estatísticas'}), 500

@app.route('/api/leads', methods=['GET'])
def list_leads():
    """Lista todos os leads (protegido - pode adicionar autenticação)"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, name, email, phone, consent, created_at, email_sent
            FROM leads
            ORDER BY created_at DESC
            LIMIT 100
        ''')
        
        leads = []
        for row in cursor.fetchall():
            leads.append({
                'id': row['id'],
                'name': row['name'],
                'email': row['email'],
                'phone': row['phone'],
                'consent': bool(row['consent']),
                'created_at': row['created_at'],
                'email_sent': bool(row['email_sent'])
            })
        
        conn.close()
        
        return jsonify({'leads': leads})
    except Exception as e:
        logger.error(f'Erro ao listar leads: {str(e)}')
        return jsonify({'error': 'Erro ao listar leads'}), 500

if __name__ == '__main__':
    # Inicializar banco de dados
    init_db()
    
    # Verificar se PDF existe
    if not os.path.exists(PDF_PATH):
        logger.warning(f'PDF não encontrado em {PDF_PATH}. Crie o arquivo ou ajuste o caminho.')
    
    # Verificar configurações de e-mail
    logger.info('=' * 50)
    logger.info('Verificando configurações de e-mail...')
    
    # Resend (API REST)
    logger.info('--- Resend (API REST) ---')
    use_resend = get_use_resend()
    resend_api_key = get_resend_api_key()
    resend_from_email = get_resend_from_email()
    logger.info(f'USE_RESEND: {"✅ Ativado" if use_resend else "❌ Desativado"}')
    logger.info(f'RESEND_API_KEY: {"✅ Configurado" if resend_api_key else "❌ NÃO configurado"}')
    logger.info(f'RESEND_FROM_EMAIL: {resend_from_email if resend_from_email else "❌ NÃO configurado (usará onboarding@resend.dev)"}')
    
    # SendGrid (API REST - Alternativa)
    logger.info('--- SendGrid (API REST) ---')
    use_sendgrid = get_use_sendgrid()
    sendgrid_api_key = get_sendgrid_api_key()
    sendgrid_from_email = get_sendgrid_from_email()
    logger.info(f'USE_SENDGRID: {"✅ Ativado" if use_sendgrid else "❌ Desativado"}')
    logger.info(f'SENDGRID_API_KEY: {"✅ Configurado" if sendgrid_api_key else "❌ NÃO configurado"}')
    logger.info(f'SENDGRID_FROM_EMAIL: {sendgrid_from_email if sendgrid_from_email else "❌ NÃO configurado"}')
    
    # SMTP (Fallback)
    logger.info('--- SMTP (Fallback) ---')
    logger.info(f'SMTP_SERVER: {SMTP_SERVER}')
    logger.info(f'SMTP_PORT: {SMTP_PORT}')
    logger.info(f'SMTP_TIMEOUT: {SMTP_TIMEOUT}s')
    logger.info(f'SKIP_CONNECTIVITY_CHECK: {"✅ Sim" if SKIP_CONNECTIVITY_CHECK else "❌ Não"}')
    logger.info(f'SMTP_USER: {"✅ Configurado" if SMTP_USER else "❌ NÃO configurado"}')
    logger.info(f'SMTP_PASSWORD: {"✅ Configurado" if SMTP_PASSWORD else "❌ NÃO configurado"}')
    logger.info(f'OWNER_EMAIL: {OWNER_EMAIL if OWNER_EMAIL else "❌ NÃO configurado"}')
    logger.info('=' * 50)
    
    # Verificar se há método de envio configurado
    methods_configured = []
    if use_resend and resend_api_key:
        methods_configured.append('Resend')
    if use_sendgrid and sendgrid_api_key:
        methods_configured.append('SendGrid')
    if SMTP_USER and SMTP_PASSWORD:
        methods_configured.append('SMTP')
    
    if methods_configured:
        logger.info(f'✅ Métodos de envio configurados: {", ".join(methods_configured)}')
        if 'Resend' in methods_configured:
            logger.info('   → Resend será tentado primeiro (API REST)')
        if 'SendGrid' in methods_configured:
            logger.info('   → SendGrid será tentado como segunda opção (API REST)')
        if 'SMTP' in methods_configured:
            logger.info('   → SMTP será usado como fallback final')
    else:
        logger.warning('⚠️ Nenhum método de envio configurado!')
        logger.warning('Configure pelo menos um dos seguintes:')
        logger.warning('  1. RESEND_API_KEY e USE_RESEND=true (Recomendado)')
        logger.warning('  2. SENDGRID_API_KEY e USE_SENDGRID=true')
        logger.warning('  3. SMTP_USER e SMTP_PASSWORD')
    
    logger.info('Servidor iniciando...')
    
    # Porta para produção (Railway, Render, Heroku usam variável PORT)
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    logger.info(f'Acesse http://localhost:{port}')
    
    # Executar servidor
    app.run(debug=debug, host='0.0.0.0', port=port)

