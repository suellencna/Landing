# 🚀 Como Colocar a Landing Page Online

## 📋 Opções de Deploy

Você tem algumas opções para colocar sua landing page online. Vou explicar as melhores opções:

---

## 🎯 OPÇÃO 1: Railway (Recomendado - Mais Fácil)

**Railway** é uma plataforma que faz deploy automático do seu código Python.

### ✅ Vantagens:
- ✅ Grátis para começar ($5 grátis por mês)
- ✅ Deploy automático do GitHub
- ✅ Suporta Python/Flask
- ✅ Banco de dados incluído
- ✅ HTTPS automático
- ✅ Muito fácil de usar

### 📝 Passo a Passo:

1. **Criar conta no Railway:**
   - Acesse: https://railway.app
   - Faça login com GitHub

2. **Preparar o projeto:**
   - Crie um arquivo `Procfile` na raiz do projeto:
   ```
   web: python app.py
   ```

3. **Criar arquivo `runtime.txt`** (opcional, mas recomendado):
   ```
   python-3.11.0
   ```

4. **Fazer commit no GitHub:**
   - Se ainda não tem, crie um repositório no GitHub
   - Faça commit de todos os arquivos (exceto `.env` e `leads.db`)
   - Push para o GitHub

5. **Deploy no Railway:**
   - No Railway, clique em "New Project"
   - Selecione "Deploy from GitHub repo"
   - Escolha seu repositório
   - Railway detecta automaticamente que é Python

6. **Configurar variáveis de ambiente:**
   - No Railway, vá em "Variables"
   - Adicione todas as variáveis do seu `.env`:
     - `SMTP_SERVER=smtp.gmail.com`
     - `SMTP_PORT=587`
     - `SMTP_USER=investir.realizar@gmail.com`
     - `SMTP_PASSWORD=sua_senha_de_app`
     - `OWNER_EMAIL=investir.realizar@gmail.com`

7. **Configurar domínio:**
   - Railway gera um domínio automático (ex: `seuprojeto.railway.app`)
   - Você pode adicionar um domínio personalizado depois

### 💰 Custo:
- **Gratuito:** $5 grátis por mês (suficiente para começar)
- **Pago:** A partir de $5/mês se precisar de mais recursos

---

## 🎯 OPÇÃO 2: Render (Gratuito com Limitações)

**Render** oferece plano gratuito, mas com algumas limitações.

### ✅ Vantagens:
- ✅ Plano gratuito disponível
- ✅ Deploy automático do GitHub
- ✅ HTTPS automático
- ✅ Fácil de usar

### ⚠️ Limitações do Plano Gratuito:
- ⚠️ Servidor "dorme" após 15 minutos de inatividade
- ⚠️ Primeira requisição pode demorar alguns segundos
- ⚠️ Limite de recursos

### 📝 Passo a Passo:

1. **Criar conta no Render:**
   - Acesse: https://render.com
   - Faça login com GitHub

2. **Criar novo Web Service:**
   - Clique em "New +" > "Web Service"
   - Conecte seu repositório do GitHub
   - Configure:
     - **Name:** investir-e-realizar
     - **Environment:** Python 3
     - **Build Command:** `pip install -r requirements.txt`
     - **Start Command:** `python app.py`

3. **Configurar variáveis de ambiente:**
   - Na seção "Environment Variables"
   - Adicione todas as variáveis do `.env`

4. **Deploy:**
   - Clique em "Create Web Service"
   - Render fará o deploy automaticamente

### 💰 Custo:
- **Gratuito:** Disponível, mas com limitações
- **Pago:** A partir de $7/mês para plano sem limitações

---

## 🎯 OPÇÃO 3: Heroku (Pago, mas Confiável)

**Heroku** é uma das plataformas mais populares, mas não tem mais plano gratuito.

### ✅ Vantagens:
- ✅ Muito confiável
- ✅ Excelente documentação
- ✅ Add-ons disponíveis

### ⚠️ Desvantagens:
- ⚠️ Não tem mais plano gratuito (mínimo $5/mês)

### 📝 Passo a Passo:

1. **Criar conta no Heroku:**
   - Acesse: https://heroku.com
   - Crie uma conta

