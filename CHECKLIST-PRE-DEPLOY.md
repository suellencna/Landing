# ✅ Checklist Antes de Fazer Deploy no Railway

## 📋 Verificações Necessárias

### ✅ Arquivos Essenciais (Devem estar no GitHub):

- [x] `app.py` - Backend Flask
- [x] `requirements.txt` - Dependências
- [x] `Procfile` - Para Railway
- [x] `runtime.txt` - Versão do Python
- [x] `index.html` - Página principal
- [x] `obrigado.html` - Página de agradecimento
- [x] `privacy.html` - Política de privacidade
- [x] `assets/styles.css` - Estilos
- [x] `assets/script.js` - JavaScript
- [x] `assets/pdf/corretoras.pdf` - PDF para download
- [x] `.gitignore` - Arquivos ignorados

### ❌ Arquivos que NÃO devem estar no GitHub:

- [ ] `.env` - Variáveis de ambiente (configurar no Railway)
- [ ] `leads.db` - Banco de dados (será criado no servidor)
- [ ] `CORRETORAS - Investir é Realizar.pdf` - PDF original (já copiado para assets/pdf/)

---

## 🔧 Ações Antes de Fazer Commit

### 1. Verificar se leads.db está no .gitignore

O arquivo `leads.db` NÃO deve ser commitado. Verifique se está no `.gitignore`.

### 2. Verificar se .env está no .gitignore

O arquivo `.env` NÃO deve ser commitado. Verifique se está no `.gitignore`.

### 3. Verificar se o PDF está na pasta correta

O PDF deve estar em: `assets/pdf/corretoras.pdf`

### 4. Remover arquivos desnecessários do commit

Se o `leads.db` ou `.env` estiverem sendo rastreados pelo Git, remova:

```bash
git rm --cached leads.db
git rm --cached .env
```

---

## 🚀 Próximos Passos

1. ✅ Verificar checklist acima
2. ✅ Fazer commit dos arquivos corretos
3. ✅ Push para GitHub
4. ✅ Fazer deploy no Railway (seguir DEPLOY-RAILWAY-AGORA.md)

---

## 📝 Comandos Git Úteis

### Ver o que será commitado:
```bash
git status
```

### Adicionar arquivos:
```bash
git add .
```

### Fazer commit:
```bash
git commit -m "Preparar para deploy no Railway"
```

### Push para GitHub:
```bash
git push origin main
```

---

**Tudo verificado? Vamos fazer deploy! 🚀**

