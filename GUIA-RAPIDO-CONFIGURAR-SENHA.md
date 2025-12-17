# 🚀 Guia Rápido: Configurar Senha Admin

## ⚡ Resumo Rápido

1. **Acesse o Railway**: https://railway.app/
2. **Selecione seu projeto**
3. **Vá em "Variables"** (aba de variáveis)
4. **Adicione 2 variáveis** (veja abaixo)
5. **Aguarde 2-3 minutos** (redeploy automático)

---

## 📋 Variáveis para Adicionar

### Variável 1: Senha de Acesso

```
Nome: ADMIN_PASSWORD
Valor: [escolha uma senha, ex: MinhaSenha123!]
```

### Variável 2: Chave Secreta (já gerada para você!)

```
Nome: FLASK_SECRET_KEY
Valor: KWWvo1E83MJ7e48ls9V7eSZfbByhaILIuZCNv7Om1y8
```

**Ou gere uma nova** executando no terminal:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

---

## 🎯 Passo a Passo Visual

### 1️⃣ No Railway Dashboard

```
Railway Dashboard
  └─ Seu Projeto (Landing Page)
      └─ [Clique no serviço/aplicação]
          └─ Aba "Variables" (ou "Variáveis")
              └─ Botão "+ New Variable"
```

### 2️⃣ Adicionar Primeira Variável

```
┌─────────────────────────────────────┐
│  New Variable                       │
├─────────────────────────────────────┤
│  Name:  ADMIN_PASSWORD              │
│  Value: MinhaSenha123!             │
│                                     │
│  [Cancel]  [Add]                   │
└─────────────────────────────────────┘
```

### 3️⃣ Adicionar Segunda Variável

```
┌─────────────────────────────────────┐
│  New Variable                       │
├─────────────────────────────────────┤
│  Name:  FLASK_SECRET_KEY            │
│  Value: KWWvo1E83MJ7e48ls9V7eSZfbBy │
│         haILIuZCNv7Om1y8            │
│                                     │
│  [Cancel]  [Add]                   │
└─────────────────────────────────────┘
```

### 4️⃣ Resultado Final

Você deve ter algo assim na lista de variáveis:

```
Variables
├─ ADMIN_PASSWORD      = MinhaSenha123!
├─ FLASK_SECRET_KEY    = KWWvo1E83MJ7e48ls9V7eSZfbByhaILIuZCNv7Om1y8
├─ SMTP_USER          = [sua config existente]
├─ SMTP_PASSWORD       = [sua config existente]
└─ ... (outras variáveis)
```

---

## ✅ Testar

1. Aguarde 2-3 minutos (redeploy automático)
2. Acesse: `https://web-production-4df5e.up.railway.app/ldir26`
3. Digite a senha que você configurou em `ADMIN_PASSWORD`
4. Pronto! 🎉

---

## 💡 Dicas

- **Senha**: Use algo que você consiga lembrar, mas que seja segura
- **Chave Secreta**: Pode usar a que gerei acima, ou gerar uma nova
- **Não compartilhe**: Essas informações são privadas
- **Case-sensitive**: A senha diferencia maiúsculas/minúsculas

---

## 🆘 Não Encontrou a Aba "Variables"?

No Railway, pode aparecer como:
- "Variables"
- "Variáveis" 
- "Environment Variables"
- "Env Vars"
- "Settings" → "Variables"

Procure por qualquer uma dessas opções no menu do seu serviço/aplicação.



