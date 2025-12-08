# 🚀 Migrar para Render - Solução para SMTP

## ✅ Confirmação: Gmail Funciona!

O teste local confirmou:
- ✅ E-mail de teste foi recebido
- ✅ Credenciais Gmail estão corretas
- ✅ SMTP funciona perfeitamente

**O problema é que o Railway bloqueia conexões SMTP.**

---

## 🎯 Solução: Migrar para Render

**Render geralmente NÃO bloqueia SMTP** e é gratuito!

### ✅ Vantagens do Render:
- ✅ Gratuito para começar
- ✅ Permite conexões SMTP (Gmail funciona)
- ✅ Mesma facilidade que Railway
- ✅ Deploy automático do GitHub
- ✅ Seu código já está pronto!

---

## 📝 Passo a Passo Rápido

### 1. Criar Conta no Render

1. Acesse: https://render.com
2. Clique em "Get Started for Free"
3. Escolha "Sign up with GitHub"
4. Autorize o Render

### 2. Criar Web Service

1. No Render, clique em **"New +"**
2. Selecione **"Web Service"**
3. Conecte seu repositório: **suellencna/Landing**
4. Configure:
   - **Name:** `investir-e-realizar`
   - **Region:** Escolha mais próximo
   - **Branch:** `main`
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python app.py`
   - **Plan:** `Free`

### 3. Configurar Variáveis de Ambiente

Na seção **"Environment Variables"**, adicione:

- `SMTP_SERVER` = `smtp.gmail.com`
- `SMTP_PORT` = `587` (ou `465` se preferir)
- `SMTP_USER` = `investir.realizar@gmail.com`
- `SMTP_PASSWORD` = `sua_senha_de_app` (sem espaços)
- `OWNER_EMAIL` = `investir.realizar@gmail.com`
- `SITE_NAME` = `Investir é Realizar` (opcional)
- `GUIDE_TITLE` = `Guia Rápido: Principais Corretoras do Brasil` (opcional)

### 4. Criar e Aguardar Deploy

1. Clique em **"Create Web Service"**
2. Render fará deploy automaticamente
3. Aguarde alguns minutos
4. Você receberá uma URL tipo: `investir-e-realizar.onrender.com`

### 5. Testar

1. Acesse a URL do Render
2. Preencha o formulário
3. Verifique se o e-mail é enviado!

---

## 🔄 Manter Railway ou Migrar?

Você pode:
- **Manter Railway** para o site (funciona bem)
- **Usar Render** apenas para o backend (se quiser separar)

Ou simplesmente **migrar tudo para Render** (mais simples).

---

## ⚠️ Limitação do Render Gratuito

- Servidor "dorme" após 15 min de inatividade
- Primeira requisição pode demorar 10-30s (spin-up)
- Após isso, funciona normalmente

**Para landing page, geralmente é aceitável!**

---

## ✅ Pronto para Migrar?

Seu código já está pronto! Só precisa:
1. Criar conta no Render
2. Fazer deploy
3. Configurar variáveis
4. Testar!

**Quer que eu te guie passo a passo no Render?**


