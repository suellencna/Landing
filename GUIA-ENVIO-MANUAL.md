# 📧 Guia: Envio Manual de E-mails pelo Gmail

## 🎯 Como Funciona

O sistema agora permite que você **desabilite o envio automático** e envie os e-mails manualmente pelo Gmail. Isso é útil enquanto você não configura o Resend/SendGrid.

## ⚙️ Configuração

### 1. Desabilitar Envio Automático

No Railway (ou seu provedor), adicione esta variável de ambiente:

```bash
DISABLE_AUTO_EMAIL=true
```

**O que isso faz:**
- ✅ Os leads continuam sendo salvos no banco de dados
- ✅ O sistema NÃO tenta enviar e-mails automaticamente
- ✅ Você pode acessar `/admin` para ver todos os leads
- ✅ Você envia os e-mails manualmente pelo Gmail

### 2. Acessar a Página de Administração

Após fazer deploy, acesse:

```
https://seu-dominio.com/admin
```

Ou se estiver em desenvolvimento local:

```
http://localhost:8080/admin
```

## 📋 Como Usar a Página de Administração

### Visualizar Leads

A página mostra:
- **Total de Leads**: Quantidade total cadastrada
- **E-mails Pendentes**: Leads que ainda não receberam e-mail
- **E-mails Enviados**: Leads que já receberam e-mail

### Filtrar Leads

Use os botões de filtro:
- **Todos**: Mostra todos os leads
- **Pendentes**: Mostra apenas leads que precisam receber e-mail
- **Enviados**: Mostra leads que já receberam e-mail

### Copiar Informações do Lead

1. Clique no botão **"📋 Copiar Info"** ao lado do lead
2. As informações são copiadas para a área de transferência no formato:
   ```
   Para: email@exemplo.com
   Assunto: Seu PDF: Guia Rápido: Principais Corretoras do Brasil
   
   Oi, Nome do Lead!
   
   Segue o seu PDF gratuito: Guia Rápido: Principais Corretoras do Brasil.
   
   ...
   ```

3. Cole no Gmail e envie manualmente

### Marcar E-mail como Enviado

Após enviar o e-mail pelo Gmail:

1. Clique no botão **"✅ Marcar Enviado"** ao lado do lead
2. O status será atualizado para "✅ Enviado"
3. O lead não aparecerá mais na lista de pendentes

## 📝 Processo Completo

### Passo a Passo:

1. **Cliente preenche o formulário** na landing page
2. **Lead é salvo** no banco de dados
3. **Você acessa `/admin`** para ver o novo lead
4. **Clica em "📋 Copiar Info"** para copiar as informações
5. **Abre o Gmail** e cola as informações
6. **Anexa o PDF** (se necessário)
7. **Envia o e-mail** manualmente
8. **Volta para `/admin`** e clica em "✅ Marcar Enviado"

## 🔄 Atualização Automática

A página atualiza automaticamente a cada 30 segundos para mostrar novos leads.

Você também pode clicar em **"🔄 Atualizar"** para atualizar manualmente.

## 📊 Estatísticas

A página mostra estatísticas em tempo real:
- Total de leads cadastrados
- Quantos e-mails estão pendentes
- Quantos e-mails já foram enviados

## 💡 Dicas

1. **Organize por data**: Os leads mais recentes aparecem primeiro
2. **Filtre por pendentes**: Use o filtro "Pendentes" para ver apenas o que precisa de atenção
3. **Marque como enviado**: Sempre marque após enviar para manter o controle
4. **Anexe o PDF**: Lembre-se de anexar o PDF quando enviar pelo Gmail

## 🔒 Segurança

**Importante:** A página `/admin` está **pública** por padrão. Para produção, considere:

1. Adicionar autenticação básica
2. Restringir acesso por IP
3. Adicionar senha simples

## ✅ Vantagens

- ✅ Funciona imediatamente, sem configuração de API
- ✅ Você tem controle total sobre os e-mails
- ✅ Pode personalizar cada e-mail se necessário
- ✅ Não depende de serviços externos
- ✅ Ideal para volumes baixos de leads

## ⚠️ Limitações

- ⚠️ Processo manual (mais trabalhoso)
- ⚠️ Não escala bem para muitos leads
- ⚠️ Requer que você acesse regularmente

## 🚀 Próximos Passos

Quando quiser automatizar novamente:

1. Configure SendGrid ou Resend (com domínio verificado)
2. Remova ou defina `DISABLE_AUTO_EMAIL=false`
3. O sistema voltará a enviar automaticamente

