# 🐘 Como Configurar PostgreSQL no Railway

## ✅ Solução Recomendada: PostgreSQL do Railway

Em vez de usar volumes (que podem não estar disponíveis), vamos usar **PostgreSQL** que o Railway oferece como serviço gerenciado. É mais robusto e os dados nunca são perdidos!

---

## 🚀 Passo a Passo

### 1️⃣ Adicionar Serviço PostgreSQL no Railway

1. No Railway Dashboard, vá para seu projeto
2. Clique no botão **"+ New"** (ou **"+ Novo"**)
3. Selecione **"Database"** → **"Add PostgreSQL"**
4. O Railway vai criar automaticamente um banco PostgreSQL para você

### 2️⃣ Conectar ao Banco

O Railway **automaticamente** cria variáveis de ambiente com as credenciais:

- `DATABASE_URL` - URL completa de conexão
- `PGHOST` - Host do banco
- `PGPORT` - Porta
- `PGUSER` - Usuário
- `PGPASSWORD` - Senha
- `PGDATABASE` - Nome do banco

**Você não precisa fazer nada!** O Railway já configura tudo.

### 3️⃣ Verificar Variáveis

1. No Railway, vá em **"Variables"** (aba ao lado de "Settings")
2. Você deve ver as variáveis do PostgreSQL listadas
3. A mais importante é `DATABASE_URL`

---

## 🔧 O Código Já Está Pronto!

O código que vou criar detecta automaticamente:
- Se `DATABASE_URL` existe → usa PostgreSQL
- Se não existe → usa SQLite (fallback)

**Você só precisa adicionar o serviço PostgreSQL no Railway!**

---

## 📋 Checklist

- [ ] Adicionar serviço PostgreSQL no Railway
- [ ] Verificar se `DATABASE_URL` aparece em "Variables"
- [ ] Aguardar deploy automático
- [ ] Testar criando um novo lead

---

## ✅ Vantagens do PostgreSQL

- ✅ **Dados nunca são perdidos** (mesmo com novos deploys)
- ✅ **Mais robusto** que SQLite
- ✅ **Gerenciado pelo Railway** (backup automático)
- ✅ **Gratuito** no plano básico do Railway
- ✅ **Escalável** para quando crescer

---

**Próximo passo**: Adicione o PostgreSQL no Railway e me avise quando estiver pronto! 🚀



