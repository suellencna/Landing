# 🔐 Como Configurar Senha e Chave Secreta

## 📍 Onde Configurar

As variáveis de ambiente são configuradas **no Railway** (onde sua aplicação está hospedada), não no código.

## 🚀 Passo a Passo no Railway

### 1. Acesse o Railway Dashboard

1. Vá para: https://railway.app/
2. Faça login na sua conta
3. Selecione seu projeto (Landing Page)

### 2. Configure as Variáveis de Ambiente

1. No projeto, clique na sua **aplicação/serviço** (geralmente aparece como "web" ou o nome do seu projeto)
2. Vá na aba **"Variables"** (ou "Variáveis" em português)
3. Clique em **"+ New Variable"** (ou "+ Nova Variável")

### 3. Adicione as Duas Variáveis

#### Variável 1: `ADMIN_PASSWORD`
- **Nome da Variável**: `ADMIN_PASSWORD`
- **Valor**: Escolha uma senha segura (ex: `MinhaSenhaSuperSegura2024!`)
- Clique em **"Add"**

#### Variável 2: `FLASK_SECRET_KEY`
- **Nome da Variável**: `FLASK_SECRET_KEY`
- **Valor**: Uma chave aleatória longa (veja como gerar abaixo)
- Clique em **"Add"**

### 4. Aguarde o Redeploy

Após adicionar as variáveis, o Railway **automaticamente faz um redeploy**. Aguarde 2-3 minutos.

---

## 🔑 Como Gerar uma Chave Secreta Segura

### Opção 1: Usando Python (Recomendado)

Abra um terminal e execute:

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Isso vai gerar algo como:
```
xK9mP2qR7vT4wY8zA1bC3dE5fG6hI7jK8lM9nO0pQ1rS2tU3vW4xY5z
```

**Copie essa chave** e use como valor de `FLASK_SECRET_KEY`.

### Opção 2: Usando um Gerador Online

1. Acesse: https://randomkeygen.com/
2. Escolha "CodeIgniter Encryption Keys" ou "Fort Knox Passwords"
3. Copie uma das chaves geradas
4. Use como valor de `FLASK_SECRET_KEY`

### Opção 3: Gerar Manualmente

Use uma string aleatória de pelo menos 32 caracteres, por exemplo:
```
MinhaChaveSecretaSuperSegura2024!@#$%^&*()
```

---

## 📝 Exemplo de Configuração

No Railway, você terá algo assim:

| Nome da Variável | Valor |
|-----------------|-------|
| `ADMIN_PASSWORD` | `MinhaSenha123!` |
| `FLASK_SECRET_KEY` | `xK9mP2qR7vT4wY8zA1bC3dE5fG6hI7jK8lM9nO0pQ1rS2tU3vW4xY5z` |

---

## ✅ Como Testar

1. Aguarde o redeploy (2-3 minutos após adicionar as variáveis)
2. Acesse: `https://web-production-4df5e.up.railway.app/ldir26`
3. Você será redirecionado para a página de login
4. Digite a senha que você configurou em `ADMIN_PASSWORD`
5. Se funcionar, está tudo certo! ✅

---

## ⚠️ Importante

- **NÃO compartilhe** essas senhas/chaves publicamente
- **NÃO commite** essas variáveis no código (elas já estão configuradas para usar variáveis de ambiente)
- **Mude a senha padrão** se ainda não mudou
- A `FLASK_SECRET_KEY` é usada para criptografar as sessões - mantenha-a segura

---

## 🆘 Problemas Comuns

### "Não consigo fazer login"
- Verifique se a variável `ADMIN_PASSWORD` está escrita exatamente como está no Railway
- A senha é **case-sensitive** (diferencia maiúsculas/minúsculas)
- Aguarde o redeploy completo (pode levar alguns minutos)

### "Erro ao acessar a página"
- Verifique se ambas as variáveis foram adicionadas
- Verifique se não há espaços extras no nome ou valor das variáveis
- Verifique os logs do Railway para ver se há erros

---

**Dúvidas?** Verifique os logs do Railway na aba "Deployments" ou "Logs".

