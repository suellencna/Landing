# 🔍 Guia de Debug - E-mail não está sendo enviado

## 📋 Checklist de Verificação

### 1. Verificar Configuração no Railway/Provedor

Certifique-se de que as variáveis de ambiente estão configuradas corretamente:

```bash
RESEND_API_KEY=re_xxxxxxxxxxxxxxxxxxxxx  # ✅ Deve começar com "re_"
USE_RESEND=true                        # ✅ Deve ser exatamente "true" (minúsculo)
```

**Importante:**
- A API Key deve ser copiada COMPLETA do dashboard do Resend
- Não deve ter espaços antes ou depois
- `USE_RESEND` deve ser exatamente `true` (não `True`, `TRUE`, etc.)

### 2. Verificar Logs ao Iniciar o Servidor

Ao iniciar, você deve ver:

```
INFO: ==================================================
INFO: Verificando configurações de e-mail...
INFO: --- Resend (API REST) ---
INFO: USE_RESEND: ✅ Ativado
INFO: RESEND_API_KEY: ✅ Configurado
INFO: RESEND_FROM_EMAIL: ❌ NÃO configurado (usará onboarding@resend.dev)
```

**Se você NÃO vê "✅ Configurado" na RESEND_API_KEY:**
- A variável não está configurada no Railway
- Ou o nome da variável está errado
- Verifique no Railway Dashboard → Variables

### 3. Verificar Logs ao Enviar E-mail

Quando alguém preenche o formulário, você deve ver logs como:

```
INFO: Resend configurado. Tentando enviar via API REST...
INFO: Tentando enviar e-mail via Resend para usuario@email.com (de: onboarding@resend.dev)
INFO: Parâmetros do e-mail: from=onboarding@resend.dev, to=usuario@email.com, subject=...
INFO: Enviando e-mail via API Resend...
INFO: API Key configurada: re_1234567...xyz
INFO: Tipo da resposta: <class 'dict'>
INFO: Resposta completa do Resend: {'id': 'abc123...'}
INFO: ✅ E-mail enviado com sucesso via Resend para usuario@email.com (ID: abc123...)
```

### 4. Problemas Comuns e Soluções

#### ❌ Erro: "RESEND_API_KEY não configurada"

**Causa:** A variável não está configurada no Railway.

**Solução:**
1. Vá no Railway Dashboard
2. Seu Projeto → Variables
3. Adicione: `RESEND_API_KEY` = `sua_api_key_aqui`
4. Adicione: `USE_RESEND` = `true`
5. Aguarde o redeploy (2-3 minutos)

#### ❌ Erro: "SDK do Resend não está instalado"

**Causa:** O pacote `resend` não está instalado.

**Solução:**
1. Verifique se `resend==2.1.0` está no `requirements.txt`
2. Se não estiver, adicione: `resend==2.1.0`
3. Faça commit e push
4. O Railway fará deploy automático

#### ❌ Erro: "Invalid API Key" ou "Unauthorized"

**Causa:** A API Key está incorreta ou foi revogada.

**Solução:**
1. Vá no dashboard do Resend: https://resend.com/api-keys
2. Verifique se a API Key ainda existe
3. Se não existir, crie uma nova
4. Copie a nova API Key COMPLETA
5. Atualize no Railway: `RESEND_API_KEY` = `nova_api_key`
6. Aguarde o redeploy

#### ❌ Erro: "Domain is not verified"

**Causa:** Tentando usar um domínio não verificado (como gmail.com).

**Solução:**
- ✅ **JÁ RESOLVIDO NO CÓDIGO!** O sistema detecta automaticamente e usa `onboarding@resend.dev`
- Se ainda der erro, verifique os logs - deve tentar automaticamente com o domínio do Resend

#### ❌ Erro: "Rate limit exceeded"

**Causa:** Excedeu o limite de e-mails (3.000/mês no plano gratuito).

**Solução:**
1. Verifique no dashboard do Resend quantos e-mails foram enviados
2. Aguarde até o próximo mês OU
3. Faça upgrade do plano

#### ⚠️ Nenhum erro, mas e-mail não chega

**Possíveis causas:**

1. **E-mail na caixa de spam:**
   - Peça para verificar a pasta de spam
   - E-mails de `onboarding@resend.dev` podem ir para spam inicialmente

2. **E-mail inválido:**
   - Verifique se o e-mail do destinatário está correto
   - Teste com seu próprio e-mail primeiro

3. **Resposta do Resend não contém ID:**
   - Verifique os logs - se aparecer "Resposta completa do Resend: ..."
   - O e-mail pode ter sido enviado mesmo sem ID na resposta
   - Verifique no dashboard do Resend: https://resend.com/emails

## 🔬 Debug Avançado

### Verificar se a API Key está sendo lida corretamente

Adicione temporariamente este log no código (remova depois):

```python
logger.info(f'API Key lida: {resend_api_key[:10]}...{resend_api_key[-4:] if len(resend_api_key) > 14 else "***"}')
```

### Verificar resposta completa do Resend

Os logs agora mostram:
- Tipo da resposta
- Resposta completa
- Se contém ID de sucesso

### Verificar no Dashboard do Resend

1. Acesse: https://resend.com/emails
2. Veja se há e-mails enviados
3. Clique em um e-mail para ver detalhes
4. Verifique o status: `sent`, `delivered`, `bounced`, etc.

### Testar API Key diretamente

Você pode testar a API Key usando cURL:

```bash
curl -X POST 'https://api.resend.com/emails' \
  -H 'Authorization: Bearer re_SUA_API_KEY_AQUI' \
  -H 'Content-Type: application/json' \
  -d '{
    "from": "onboarding@resend.dev",
    "to": "seu_email@exemplo.com",
    "subject": "Teste",
    "text": "Este é um teste"
  }'
```

Se funcionar via cURL mas não no código, o problema está na implementação.

## 📊 Verificar Estatísticas

No dashboard do Resend:
- **Emails**: https://resend.com/emails - Veja todos os e-mails enviados
- **API Keys**: https://resend.com/api-keys - Veja uso da API Key
- **Logs**: https://resend.com/logs - Veja logs detalhados

## 🆘 Se Nada Funcionar

1. **Verifique os logs completos** do Railway
2. **Copie TODOS os logs** de quando tenta enviar e-mail
3. **Verifique no dashboard do Resend** se há tentativas de envio
4. **Teste a API Key** diretamente via cURL (veja acima)

## ✅ Checklist Final

- [ ] `RESEND_API_KEY` configurada no Railway
- [ ] `USE_RESEND=true` configurado no Railway
- [ ] `resend==2.1.0` está no `requirements.txt`
- [ ] Logs mostram "✅ Configurado" na inicialização
- [ ] Logs mostram tentativa de envio quando formulário é preenchido
- [ ] Verificou no dashboard do Resend se há e-mails enviados
- [ ] Testou com seu próprio e-mail primeiro
- [ ] Verificou pasta de spam

Se todos os itens estão ✅ mas ainda não funciona, compartilhe os logs completos para análise.

