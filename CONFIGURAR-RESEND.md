# 📧 Configurar Resend (API REST) - Solução para Bloqueio SMTP

## 🎯 Por Que Usar Resend?

Se você está recebendo o erro **"Network is unreachable"** ao tentar enviar e-mails via SMTP, isso significa que seu provedor de hospedagem está **bloqueando conexões SMTP**.

O **Resend** resolve isso usando **API REST** em vez de SMTP, então não depende de conexões de rede bloqueadas.

### ✅ Vantagens do Resend:

- ✅ **Não depende de SMTP** - usa API REST (HTTP/HTTPS)
- ✅ **Gratuito:** 3.000 e-mails/mês
- ✅ **Setup rápido:** 5 minutos
- ✅ **Mais confiável:** não é bloqueado por firewalls
- ✅ **API simples:** fácil de usar

## 📋 Passo a Passo

### 1. Criar Conta no Resend

1. Acesse: https://resend.com
2. Clique em **"Sign Up"** (gratuito)
3. Crie sua conta (pode usar Google/GitHub)

### 2. Verificar Domínio (Opcional - Recomendado)

Para enviar de seu próprio domínio:

1. No dashboard do Resend, vá em **"Domains"**
2. Clique em **"Add Domain"**
3. Adicione seu domínio (ex: `investirerealizar.com`)
4. Siga as instruções para adicionar os registros DNS

**Nota:** Se não tiver domínio próprio, você pode usar o domínio do Resend temporariamente.

### 3. Obter API Key

1. No dashboard do Resend, vá em **"API Keys"**
2. Clique em **"Create API Key"**
3. Dê um nome (ex: "Landing Page")
4. **Copie a API Key** (você só verá ela uma vez!)

### 4. Configurar Variáveis de Ambiente

No seu provedor de hospedagem (Railway, Render, etc.), adicione estas variáveis:

#### Variáveis Obrigatórias:

```
RESEND_API_KEY=re_xxxxxxxxxxxxxxxxxxxxx
USE_RESEND=true
RESEND_FROM_EMAIL=investir.realizar@gmail.com
```

#### Variáveis Opcionais (já existentes):

```
OWNER_EMAIL=investir.realizar@gmail.com
SITE_NAME=Investir é Realizar
GUIDE_TITLE=Guia Rápido: Principais Corretoras do Brasil
```

### 5. E-mail do Remetente

O `RESEND_FROM_EMAIL` deve ser:

- ✅ Um e-mail verificado no Resend, OU
- ✅ Um domínio verificado no Resend (ex: `noreply@investirerealizar.com`)

**Se usar Gmail:**
- Você pode usar `investir.realizar@gmail.com` se verificar esse e-mail no Resend
- Ou use um domínio próprio se tiver

## 🔄 Como Funciona

O sistema agora tenta enviar e-mails nesta ordem:

1. **Primeiro:** Tenta Resend (API REST) - se `USE_RESEND=true` e `RESEND_API_KEY` configurado
2. **Fallback:** Tenta SMTP - se Resend falhar ou não estiver configurado

Isso garante que mesmo se o Resend tiver problemas, o SMTP ainda funciona como backup.

## ✅ Verificar se Funcionou

Após configurar e fazer deploy:

1. **Verifique os logs** ao iniciar o servidor:
   ```
   INFO: --- Resend (API REST) ---
   INFO: USE_RESEND: ✅ Ativado
   INFO: RESEND_API_KEY: ✅ Configurado
   INFO: ✅ Resend configurado - usando API REST para envio de e-mails
   ```

2. **Teste o formulário** na landing page

3. **Verifique os logs** ao enviar:
   ```
   INFO: Resend configurado. Tentando enviar via API REST...
   INFO: Tentando enviar e-mail via Resend para usuario@email.com
   INFO: ✅ E-mail enviado com sucesso via Resend para usuario@email.com
   ```

## 🆘 Problemas Comuns

### Erro: "Invalid API Key"
- Verifique se copiou a API Key completa
- Verifique se não há espaços extras

### Erro: "Domain not verified"
- Verifique se o domínio está verificado no Resend
- Ou use um e-mail verificado no Resend

### Erro: "From email not verified"
- O e-mail em `RESEND_FROM_EMAIL` deve estar verificado no Resend
- Ou deve ser de um domínio verificado

## 📊 Limites do Plano Gratuito

- ✅ **3.000 e-mails/mês** grátis
- ✅ **100 e-mails/dia** grátis
- ✅ Sem limite de anexos
- ✅ Suporte por e-mail

Se precisar de mais, há planos pagos a partir de $20/mês.

## 🔒 Segurança

- ✅ **NUNCA** compartilhe sua API Key
- ✅ **NUNCA** faça commit da API Key no Git
- ✅ Use variáveis de ambiente no provedor de hospedagem
- ✅ Revogue API Keys antigas se suspeitar de vazamento

## 📝 Exemplo de Configuração Completa

No Railway/Render, suas variáveis de ambiente devem ficar assim:

```
# Resend (API REST) - PRINCIPAL
RESEND_API_KEY=re_abc123xyz789...
USE_RESEND=true
RESEND_FROM_EMAIL=investir.realizar@gmail.com

# SMTP (Fallback) - OPCIONAL
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=465
SMTP_USER=investir.realizar@gmail.com
SMTP_PASSWORD=senha_de_app_gmail

# Outras
OWNER_EMAIL=investir.realizar@gmail.com
SITE_NAME=Investir é Realizar
GUIDE_TITLE=Guia Rápido: Principais Corretoras do Brasil
```

## 🎉 Pronto!

Após configurar, faça o deploy e teste. O sistema agora usa Resend (API REST) e não depende mais de SMTP!

---

**Dúvidas?** Consulte a documentação do Resend: https://resend.com/docs

