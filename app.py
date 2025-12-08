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

# Tentar carregar python-dotenv (opcional)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # Se não tiver dotenv instalado, usa apenas variáveis de ambiente do sistema

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

def send_email(to_email, subject, body, pdf_path=None, name=''):
    """Envia e-mail com PDF anexado"""
    # Verificar credenciais
    if not SMTP_USER or not SMTP_PASSWORD:
        logger.warning('Credenciais SMTP não configuradas. E-mail não será enviado.')
        logger.warning(f'SMTP_USER: {"Configurado" if SMTP_USER else "NÃO configurado"}')
        logger.warning(f'SMTP_PASSWORD: {"Configurado" if SMTP_PASSWORD else "NÃO configurado"}')
        return False
    
    logger.info(f'Tentando enviar e-mail para {to_email}')
    logger.info(f'SMTP Server: {SMTP_SERVER}:{SMTP_PORT}')
    logger.info(f'SMTP User: {SMTP_USER}')
    
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
        
        # Conectar e enviar
        logger.info('Conectando ao servidor SMTP...')
        
        # Tentar porta 587 com TLS primeiro, se falhar tenta 465 com SSL
        try:
            if SMTP_PORT == 587:
                # Tentar TLS na porta 587
                logger.info(f'Tentando conexão TLS na porta {SMTP_PORT}...')
                server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=30)
                logger.info('Iniciando TLS...')
                server.starttls()
            else:
                # Usar SSL na porta 465
                logger.info(f'Tentando conexão SSL na porta {SMTP_PORT}...')
                server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, timeout=30)
            
            logger.info('Fazendo login...')
            server.login(SMTP_USER, SMTP_PASSWORD)
            logger.info('Login bem-sucedido. Enviando mensagem...')
            server.send_message(msg)
            server.quit()
        except (OSError, smtplib.SMTPException) as e:
            # Se falhar na porta 587, tentar porta 465 com SSL
            if SMTP_PORT == 587:
                logger.warning(f'Falha na porta 587, tentando porta 465 com SSL...')
                try:
                    server = smtplib.SMTP_SSL(SMTP_SERVER, 465, timeout=30)
                    logger.info('Conexão SSL estabelecida. Fazendo login...')
                    server.login(SMTP_USER, SMTP_PASSWORD)
                    logger.info('Login bem-sucedido. Enviando mensagem...')
                    server.send_message(msg)
                    server.quit()
                except Exception as e2:
                    logger.error(f'Erro ao tentar porta 465: {str(e2)}')
                    raise e2
            else:
                raise
        
        logger.info(f'✅ E-mail enviado com sucesso para {to_email}')
        return True
    except smtplib.SMTPAuthenticationError as e:
        logger.error(f'❌ Erro de autenticação SMTP: {str(e)}')
        logger.error('Verifique: 1) Senha de app está correta? 2) Verificação em duas etapas está ativada?')
        return False
    except smtplib.SMTPException as e:
        logger.error(f'❌ Erro SMTP: {str(e)}')
        return False
    except Exception as e:
        logger.error(f'❌ Erro ao enviar e-mail: {type(e).__name__}: {str(e)}')
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
        
        # Preparar e-mail para o lead
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
        
        # Enviar e-mail ao lead
        email_sent = send_email(
            email,
            email_subject,
            email_body,
            PDF_PATH,
            name
        )
        
        # Atualizar status do envio
        if email_sent:
            cursor.execute('''
                UPDATE leads 
                SET email_sent = 1, email_sent_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (lead_id,))
            conn.commit()
        
        # Notificar o dono (opcional)
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
        
        conn.close()
        
        logger.info(f'Lead criado com sucesso: {email} (ID: {lead_id})')
        
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
    logger.info(f'SMTP_SERVER: {SMTP_SERVER}')
    logger.info(f'SMTP_PORT: {SMTP_PORT}')
    logger.info(f'SMTP_USER: {"✅ Configurado" if SMTP_USER else "❌ NÃO configurado"}')
    logger.info(f'SMTP_PASSWORD: {"✅ Configurado" if SMTP_PASSWORD else "❌ NÃO configurado"}')
    logger.info(f'OWNER_EMAIL: {OWNER_EMAIL if OWNER_EMAIL else "❌ NÃO configurado"}')
    logger.info('=' * 50)
    
    if not SMTP_USER or not SMTP_PASSWORD:
        logger.warning('⚠️ SMTP não configurado. E-mails não serão enviados.')
        logger.info('Configure as variáveis de ambiente no Railway: SMTP_USER, SMTP_PASSWORD, OWNER_EMAIL')
    else:
        logger.info('✅ Configurações SMTP encontradas')
    
    logger.info('Servidor iniciando...')
    
    # Porta para produção (Railway, Render, Heroku usam variável PORT)
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    logger.info(f'Acesse http://localhost:{port}')
    
    # Executar servidor
    app.run(debug=debug, host='0.0.0.0', port=port)

