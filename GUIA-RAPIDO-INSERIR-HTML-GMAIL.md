# ⚡ Guia Rápido: Inserir HTML no Gmail

## 🎯 Método Mais Fácil (Recomendado)

### Passo a Passo Visual:

1. **Abra o Gmail** → Clique em **"Escrever"**

2. **Abra o Console do Navegador**:
   - Pressione **`F12`** (ou `Ctrl + Shift + I` no Windows/Linux)
   - Ou `Cmd + Option + I` no Mac

3. **No Console, digite este comando**:
   ```javascript
   document.querySelector('div[contenteditable="true"]').innerHTML = `[COLE SEU HTML AQUI]`
   ```
   
   **OU** use este método mais seguro:
   ```javascript
   const editor = document.querySelector('div[contenteditable="true"]');
   editor.innerHTML = `[COLE SEU HTML AQUI]`;
   ```

4. **Substitua `[COLE SEU HTML AQUI]`** pelo HTML completo (do `<!DOCTYPE html>` até `</html>`)

5. **Pressione Enter** no console

6. **Feche o console** (F12 novamente)

7. **Adicione o PDF como anexo** e envie!

---

## 📋 Exemplo Prático

1. Abra o Gmail e clique em "Escrever"
2. Pressione **F12**
3. Vá na aba **"Console"**
4. Cole este código (substituindo o HTML):

```javascript
document.querySelector('div[contenteditable="true"]').innerHTML = `<!DOCTYPE html>
<html>
<body style="margin: 0; padding: 20px; font-family: Arial, sans-serif;">
    <table width="100%" style="max-width: 600px; margin: 0 auto; background: white;">
        <tr>
            <td style="padding: 30px; background: #667eea; text-align: center;">
                <img src="https://raw.githubusercontent.com/suellencna/Landing/main/LOGO%20-%20sem%20fundo.png" width="200" />
            </td>
        </tr>
        <tr>
            <td style="padding: 30px;">
                <h1>Olá, Suellen Pinto! 👋</h1>
                <p>Obrigado por se cadastrar! Segue o seu PDF gratuito.</p>
                <p><strong>📄 Guia Rápido: Principais Corretoras do Brasil</strong></p>
                <p style="text-align: center;">
                    <a href="https://web-production-4df5e.up.railway.app/api/download-pdf" style="display: inline-block; padding: 14px 32px; background: #667eea; color: white; text-decoration: none; border-radius: 6px;">
                        📥 Baixar PDF Agora
                    </a>
                </p>
                <p>Bons estudos!</p>
                <p><strong>Equipe Investir é Realizar</strong></p>
            </td>
        </tr>
    </table>
</body>
</html>`;
```

5. Pressione **Enter**
6. Feche o console (F12)
7. Adicione o PDF e envie!

---

## 🆘 Se Não Funcionar

### Alternativa 1: Usar o HTML Simplificado
Use o arquivo `TEMPLATE-EMAIL-GMAIL-SIMPLIFICADO.html` que criei - ele é mais compatível!

### Alternativa 2: Criar um Rascunho
1. Crie o e-mail no Gmail
2. Formate manualmente (sem HTML)
3. Salve como rascunho
4. Use esse rascunho como template para os próximos

### Alternativa 3: Usar o Modo de Texto
1. Clique nos três pontos (⋮) no Gmail
2. Selecione "Modo de texto simples"
3. Cole apenas o texto (sem HTML)

---

## 💡 Dica Pro

Depois de criar o primeiro e-mail com HTML:
1. **Envie para você mesmo**
2. **Salve como rascunho** ou **arquive**
3. **Reencaminhe** esse e-mail para os próximos leads
4. **Edite apenas o nome** do destinatário!

---

**Pronto! Agora você consegue inserir HTML no Gmail!** 🚀

