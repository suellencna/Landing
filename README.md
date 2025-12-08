# Landing Page - Investir é Realizar

Landing page moderna para captação de leads com download gratuito de PDF sobre corretoras de investimentos.

## 🚀 Funcionalidades

- ✅ Design moderno e responsivo
- ✅ Formulário de captação com validação em tempo real
- ✅ Máscara de telefone automática
- ✅ Banco de dados SQLite para armazenar leads
- ✅ Envio automático de e-mail com PDF anexado
- ✅ Proteção contra spam (honeypot)
- ✅ Rate limiting (limite de requisições)
- ✅ Página de agradecimento com download direto
- ✅ Política de privacidade completa (LGPD)
- ✅ Animações suaves e UX aprimorada

## 📋 Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

## 🛠️ Instalação

1. **Clone ou baixe este repositório**

2. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

3. **Configure as variáveis de ambiente:**

   Crie um arquivo `.env` baseado no `.env.example`:
```bash
cp .env.example .env
```

   Edite o `.env` com suas configurações:
   - **SMTP_USER**: Seu e-mail (ex: seuemail@gmail.com)
   - **SMTP_PASSWORD**: Senha de app do Gmail (veja instruções abaixo)
   - **OWNER_EMAIL**: E-mail para receber notificações de novos leads

   **Para Gmail:**
   - Ative a verificação em duas etapas
   - Crie uma "Senha de App": https://myaccount.google.com/apppasswords
   - Use essa senha no `SMTP_PASSWORD`

4. **Adicione o PDF:**
   - Coloque seu PDF em `assets/pdf/corretoras.pdf`
   - Ou ajuste o caminho no arquivo `app.py` (variável `PDF_PATH`)

5. **Personalize os links:**
   - Edite `index.html` e `privacy.html`
   - Instagram já configurado: https://www.instagram.com/suellenandradepinto/
   - Atualize o e-mail de contato em `privacy.html`

## 🚀 Como Executar

1. **Inicie o servidor backend:**
```bash
python app.py
```

2. **Acesse no navegador:**
```
http://localhost:5000
```

O servidor estará rodando na porta 5000.

## 📁 Estrutura de Arquivos

```
landing-page/
├── app.py                 # Backend Flask
├── requirements.txt       # Dependências Python
├── .env.example          # Exemplo de configuração
├── leads.db              # Banco de dados SQLite (criado automaticamente)
├── index.html            # Página principal
├── obrigado.html         # Página de agradecimento
├── privacy.html          # Política de privacidade
└── assets/
    ├── styles.css        # Estilos CSS
    ├── script.js         # JavaScript do frontend
    └── pdf/
        └── corretoras.pdf # PDF para download
```

## 🔧 Configurações Adicionais

### Alterar Porta do Servidor

Edite `app.py` na última linha:
```python
app.run(debug=True, host='0.0.0.0', port=5000)  # Altere 5000 para a porta desejada
```

### Usar Outro Servidor SMTP

Edite o arquivo `.env`:
- **Outlook/Hotmail**: `SMTP_SERVER=smtp-mail.outlook.com`
- **Yahoo**: `SMTP_SERVER=smtp.mail.yahoo.com`
- **Servidor próprio**: Configure conforme seu provedor

### Ajustar Rate Limiting

No arquivo `app.py`, função `create_lead()`:
```python
@rate_limit(max_requests=5, window=60)  # 5 requisições por 60 segundos
```

## 📊 API Endpoints

### POST `/api/leads`
Cria um novo lead.

**Body:**
```json
{
  "name": "João Silva",
  "email": "joao@exemplo.com",
  "phone": "(11) 99999-9999",
  "consent": true
}
```

### GET `/api/download-pdf`
Faz download do PDF.

### GET `/api/stats`
Retorna estatísticas (total de leads, leads hoje, etc.)

### GET `/api/leads`
Lista todos os leads (últimos 100)

## 🗄️ Banco de Dados

O banco de dados SQLite é criado automaticamente na primeira execução.

**Tabela `leads`:**
- `id`: ID único
- `name`: Nome completo
- `email`: E-mail
- `phone`: Telefone
- `consent`: Consentimento (boolean)
- `user_agent`: User agent do navegador
- `ip_address`: IP do usuário
- `created_at`: Data de criação
- `email_sent`: Se o e-mail foi enviado
- `email_sent_at`: Data de envio do e-mail

## 🔒 Segurança

- ✅ Validação de dados no frontend e backend
- ✅ Sanitização de inputs
- ✅ Honeypot para proteção contra bots
- ✅ Rate limiting por IP
- ✅ CORS configurado
- ✅ Proteção contra SQL injection (usando parâmetros)

## 📝 Próximos Passos

1. **Adicionar reCAPTCHA** (opcional, mas recomendado para produção)
2. **Configurar domínio próprio**
3. **Adicionar analytics** (Google Analytics, Facebook Pixel)
4. **Implementar autenticação** para visualizar leads
5. **Adicionar dashboard** para gerenciar leads
6. **Configurar backup automático** do banco de dados

## 🌐 Deploy

### Opção 1: GitHub Pages (Frontend) + Servidor Próprio (Backend)
- Frontend: GitHub Pages
- Backend: Servidor com Python (Heroku, Railway, Render, etc.)

### Opção 2: Servidor Completo
- Deploy completo em servidor com Python (VPS, Heroku, Railway, etc.)

## 📞 Suporte

Para dúvidas ou problemas, verifique:
1. Logs do servidor (console onde `app.py` está rodando)
2. Banco de dados (`leads.db`)
3. Configurações de e-mail (`.env`)

## 📄 Licença

Este projeto é de uso livre para fins educacionais e comerciais.

---

**Desenvolvido com ❤️ para Investir é Realizar**

