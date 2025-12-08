# 🧪 Guia de Teste

## ✅ Status do Sistema

O servidor está configurado e pronto para testar!

## 🚀 Como Testar

### 1. Iniciar o Servidor

O servidor já está rodando em background. Se precisar reiniciar:

```bash
python app.py
```

Ou simplesmente execute:
```bash
start.bat
```

### 2. Acessar a Landing Page

Abra seu navegador e acesse:
```
http://localhost:5000
```

### 3. Testar o Formulário

1. **Preencha o formulário:**
   - Nome: Teste seu nome
   - E-mail: seuemail@teste.com
   - WhatsApp: (11) 99999-9999
   - Marque o checkbox de consentimento

2. **Clique em "Quero baixar o PDF gratuito"**

3. **Verifique:**
   - ✅ Redirecionamento para página de obrigado
   - ✅ Mensagem de sucesso
   - ✅ Download do PDF (se existir)

### 4. Verificar Banco de Dados

O banco de dados `leads.db` será criado automaticamente.

Para ver os leads cadastrados, acesse:
```
http://localhost:5000/api/leads
```

### 5. Ver Estatísticas

Acesse:
```
http://localhost:5000/api/stats
```

## ⚠️ Observações Importantes

### E-mail não configurado?
- O sistema funcionará normalmente
- Os leads serão salvos no banco de dados
- Mas os e-mails NÃO serão enviados
- Para configurar, edite o arquivo `.env`

### PDF não encontrado?
- O sistema funcionará normalmente
- Mas o download do PDF retornará erro 404
- Adicione seu PDF em: `assets/pdf/corretoras.pdf`

## 📝 Checklist de Teste

- [ ] Servidor iniciou sem erros
- [ ] Página principal carrega corretamente
- [ ] Formulário exibe validações em tempo real
- [ ] Máscara de telefone funciona
- [ ] Submissão do formulário funciona
- [ ] Redirecionamento para obrigado.html
- [ ] Lead foi salvo no banco de dados
- [ ] API de estatísticas funciona
- [ ] API de listagem de leads funciona

## 🔧 Problemas Comuns

### Erro: "Address already in use"
- A porta 5000 já está em uso
- Pare o servidor anterior ou mude a porta no `app.py`

### Erro: "Module not found"
- Execute: `pip install -r requirements.txt`

### Página não carrega
- Verifique se o servidor está rodando
- Verifique o console para erros
- Tente acessar: http://127.0.0.1:5000

## 📊 Próximos Passos Após Teste

1. ✅ Adicionar o PDF em `assets/pdf/corretoras.pdf`
2. ✅ Configurar e-mail no arquivo `.env`
3. ✅ Personalizar links do Instagram
4. ✅ Atualizar e-mail de contato na privacy.html
5. ✅ Testar envio de e-mail real

---

**Boa sorte com os testes! 🎉**

