# 🗄️ Sobre o Banco de Dados

## 1. ✅ Sim, existe um banco de dados!

O sistema usa **SQLite**, um banco de dados simples e eficiente que armazena tudo em um único arquivo.

**Nome do arquivo**: `leads.db`

---

## 2. 📍 Onde está o banco de dados?

### No Railway (Produção):
O banco está **dentro do container/servidor do Railway**, no diretório raiz do projeto.

**Caminho no servidor**: `/app/leads.db` (ou similar, dependendo da configuração do Railway)

### No seu computador (Desenvolvimento):
Se você rodar localmente, o arquivo `leads.db` será criado na mesma pasta onde está o `app.py`.

**Caminho local**: `C:\Users\Suellen\OneDrive\Área de Trabalho\Python\landing page\leads.db`

---

## 3. ⚠️ Por que os leads antigos sumiram?

### Problema: Banco de dados é recriado a cada deploy

No Railway, quando você faz um novo deploy, o container é **recriado do zero**. Isso significa:

1. ❌ O arquivo `leads.db` **não persiste** entre deploys
2. ❌ Todos os dados são **perdidos** quando há um novo deploy
3. ✅ O banco é **recriado automaticamente** (vazio) na primeira execução

### Por que isso acontece?

- O Railway usa **containers efêmeros** (temporários)
- Cada deploy cria um **novo container limpo**
- Arquivos criados em runtime **não são salvos** automaticamente
- O `leads.db` está no `.gitignore`, então **não é versionado** no Git

---

## 🔧 Soluções

### Opção 1: Usar Volume Persistente no Railway (Recomendado) ✅

1. No Railway, vá em seu projeto
2. Clique no serviço/aplicação
3. Vá em **"Settings"** → **"Volumes"**
4. Clique em **"+ New Volume"**
5. Configure:
   - **Mount Path**: `/data` (ou `/app/data`)
   - **Name**: `database-volume`
6. Atualize o código para salvar o banco no volume:

```python
# No app.py, mude:
DATABASE = '/data/leads.db'  # Em vez de 'leads.db'
```

### Opção 2: Usar Banco de Dados Externo (Melhor para produção) ✅

Migrar para um banco de dados persistente:
- **PostgreSQL** (Railway oferece)
- **MySQL**
- **SQLite em volume persistente**

### Opção 3: Backup Manual (Temporário) ⚠️

Fazer backup do banco antes de cada deploy (não recomendado para produção).

---

## 📊 Estrutura do Banco de Dados

O banco tem uma tabela chamada `leads` com os seguintes campos:

```sql
CREATE TABLE leads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT,
    consent INTEGER DEFAULT 0,
    user_agent TEXT,
    ip_address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    email_sent INTEGER DEFAULT 0,
    email_sent_at TIMESTAMP
);
```

---

## 🔍 Como Verificar se o Banco Existe

### No Railway (via logs):
Os logs mostram quando o banco é criado:
```
INFO:__main__:Banco de dados inicializado com sucesso
```

### Localmente:
Verifique se o arquivo `leads.db` existe na pasta do projeto.

---

## ⚡ Solução Rápida: Configurar Volume no Railway

Vou criar um guia passo a passo para você configurar um volume persistente no Railway, assim os dados não serão perdidos entre deploys.

**Quer que eu implemente isso agora?**

---

## 📝 Resumo

| Pergunta | Resposta |
|----------|----------|
| **Existe banco de dados?** | ✅ Sim, SQLite (`leads.db`) |
| **Onde está?** | No servidor Railway (dentro do container) |
| **Por que sumiram os leads?** | ⚠️ Banco é recriado a cada deploy (sem persistência) |
| **Solução?** | 🔧 Configurar volume persistente no Railway |

---

**Próximo passo**: Configurar volume persistente para que os dados não sejam perdidos! 🚀

