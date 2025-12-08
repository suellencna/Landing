# 🌐 Deploy com GitHub Pages (Frontend) + Backend Separado

## ⚠️ Importante: GitHub Pages Limitação

**GitHub Pages** é **100% gratuito**, mas tem uma limitação importante:

- ✅ **Funciona para:** HTML, CSS, JavaScript (arquivos estáticos)
- ❌ **NÃO funciona para:** Python, Flask, banco de dados, envio de e-mail

### 💡 Solução: Frontend no GitHub Pages + Backend em outro lugar

Você pode usar:
- **GitHub Pages** (gratuito) → Para o frontend (HTML, CSS, JS)
- **Railway/Render** (gratuito/barato) → Para o backend (Python/Flask)

---

## 🎯 Opção 1: GitHub Pages + Railway (Recomendado)

### ✅ Vantagens:
- ✅ **100% gratuito** (GitHub Pages + $5 grátis do Railway)
- ✅ Frontend rápido e confiável
- ✅ Backend separado e escalável

### 📝 Passo a Passo:

#### Parte 1: Frontend no GitHub Pages

1. **Criar repositório para frontend:**
   - Acesse: https://github.com/new
   - Nome: `investir-e-realizar` (ou outro)
   - Marque como **Público** (GitHub Pages precisa ser público no plano gratuito)
   - Crie o repositório

2. **Fazer upload dos arquivos do frontend:**
   - `index.html`
   - `obrigado.html`
   - `privacy.html`
   - Pasta `assets/` completa (CSS, JS, PDF)
   - `.gitignore`

3. **Ativar GitHub Pages:**
   - No repositório, vá em **Settings**
   - Role até **Pages**
   - Em **Source**, selecione: **Deploy from a branch**
   - Branch: `main` (ou `master`)
   - Folder: `/ (root)`
   - Clique em **Save**

4. **Aguardar deploy:**
   - GitHub Pages leva alguns minutos para fazer o deploy
   - Sua URL será: `https://seuusuario.github.io/investir-e-realizar`

#### Parte 2: Backend no Railway

1. **Criar repositório separado para backend:**
   - Crie outro repositório: `investir-e-realizar-backend`
   - Faça upload apenas dos arquivos do backend:
     - `app.py`
     - `requirements.txt`
     - `Procfile`
     - `runtime.txt`
     - `.gitignore`

2. **Deploy no Railway:**
   - Siga o guia `DEPLOY-RAILWAY.md`
   - Configure as variáveis de ambiente
   - Anote a URL do backend (ex: `backend.railway.app`)

#### Parte 3: Conectar Frontend ao Backend

1. **Atualizar `assets/script.js`:**
   - Abra `assets/script.js`
   - Encontre a linha:
   ```javascript
   const API_URL = 'http://localhost:5000/api';
   ```
   - Substitua por:
   ```javascript
   const API_URL = 'https://seu-backend.railway.app/api';
   ```

2. **Atualizar link do PDF:**
   - No `obrigado.html`, atualize:
   ```html
   <a href="/api/download-pdf" download>
   ```
   - Para:
   ```html
   <a href="https://seu-backend.railway.app/api/download-pdf" download>
   ```

3. **Fazer commit e push:**
   ```bash
   git add .
   git commit -m "Conectar frontend ao backend"
   git push
   ```

4. **Pronto!**
   - Frontend: `https://seuusuario.github.io/investir-e-realizar`
   - Backend: `https://seu-backend.railway.app`

---

## 🎯 Opção 2: Tudo no Railway (Mais Simples)

Se preferir simplicidade, coloque tudo no Railway:

- ✅ Frontend e backend juntos
- ✅ Mais fácil de gerenciar
- ✅ Ainda gratuito ($5 grátis/mês)

Siga o guia `DEPLOY-RAILWAY.md` normalmente.

---

## 📊 Comparação

| Aspecto | GitHub Pages + Backend | Tudo no Railway |
|---------|----------------------|-----------------|
| **Custo** | 100% Gratuito | $5 grátis/mês |
| **Complexidade** | Média (2 serviços) | Baixa (1 serviço) |
| **Velocidade Frontend** | Muito rápida | Rápida |
| **Manutenção** | 2 lugares | 1 lugar |
| **Recomendado para** | Quem quer 100% grátis | Quem quer simplicidade |

---

## 🎯 Minha Recomendação

Para começar, recomendo **Tudo no Railway** porque:
- ✅ Mais simples de configurar
- ✅ Mais fácil de manter
- ✅ $5 grátis é suficiente
- ✅ Se precisar escalar, é mais fácil

**GitHub Pages + Backend** é melhor se:
- Você quer 100% gratuito (sem limites)
- Você já tem experiência com múltiplos serviços
- Você quer separar frontend e backend

---

## 🚀 Próximos Passos

1. **Decida qual opção prefere:**
   - Opção 1: GitHub Pages + Railway (2 serviços)
   - Opção 2: Tudo no Railway (1 serviço)

2. **Siga o guia correspondente:**
   - Opção 1: Este arquivo (`DEPLOY-GITHUB-PAGES.md`)
   - Opção 2: `DEPLOY-RAILWAY.md`

3. **Teste tudo antes de compartilhar!**

---

## ❓ Dúvidas?

- **GitHub Pages é gratuito?** Sim, 100% gratuito
- **Preciso de domínio próprio?** Não, GitHub fornece URL grátis
- **Posso usar domínio próprio?** Sim, nas configurações do GitHub Pages
- **GitHub Pages tem limites?** Sim, 1GB de armazenamento e 100GB de bandwidth/mês (suficiente para landing page)

---

**Boa sorte com o deploy! 🚀**

