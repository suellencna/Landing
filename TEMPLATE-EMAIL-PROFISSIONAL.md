# 📧 Template de E-mail Profissional

## ✅ O que foi criado

Um template HTML profissional e responsivo que funciona perfeitamente no Gmail, com:

- ✅ Design moderno e profissional
- ✅ Compatível com Gmail (usa tabelas HTML)
- ✅ Responsivo (funciona em mobile)
- ✅ Espaço para logo personalizado
- ✅ Botão de download estilizado
- ✅ Cores da marca (gradiente roxo)
- ✅ Footer profissional

## 🎨 Características do Template

### Design
- **Cores**: Gradiente roxo (#667eea → #764ba2)
- **Layout**: Centralizado, largura máxima 600px
- **Tipografia**: Fontes do sistema (Arial, Roboto, etc.)
- **Espaçamento**: Generoso e bem organizado

### Elementos Incluídos
1. **Header com Logo**: Espaço destacado para logo da marca
2. **Saudação Personalizada**: "Olá, [Nome]! 👋"
3. **Destaque do PDF**: Box destacado com o nome do guia
4. **Botão de Download**: Botão estilizado com gradiente
5. **Mensagem Motivacional**: Texto de incentivo
6. **Footer**: Informações legais e copyright

## 📋 Como Usar

### 1. Acessar a Página de Administração

```
https://web-production-4df5e.up.railway.app/admin
```

### 2. Visualizar o Template

1. Clique no botão **"📧 Ver Template"** ao lado de qualquer lead
2. Um modal abrirá com 3 abas:
   - **👁️ Visualizar**: Preview do e-mail
   - **📝 HTML**: Código HTML para copiar
   - **📄 Texto**: Versão texto simples

### 3. Copiar e Usar no Gmail

#### Opção 1: Usar HTML (Recomendado)

1. Clique na aba **"📝 HTML"**
2. Clique em **"📋 Copiar HTML"**
3. No Gmail:
   - Clique nos três pontos (⋮) no editor
   - Selecione **"Inserir HTML"**
   - Cole o HTML copiado
   - Adicione o PDF como anexo
   - Envie

#### Opção 2: Usar Texto Simples

1. Clique na aba **"📄 Texto"**
2. Clique em **"📋 Copiar Texto"**
3. Cole diretamente no Gmail

## 🖼️ Personalizar o Logo

O template atualmente mostra o texto "💰 Investir é Realizar" no header.

Para usar seu logo real:

1. Faça upload do logo para um serviço de hospedagem de imagens (ex: Imgur, Cloudinary)
2. Obtenha a URL da imagem
3. No código, substitua a linha do logo por:

```html
<img src="URL_DO_SEU_LOGO_AQUI" alt="Investir é Realizar" style="max-width: 200px; height: auto; display: block;" />
```

**Localização no código:**
- Arquivo: `app.py`
- Função: `generateEmailHTML()`
- Procure por: `<!-- SUBSTITUA ACIMA PELO SEU LOGO`

## 🎨 Personalizar Cores

Para alterar as cores do template:

1. Abra `app.py`
2. Procure pela função `generateEmailHTML()`
3. Altere os valores de cor:
   - `#667eea` e `#764ba2` → Cores do gradiente
   - `#333333` → Cor do texto principal
   - `#666666` → Cor do texto secundário

## 📱 Compatibilidade

O template é compatível com:
- ✅ Gmail (Desktop e Mobile)
- ✅ Outlook
- ✅ Apple Mail
- ✅ Yahoo Mail
- ✅ Outros clientes de e-mail modernos

## 💡 Dicas

1. **Sempre anexe o PDF**: O template menciona que o PDF está anexado
2. **Teste antes**: Envie um e-mail de teste para você mesmo primeiro
3. **Verifique no mobile**: Abra o e-mail no celular para ver como fica
4. **Use o preview**: A aba "Visualizar" mostra exatamente como o e-mail aparecerá

## 🔧 Estrutura do Template

```
┌─────────────────────────────┐
│   Header (Logo/Gradiente)   │
├─────────────────────────────┤
│                             │
│   Saudação Personalizada    │
│   Mensagem Principal        │
│   Destaque do PDF           │
│   Botão de Download         │
│   Mensagem Final            │
│                             │
├─────────────────────────────┤
│   Footer (Legal/Copyright)  │
└─────────────────────────────┘
```

## ✅ Vantagens

- **Profissional**: Design moderno e limpo
- **Responsivo**: Funciona em todos os dispositivos
- **Compatível**: Funciona em todos os clientes de e-mail
- **Personalizável**: Fácil de modificar cores e logo
- **Prático**: Copiar e colar, pronto para usar

O template está pronto para uso! 🚀

