# 🚀 Deploy no Render - Passo a Passo Completo

## ✅ Sim! Você pode usar SOMENTE o Render!

O **Render** suporta aplicações Python/Flask completas, então você pode colocar **tudo** (frontend + backend) em um único lugar.

### ✅ Vantagens do Render:
- ✅ **Plano gratuito disponível**
- ✅ Frontend + Backend juntos
- ✅ Deploy automático do GitHub
- ✅ HTTPS automático
- ✅ Muito fácil de usar

### ⚠️ Limitações do Plano Gratuito:
- ⚠️ Servidor "dorme" após 15 minutos de inatividade
- ⚠️ Primeira requisição pode demorar alguns segundos (spin-up)
- ⚠️ Limite de recursos (suficiente para landing page)

---

## 🎯 Passo 1: Preparar o Repositório GitHub

### 1.1 Criar Repositório

1. Acesse: https://github.com/new
2. Nome: `investir-e-realizar` (ou outro)
3. Marque como **Público** ou **Privado**
4. **NÃO** marque "Add README"
5. Clique em "Create repository"

### 1.2 Fazer Upload dos Arquivos

**Opção A - Via GitHub Web:**
1. No repositório, clique em "uploading an existing file"
2. Arraste todos os arquivos (exceto `.env` e `leads.db`)
3. Faça commit

**Opção B - Via Git:**
```bash
# Na pasta do projeto
git init
git add .
git commit -m "Initial commit - Landing page completa"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/investir-e-realizar.git
git push -u origin main
```

### 1.3 Verificar Arquivos

Certifique-se de ter:
- ✅ `app.py`
- ✅ `requirements.txt`
- ✅ `index.html`, `obrigado.html`, `privacy.html`
- ✅ `assets/` (pasta completa)
- ✅ `.gitignore`

**NÃO deve estar:**
- ❌ `.env`
- ❌ `leads.db`

---

## 🎯 Passo 2: Criar Conta no Render

1. Acesse: https://render.com
2. Clique em "Get Started for Free"
3. Escolha "Sign up with GitHub"
4. Autorize o Render a acessar seus repositórios

---

## 🎯 Passo 3: Criar Web Service

### 3.1 Novo Serviço

1. No dashboard do Render, clique em **"New +"**
2. Selecione **"Web Service"**

### 3.2 Conectar Repositório

1. Selecione seu repositório `investir-e-realizar`
2. Clique em **"Connect"**

### 3.3 Configurar Serviço

Preencha os campos:

- **Name:** `investir-e-realizar` (ou outro nome)
- **Region:** Escolha mais próximo (ex: `Oregon (US West)`)
- **Branch:** `main` (ou `master`)
- **Root Directory:** (deixe vazio)
- **Runtime:** `Python 3`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `python app.py`

### 3.4 Plano

- Selecione **"Free"** (plano gratuito)

### 3.5 Avançar

Clique em **"Advanced"** para configurar variáveis de ambiente

---

## 🎯 Passo 4: Configurar Variáveis de Ambiente

### 4.1 Adicionar Variáveis

Na seção **"Environment Variables"**, clique em **"Add Environment Variable"** e adicione:

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

### 4.2 Porta (Importante!)

O Render define automaticamente a porta via variável `PORT`, mas vamos garantir:

- **PORT** (opcional, Render define automaticamente)
  - Key: `PORT`
  - Value: `10000` (ou deixe Render definir)

---

## 🎯 Passo 5: Criar Web Service

1. Clique em **"Create Web Service"**
2. Render começará o deploy automaticamente
3. Aguarde alguns minutos (primeiro deploy pode demorar 5-10 minutos)

---

## 🎯 Passo 6: Obter URL do Site

1. Após o deploy concluir, você verá:
   - Status: **"Live"** (verde)
   - URL: `https://investir-e-realizar.onrender.com` (ou similar)

2. **Copie essa URL** - essa é a URL do seu site!

---

## 🎯 Passo 7: Testar

1. Acesse a URL do Render
2. Teste o formulário completo
3. Verifique se:
   - ✅ Página carrega corretamente
   - ✅ Formulário funciona
   - ✅ E-mail é enviado
   - ✅ PDF é baixado

---

## 🔧 Ajustes no Código (Já Feito!)

O arquivo `app.py` já está configurado para usar a variável `PORT` do ambiente, então funciona automaticamente no Render! ✅

---

## 📊 Monitoramento

### Ver Logs:
- Render Dashboard > Seu Serviço > Aba **"Logs"**
- Você verá logs em tempo real

### Ver Estatísticas:
- Acesse: `https://seu-site.onrender.com/api/stats`

### Ver Leads:
- Acesse: `https://seu-site.onrender.com/api/leads`

---

## ⚠️ Importante: Servidor "Dorme" no Plano Gratuito

### O que acontece:
- Após **15 minutos de inatividade**, o servidor "dorme"
- A primeira requisição após dormir pode demorar **10-30 segundos** (spin-up)
- Após spin-up, funciona normalmente

### Soluções:

**Opção 1: Aceitar o delay** (recomendado para começar)
- Funciona perfeitamente, só tem delay na primeira requisição
- Para landing page, geralmente é aceitável

**Opção 2: Usar serviço de "keep-alive"**
- Serviços gratuitos que fazem ping no seu site a cada 5-10 minutos
- Exemplos: UptimeRobot, Pingdom (plano gratuito)

**Opção 3: Upgrade para plano pago**
- A partir de $7/mês, servidor não dorme
- Recomendado quando tiver tráfego regular

---

## 🔧 Troubleshooting

### Erro: "Module not found"
- Verifique se `requirements.txt` está correto
- Verifique os logs no Render

### E-mail não envia
- Verifique se todas as variáveis estão configuradas
- Verifique se a senha de app está correta (sem espaços)
- Veja os logs no Render

### Site não carrega
- Verifique os logs no Render
- Certifique-se de que o deploy foi concluído
- Aguarde alguns minutos após criar o serviço

### PDF não baixa
- Verifique se `assets/pdf/corretoras.pdf` está no repositório
- Verifique os logs para erros

### Servidor demora para responder
- Normal no plano gratuito (spin-up)
- Primeira requisição após 15 min de inatividade demora
- Considere usar keep-alive ou upgrade

---

## 💰 Custos

- **Gratuito:** Disponível, mas servidor dorme após 15 min
- **Starter:** $7/mês - Servidor não dorme, mais recursos
- **Standard:** $25/mês - Mais recursos, melhor performance

---

## 🎯 Configurar Domínio Personalizado (Opcional)

1. No Render, vá em **"Settings"** do seu serviço
2. Role até **"Custom Domains"**
3. Clique em **"Add Custom Domain"**
4. Digite seu domínio (ex: `investirerealizar.com.br`)
5. Siga as instruções para configurar DNS

---

## ✅ Pronto!

Sua landing page está online no Render! 🎉

**URL do seu site:** `https://seu-site.onrender.com`

Compartilhe o link e comece a captar leads!

---

## 📝 Resumo Rápido

1. ✅ Criar repositório no GitHub
2. ✅ Fazer upload dos arquivos
3. ✅ Criar conta no Render
4. ✅ Criar Web Service
5. ✅ Configurar variáveis de ambiente
6. ✅ Deploy automático
7. ✅ Testar e compartilhar!

---

**Dúvidas?** Consulte os logs no Render ou me avise!

