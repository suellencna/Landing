# 🚨 URGENTE: Credenciais SMTP Expostas no GitHub

## ⚠️ Problema Detectado

O GitGuardian detectou que credenciais SMTP foram expostas no seu repositório GitHub.

## 🔧 Ações Imediatas Necessárias

### 1. ROTACIONAR A SENHA DE APP (CRÍTICO!)

**A senha de app do Gmail foi exposta e precisa ser revogada IMEDIATAMENTE:**

1. Acesse: https://myaccount.google.com/apppasswords
2. Encontre a senha de app que você criou
3. Clique em **"Excluir"** ou **"Revogar"**
4. Crie uma **NOVA senha de app**
5. Atualize no Railway com a nova senha

### 2. Verificar o que foi Exposto

Provavelmente o arquivo `.env` foi commitado acidentalmente. Precisamos:
- Remover do histórico do Git
- Garantir que está no `.gitignore`
- Limpar qualquer referência

### 3. Atualizar Variáveis no Railway

Após criar a nova senha de app:
1. Acesse o Railway Dashboard
2. Vá em seu projeto > Variables
3. Atualize `SMTP_PASSWORD` com a nova senha

---

## 🛠️ Como Remover do Histórico do Git

Se o arquivo `.env` foi commitado, precisamos removê-lo do histórico:

### Opção 1: Usar git-filter-repo (Recomendado)

```bash
# Instalar git-filter-repo (se não tiver)
pip install git-filter-repo

# Remover .env do histórico
git filter-repo --path .env --invert-paths --force
```

### Opção 2: Usar BFG Repo-Cleaner

```bash
# Baixar BFG: https://rtyley.github.io/bfg-repo-cleaner/
java -jar bfg.jar --delete-files .env
git reflog expire --expire=now --all
git gc --prune=now --aggressive
```

### Opção 3: Remover Manualmente (Mais Simples)

Se o arquivo foi commitado recentemente:

```bash
# Remover do índice
git rm --cached .env

# Fazer commit
git commit -m "Remover .env do repositório"

# Force push (CUIDADO - isso reescreve o histórico)
git push --force
```

---

## ✅ Verificações de Segurança

### Verificar se .env está no .gitignore:

```bash
cat .gitignore | grep .env
```

Deve mostrar: `.env`

### Verificar se está sendo rastreado:

```bash
git ls-files | grep .env
```

Não deve retornar nada.

### Verificar histórico:

```bash
git log --all --full-history -- .env
```

Se retornar commits, o arquivo foi commitado.

---

## 🔒 Prevenção Futura

1. **SEMPRE verificar antes de commitar:**
   ```bash
   git status
   ```

2. **NUNCA commitar:**
   - `.env`
   - `leads.db`
   - Qualquer arquivo com senhas/credenciais

3. **Usar variáveis de ambiente:**
   - Sempre configurar no serviço (Railway, Render, etc.)
   - Nunca no código ou arquivos versionados

---

## 📋 Checklist de Segurança

- [ ] Revogar senha de app antiga no Gmail
- [ ] Criar nova senha de app
- [ ] Atualizar no Railway
- [ ] Remover .env do histórico do Git (se foi commitado)
- [ ] Verificar que .gitignore está correto
- [ ] Testar envio de e-mail com nova senha
- [ ] Verificar que não há mais credenciais no repositório

---

## ⚠️ IMPORTANTE

**A senha de app exposta está COMPROMETIDA e deve ser revogada IMEDIATAMENTE!**

Mesmo que você remova do Git, se alguém já viu, a senha não é mais segura.

---

**Ação imediata necessária: Revogar a senha de app e criar uma nova!**

