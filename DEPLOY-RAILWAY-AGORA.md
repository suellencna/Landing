# 🚀 Deploy no Railway - Guia Rápido

## ✅ Seu Repositório: https://github.com/suellencna/Landing

---

## 🎯 Passo 1: Verificar Arquivos no GitHub

Antes de fazer deploy, certifique-se de que estes arquivos estão no repositório:

- ✅ `app.py`
- ✅ `requirements.txt`
- ✅ `Procfile`
- ✅ `runtime.txt` (opcional, mas recomendado)
- ✅ `index.html`, `obrigado.html`, `privacy.html`
- ✅ Pasta `assets/` completa
- ✅ `.gitignore`

**NÃO deve estar no GitHub:**
- ❌ `.env` (já está no .gitignore)
- ❌ `leads.db` (já está no .gitignore)

---

## 🎯 Passo 2: Criar Conta no Railway

1. Acesse: **https://railway.app**
2. Clique em **"Start a New Project"**
3. Escolha **"Login with GitHub"**
4. Autorize o Railway a acessar seus repositórios
5. Aceite os termos

---

## 🎯 Passo 3: Criar Novo Projeto

1. No dashboard do Railway, clique em **"New Project"**
2. Selecione **"Deploy from GitHub repo"**
3. Você verá seus repositórios
4. Selecione: **"suellencna/Landing"**
5. Railway detectará automaticamente que é Python

---

## 🎯 Passo 4: Configurar Variáveis de Ambiente

### 4.1 Acessar Variáveis

1. No projeto Railway, clique na aba **"Variables"**
2. Ou clique no serviço e depois em **"Variables"**

### 4.2 Adicionar Variáveis

Clique em **"New Variable"** e adicione uma por uma:

#### 1. SMTP_SERVER
- **Key:** `SMTP_SERVER`
- **Value:** `smtp.gmail.com`
- Clique em **"Add"**

#### 2. SMTP_PORT
- **Key:** `SMTP_PORT`
- **Value:** `587`
- Clique em **"Add"**

#### 3. SMTP_USER
- **Key:** `SMTP_USER`
- **Value:** `investir.realizar@gmail.com`
- Clique em **"Add"**

#### 4. SMTP_PASSWORD
- **Key:** `SMTP_PASSWORD`
- **Value:** `sua_senha_de_app` (sem espaços!)
- Clique em **"Add"**

#### 5. OWNER_EMAIL
- **Key:** `OWNER_EMAIL`
- **Value:** `investir.realizar@gmail.com`
- Clique em **"Add"**

#### 6. SITE_NAME (Opcional)
- **Key:** `SITE_NAME`
- **Value:** `Investir é Realizar`
- Clique em **"Add"**

#### 7. GUIDE_TITLE (Opcional)
- **Key:** `GUIDE_TITLE`
- **Value:** `Guia Rápido: Principais Corretoras do Brasil`
- Clique em **"Add"**

### 4.3 Verificar

Você deve ter 7 variáveis configuradas (ou pelo menos as 5 obrigatórias).

---

## 🎯 Passo 5: Aguardar Deploy

1. Após adicionar as variáveis, o Railway fará **redeploy automático**
2. Você verá os logs do deploy na aba **"Deployments"**
3. Aguarde alguns minutos (primeiro deploy pode demorar 3-5 minutos)
4. Quando aparecer **"Active"** (verde), está pronto!

---

## 🎯 Passo 6: Obter URL do Site

1. No Railway, clique no seu serviço
2. Vá em **"Settings"**
3. Role até **"Domains"**
4. Você verá uma URL tipo: `landing-production-xxxx.up.railway.app`
5. **Copie essa URL** - essa é a URL do seu site!

---

## 🎯 Passo 7: Testar

1. Acesse a URL do Railway no navegador
2. Teste o formulário completo:
   - Preencha nome, e-mail, WhatsApp
   - Marque o checkbox
   - Clique em "Quero baixar o PDF gratuito"
3. Verifique:
   - ✅ Redirecionamento para página de obrigado
   - ✅ Download do PDF
   - ✅ E-mail enviado (verifique sua caixa de entrada)

---

## 🎯 Passo 8: Verificar Estatísticas

Acesse:
- **Estatísticas:** `https://sua-url.railway.app/api/stats`
- **Leads:** `https://sua-url.railway.app/api/leads`

---

## 🔧 Troubleshooting

### Erro: "Module not found"
- Verifique se `requirements.txt` está no repositório
- Verifique os logs no Railway (aba "Deployments" > "View Logs")

### E-mail não envia
- Verifique se todas as variáveis estão configuradas
- Verifique se `SMTP_PASSWORD` está sem espaços
- Veja os logs no Railway

### Site não carrega
- Verifique os logs no Railway
- Certifique-se de que o deploy foi concluído
- Aguarde alguns minutos após criar o serviço

### PDF não baixa
- Verifique se `assets/pdf/corretoras.pdf` está no repositório GitHub
- Verifique os logs para erros

---

## 📊 Monitoramento

### Ver Logs em Tempo Real:
1. Railway Dashboard
2. Seu Projeto > Seu Serviço
3. Aba **"Deployments"**
4. Clique no deployment mais recente
5. Clique em **"View Logs"**

### Ver Métricas:
- Railway mostra uso de CPU, memória, etc.
- Acompanhe na aba **"Metrics"**

---

## 💰 Custos

- **Gratuito:** $5 grátis por mês (suficiente para começar)
- **Pago:** A partir de $5/mês se precisar de mais recursos

---

## ✅ Pronto!

Sua landing page está online no Railway! 🎉

**URL do seu site:** `https://sua-url.railway.app`

Compartilhe o link e comece a captar leads!

---

## 🎯 Próximos Passos (Opcional)

1. **Configurar domínio personalizado:**
   - Railway > Settings > Domains > Custom Domain
   - Siga as instruções para configurar DNS

2. **Monitorar leads:**
   - Acesse `/api/leads` periodicamente
   - Ou crie um dashboard simples

3. **Compartilhar:**
   - Adicione o link no seu Instagram
   - Compartilhe em stories/posts

---

**Dúvidas durante o deploy? Me avise! 🚀**

