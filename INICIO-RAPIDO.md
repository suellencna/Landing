# 🚀 Guia Rápido de Início

## Passo 1: Instalar Dependências

Abra o PowerShell ou CMD na pasta do projeto e execute:

```bash
pip install -r requirements.txt
```

Ou simplesmente execute o arquivo `start.bat` (ele instala automaticamente).

## Passo 2: Configurar E-mail

1. Crie um arquivo `.env` na raiz do projeto (copie do `.env.example`)
2. Configure suas credenciais de e-mail:

**Para Gmail:**
- Ative a verificação em duas etapas na sua conta Google
- Acesse: https://myaccount.google.com/apppasswords
- Crie uma "Senha de App"
- Use essa senha no arquivo `.env`

Exemplo de `.env`:
```
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=seuemail@gmail.com
SMTP_PASSWORD=abcd efgh ijkl mnop
OWNER_EMAIL=seuemail@gmail.com
```

## Passo 3: Adicionar o PDF

Coloque seu PDF em:
```
assets/pdf/corretoras.pdf
```

## Passo 4: Personalizar

1. **Instagram**: Edite `index.html` e `privacy.html`
   - Instagram já configurado: https://www.instagram.com/suellenandradepinto/
   - Substitua pelo seu perfil

2. **E-mail de contato**: Edite `privacy.html`
   - Procure por: `seuemail@exemplo.com`
   - Substitua pelo seu e-mail

## Passo 5: Iniciar o Servidor

Execute:
```bash
python app.py
```

Ou simplesmente clique duas vezes em `start.bat`

## Passo 6: Testar

1. Acesse: http://localhost:5000
2. Preencha o formulário
3. Verifique se:
   - O lead foi salvo no banco de dados (`leads.db`)
   - O e-mail foi enviado (verifique spam se não chegar)

## 📊 Ver Estatísticas

Acesse: http://localhost:5000/api/stats

## 📋 Ver Todos os Leads

Acesse: http://localhost:5000/api/leads

## ⚠️ Problemas Comuns

### E-mail não está sendo enviado
- Verifique as credenciais no `.env`
- Para Gmail, use "Senha de App" (não a senha normal)
- Verifique os logs no console

### Erro ao conectar ao servidor
- Certifique-se de que o `app.py` está rodando
- Verifique se a porta 5000 está livre
- Tente mudar a porta no `app.py` (última linha)

### PDF não encontrado
- Verifique se o arquivo está em `assets/pdf/corretoras.pdf`
- Ou ajuste o caminho no `app.py` (variável `PDF_PATH`)

## 🎉 Pronto!

Sua landing page está funcionando! Agora você pode:
- Personalizar ainda mais o design
- Adicionar analytics (Google Analytics, Facebook Pixel)
- Fazer deploy online quando estiver pronto

---

**Dúvidas?** Consulte o `README.md` completo para mais detalhes.

