# 🚀 Deploy no Railway - Passo a Passo Completo

## 📋 Pré-requisitos

- ✅ Conta no GitHub
- ✅ Código da landing page pronto
- ✅ 15 minutos do seu tempo

---

## 🎯 Passo 1: Preparar o Repositório GitHub

### 1.1 Criar Repositório no GitHub

1. Acesse: https://github.com/new
2. Nome do repositório: `investir-e-realizar` (ou outro nome)
3. Marque como **Público** ou **Privado** (sua escolha)
4. **NÃO** marque "Add README" (já temos um)
5. Clique em "Create repository"

### 1.2 Fazer Upload dos Arquivos

**Opção A - Via GitHub Web:**
1. No repositório criado, clique em "uploading an existing file"
2. Arraste todos os arquivos (exceto `.env` e `leads.db`)
3. Faça commit

**Opção B - Via Git (recomendado):**
```bash
# Na pasta do projeto
git init
git add .
git commit -m "Initial commit - Landing page completa"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/investir-e-realizar.git
git push -u origin main
```

### 1.3 Verificar Arquivos no GitHub

Certifique-se de que estes arquivos estão no repositório:
- ✅ `app.py`
- ✅ `requirements.txt`
- ✅ `Procfile`
- ✅ `runtime.txt`
- ✅ `index.html`, `obrigado.html`, `privacy.html`
- ✅ `assets/` (pasta completa)
- ✅ `.gitignore`

**NÃO deve estar:**
- ❌ `.env`
- ❌ `leads.db`

---

## 🎯 Passo 2: Criar Conta no Railway

1. Acesse: https://railway.app
2. Clique em "Start a New Project"
3. Escolha "Login with GitHub"
4. Autorize o Railway a acessar seus repositórios

---

## 🎯 Passo 3: Fazer Deploy

### 3.1 Criar Novo Projeto

1. No Railway, clique em "New Project"
2. Selecione "Deploy from GitHub repo"
3. Escolha seu repositório `investir-e-realizar`
4. Railway detectará automaticamente que é Python

### 3.2 Configurar Build

Railway geralmente detecta automaticamente, mas verifique:
- **Build Command:** (deixe vazio ou `pip install -r requirements.txt`)
- **Start Command:** (deixe vazio, o Procfile cuida disso)

---

## 🎯 Passo 4: Configurar Variáveis de Ambiente

### 4.1 Acessar Variáveis

1. No projeto Railway, clique em "Variables"
2. Clique em "New Variable"

### 4.2 Adicionar Variáveis

Adicione uma por uma:

1. **SMTP_SERVER**
   - Key: `SMTP_SERVER`
   - Value: `smtp.gmail.com`

2. **SMTP_PORT**
   - Key: `SMTP_PORT`
   - Value: `587`

3. **SMTP_USER**
   - Key: `SMTP_USER`
   - Value: `investir.realizar@gmail.com`

4. **SMTP_PASSWORD**
   - Key: `SMTP_PASSWORD`
   - Value: `sua_senha_de_app` (sem espaços)

5. **OWNER_EMAIL**
   - Key: `OWNER_EMAIL`
   - Value: `investir.realizar@gmail.com`

6. **SITE_NAME** (opcional)
   - Key: `SITE_NAME`
   - Value: `Investir é Realizar`

7. **GUIDE_TITLE** (opcional)
   - Key: `GUIDE_TITLE`
   - Value: `Guia Rápido: Principais Corretoras do Brasil`

### 4.3 Salvar

Após adicionar todas, o Railway fará redeploy automaticamente.

---

## 🎯 Passo 5: Obter URL do Site

1. No Railway, vá em "Settings"
2. Role até "Domains"
3. Você verá uma URL como: `investir-e-realizar-production.up.railway.app`
4. **Copie essa URL** - essa é a URL do seu site!

---

## 🎯 Passo 6: Testar

1. Acesse a URL do Railway
2. Teste o formulário
3. Verifique se:
   - ✅ Página carrega corretamente
   - ✅ Formulário funciona
   - ✅ E-mail é enviado
   - ✅ PDF é baixado

---

## 🎯 Passo 7: Configurar Domínio Personalizado (Opcional)

Se quiser usar um domínio próprio (ex: `investirerealizar.com.br`):

1. No Railway, vá em "Settings" > "Domains"
2. Clique em "Custom Domain"
3. Digite seu domínio
4. Siga as instruções para configurar DNS

---

## 🔧 Troubleshooting

### Erro: "Module not found"
- Verifique se `requirements.txt` está correto
- Railway instala automaticamente, mas pode demorar

### E-mail não envia
- Verifique se todas as variáveis de ambiente estão configuradas
- Verifique se a senha de app está correta (sem espaços)
- Veja os logs no Railway (aba "Deployments" > "View Logs")

### Site não carrega
- Verifique os logs no Railway
- Certifique-se de que o deploy foi concluído com sucesso
- Verifique se a porta está configurada corretamente

### PDF não baixa
- Verifique se o arquivo `assets/pdf/corretoras.pdf` está no repositório
- Verifique os logs para erros

---

## 📊 Monitoramento

### Ver Logs:
- Railway > Seu Projeto > "Deployments" > Clique no deployment > "View Logs"

### Ver Estatísticas:
- Acesse: `https://seu-site.railway.app/api/stats`

### Ver Leads:
- Acesse: `https://seu-site.railway.app/api/leads`

---

## 💰 Custos

- **Gratuito:** $5 grátis por mês (suficiente para começar)
- **Pago:** A partir de $5/mês se precisar de mais recursos

---

## ✅ Pronto!

Sua landing page está online! 🎉

Compartilhe o link e comece a captar leads!

---

**Dúvidas?** Consulte o arquivo `DEPLOY.md` para outras opções.

