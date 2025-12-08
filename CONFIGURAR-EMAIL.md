# 📧 Configurar E-mail para Envio Automático

## ⚠️ IMPORTANTE: Senha de App do Gmail

Para o sistema enviar e-mails automaticamente, você precisa criar uma **"Senha de App"** no Gmail.

### Passo a Passo:

1. **Acesse sua conta Google:**
   - Vá para: https://myaccount.google.com/

2. **Ative a Verificação em Duas Etapas:**
   - Se ainda não tiver, ative primeiro em: https://myaccount.google.com/security
   - É obrigatório ter verificação em duas etapas ativada

3. **Crie uma Senha de App:**
   - Acesse: https://myaccount.google.com/apppasswords
   - Selecione "App": Escolha "Outro (Nome personalizado)"
   - Digite: "Landing Page"
   - Clique em "Gerar"
   - **Copie a senha gerada** (16 caracteres, com espaços - você pode remover os espaços)

4. **Configure no arquivo .env:**
   - Abra o arquivo `.env` na raiz do projeto
   - Cole a senha de app no campo `SMTP_PASSWORD`
   - **IMPORTANTE:** Remova os espaços da senha (ex: `abcd efgh ijkl mnop` vira `abcdefghijklmnop`)

### Exemplo de .env configurado:

```
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=investir.realizar@gmail.com
SMTP_PASSWORD=abcdefghijklmnop
OWNER_EMAIL=investir.realizar@gmail.com
```

## ✅ Testar o Envio

Após configurar:

1. Reinicie o servidor (pare e inicie novamente)
2. Preencha o formulário na landing page
3. Verifique se o e-mail foi enviado
4. Verifique a caixa de spam se não chegar

## 🔒 Segurança

- **NUNCA** compartilhe sua senha de app
- **NUNCA** faça commit do arquivo `.env` no Git (já está no .gitignore)
- A senha de app é diferente da sua senha normal do Gmail

## 📝 Limites do Gmail

- Conta pessoal: ~100 e-mails por dia
- Se precisar enviar mais, considere usar um serviço de e-mail profissional

---

**Dúvidas?** Consulte o README.md para mais informações.

