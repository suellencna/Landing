# 🔍 Debug: Problema com Envio de E-mail

## ✅ Checklist de Verificação

### 1. Variáveis de Ambiente no Railway

Verifique se TODAS estas variáveis estão configuradas no Railway:

- [ ] `SMTP_SERVER` = `smtp.gmail.com`
- [ ] `SMTP_PORT` = `587`
- [ ] `SMTP_USER` = `investir.realizar@gmail.com`
- [ ] `SMTP_PASSWORD` = `nova_senha_de_app` (sem espaços!)
- [ ] `OWNER_EMAIL` = `investir.realizar@gmail.com`

### 2. Verificar Logs no Railway

1. Acesse: https://railway.app
2. Vá em seu projeto
3. Clique em "Deployments"
4. Clique no deployment mais recente
5. Clique em "View Logs"
6. Procure por erros relacionados a:
   - `SMTP`
   - `email`
   - `smtplib`
   - `authentication`
   - `535` (erro de autenticação)

### 3. Problemas Comuns

#### A) Senha de App Incorreta
- Verifique se a senha está sem espaços
- Verifique se é a senha de APP (não a senha normal do Gmail)
- Certifique-se de que a senha foi criada após revogar a antiga

#### B) Verificação em Duas Etapas Não Ativada
- Gmail requer verificação em duas etapas para senhas de app
- Ative em: https://myaccount.google.com/security

#### C) Porta ou Servidor Incorretos
- Servidor: `smtp.gmail.com`
- Porta: `587` (TLS) ou `465` (SSL)

#### D) E-mail do Remetente
- `SMTP_USER` deve ser o mesmo e-mail da conta Google
- Não pode ser um alias

---

## 🧪 Testar Manualmente

Você pode testar o envio de e-mail fazendo uma requisição de teste:

```bash
curl -X POST https://web-production-4df5e.up.railway.app/api/leads \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Teste",
    "email": "seuemail@teste.com",
    "phone": "(11) 99999-9999",
    "consent": true
  }'
```

Ou use o formulário no site e verifique os logs.

---

## 🔧 Ajustes no Código (Se Necessário)

Se os logs mostrarem erros específicos, podemos ajustar o código.

---

## 📋 Informações para Debug

Me envie:
1. Erros dos logs do Railway
2. Se as variáveis estão configuradas
3. Se a senha de app foi criada corretamente