2. **Instalar Heroku CLI:**
   - Baixe em: https://devcenter.heroku.com/articles/heroku-cli

3. **Login:**
   ```bash
   heroku login
   ```

4. **Criar app:**
   ```bash
   heroku create investir-e-realizar
   ```

5. **Configurar variáveis:**
   ```bash
   heroku config:set SMTP_SERVER=smtp.gmail.com
   heroku config:set SMTP_PORT=587
   heroku config:set SMTP_USER=investir.realizar@gmail.com
   heroku config:set SMTP_PASSWORD=sua_senha_de_app
   heroku config:set OWNER_EMAIL=investir.realizar@gmail.com
   ```

6. **Deploy:**
   ```bash
   git push heroku main
   ```

### 💰 Custo:
- **Mínimo:** $5/mês (Eco Dyno)

---

## 🎯 OPÇÃO 4: GitHub Pages (Só Frontend) + Backend Separado

Se quiser usar GitHub Pages (gratuito) para o frontend e outro serviço para o backend.

### 📝 Passo a Passo:

1. **Frontend no GitHub Pages:**
   - Crie um repositório no GitHub
   - Faça upload dos arquivos HTML, CSS, JS
   - Ative GitHub Pages nas configurações
   - Seu site ficará em: `seuusuario.github.io/seurepo`

2. **Backend separado:**
   - Use Railway, Render ou Heroku para o backend
   - Atualize a URL da API no `script.js`:
   ```javascript
   const API_URL = 'https://seu-backend.railway.app/api';
   ```

### ⚠️ Desvantagem:
- Precisa manter dois serviços separados

---

## 🎯 OPÇÃO 5: VPS (Servidor Próprio)

Se você tem um servidor próprio ou quer mais controle.

### 📝 Passo a Passo:

1. **Contratar VPS:**
   - DigitalOcean, Linode, AWS, etc.
   - Mínimo: 1GB RAM, 1 CPU

2. **Instalar dependências:**
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip nginx
   ```

3. **Configurar aplicação:**
   - Fazer upload dos arquivos
   - Instalar dependências
   - Configurar Nginx como proxy reverso

4. **Usar PM2 ou systemd:**
   - Para manter o servidor rodando

### 💰 Custo:
- **VPS:** A partir de $5-10/mês

---

## 🎯 RECOMENDAÇÃO: Railway

Para começar, recomendo **Railway** porque:
- ✅ É fácil de usar
- ✅ Tem $5 grátis por mês
- ✅ Deploy automático
- ✅ Suporta tudo que você precisa
- ✅ HTTPS automático

---

## 📝 Arquivos Necessários para Deploy

Certifique-se de ter estes arquivos no seu repositório:

- ✅ `app.py` - Backend Flask
- ✅ `requirements.txt` - Dependências
- ✅ `index.html`, `obrigado.html`, `privacy.html` - Páginas
- ✅ `assets/` - CSS, JS, PDF
- ✅ `Procfile` - Para Railway/Heroku
- ✅ `.gitignore` - Para não commitar `.env` e `leads.db`

### ❌ NÃO commitar:
- ❌ `.env` - Variáveis de ambiente (configure no serviço)
- ❌ `leads.db` - Banco de dados (será criado no servidor)

---

## 🔧 Ajustes Necessários no Código

Antes de fazer deploy, você pode precisar ajustar:

1. **Porta do servidor:**
   - Railway/Render/Heroku definem a porta via variável de ambiente
   - Atualize `app.py`:
   ```python
   port = int(os.getenv('PORT', 5000))
   app.run(host='0.0.0.0', port=port)
   ```

2. **CORS (se frontend e backend estiverem separados):**
   - Já está configurado, mas pode precisar ajustar domínios

---

## 🚀 Próximos Passos

1. Escolha uma opção (recomendo Railway)
2. Crie os arquivos necessários (`Procfile`, etc.)
3. Faça commit no GitHub
4. Configure no serviço escolhido
5. Configure variáveis de ambiente
6. Faça deploy
7. Teste tudo!

---

## 📞 Precisa de Ajuda?

Se precisar de ajuda com alguma opção específica, me avise que eu te guio passo a passo!

