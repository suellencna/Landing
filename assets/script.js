// Configuração da API
// Usa URL relativa para funcionar tanto localmente quanto em produção
const API_URL = window.location.origin + '/api';

// Elementos do formulário
const form = document.getElementById('leadForm');
const submitBtn = document.getElementById('submitBtn');
const errEl = document.getElementById('formError');
const okEl = document.getElementById('formSuccess');

// Máscara de telefone
function maskPhone(value) {
  // Remove tudo que não é número
  value = value.replace(/\D/g, '');
  
  // Aplica a máscara (XX) XXXXX-XXXX ou (XX) XXXX-XXXX
  if (value.length <= 10) {
    value = value.replace(/^(\d{2})(\d{4})(\d{0,4}).*/, '($1) $2-$3');
  } else {
    value = value.replace(/^(\d{2})(\d{5})(\d{0,4}).*/, '($1) $2-$3');
  }
  
  return value;
}

// Aplicar máscara no campo de telefone
const phoneInput = document.getElementById('phone');
if (phoneInput) {
  phoneInput.addEventListener('input', (e) => {
    e.target.value = maskPhone(e.target.value);
  });
  
  phoneInput.addEventListener('blur', (e) => {
    const value = e.target.value.replace(/\D/g, '');
    if (value.length < 10) {
      showFieldError('phoneError', 'Telefone inválido. Digite pelo menos 10 dígitos.');
      phoneInput.classList.add('error');
    } else {
      hideFieldError('phoneError');
      phoneInput.classList.remove('error');
    }
  });
}

// Validação de campos
function validateName(name) {
  if (!name || name.trim().length < 3) {
    return 'Nome deve ter pelo menos 3 caracteres.';
  }
  if (name.trim().length > 100) {
    return 'Nome muito longo.';
  }
  return null;
}

function validateEmail(email) {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!email || !emailRegex.test(email)) {
    return 'E-mail inválido.';
  }
  return null;
}

function validatePhone(phone) {
  const phoneDigits = phone.replace(/\D/g, '');
  if (phoneDigits.length < 10 || phoneDigits.length > 11) {
    return 'Telefone inválido. Use o formato (DDD) 99999-9999.';
  }
  return null;
}

// Funções de exibição de erros
function showFieldError(fieldId, message) {
  const errorEl = document.getElementById(fieldId);
  if (errorEl) {
    errorEl.textContent = message;
    errorEl.classList.add('show');
  }
}

function hideFieldError(fieldId) {
  const errorEl = document.getElementById(fieldId);
  if (errorEl) {
    errorEl.textContent = '';
    errorEl.classList.remove('show');
  }
}

function showError(message) {
  errEl.textContent = message;
  errEl.classList.add('show');
  okEl.classList.remove('show');
  setTimeout(() => {
    errEl.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }, 100);
}

function showSuccess(message) {
  okEl.textContent = message;
  okEl.classList.add('show');
  errEl.classList.remove('show');
}

function hideMessages() {
  errEl.classList.remove('show');
  okEl.classList.remove('show');
  ['nameError', 'emailError', 'phoneError'].forEach(id => hideFieldError(id));
}

function setLoading(state) {
  if (state) {
    submitBtn.disabled = true;
    submitBtn.classList.add('loading');
  } else {
    submitBtn.disabled = false;
    submitBtn.classList.remove('loading');
  }
}

// Validação em tempo real
const nameInput = document.getElementById('name');
const emailInput = document.getElementById('email');

if (nameInput) {
  nameInput.addEventListener('blur', (e) => {
    const error = validateName(e.target.value);
    if (error) {
      showFieldError('nameError', error);
      nameInput.classList.add('error');
    } else {
      hideFieldError('nameError');
      nameInput.classList.remove('error');
    }
  });
}

if (emailInput) {
  emailInput.addEventListener('blur', (e) => {
    const error = validateEmail(e.target.value);
    if (error) {
      showFieldError('emailError', error);
      emailInput.classList.add('error');
    } else {
      hideFieldError('emailError');
      emailInput.classList.remove('error');
    }
  });
}

// Submissão do formulário
form.addEventListener('submit', async (e) => {
  e.preventDefault();
  hideMessages();

  // Limpar erros visuais dos campos
  [nameInput, emailInput, phoneInput].forEach(input => {
    if (input) input.classList.remove('error');
  });

  const data = {
    name: nameInput.value.trim(),
    email: emailInput.value.trim(),
    phone: phoneInput.value.trim(),
    consent: document.getElementById('consent').checked,
    website: document.getElementById('website').value, // honeypot
    userAgent: navigator.userAgent,
    timestamp: new Date().toISOString()
  };

  // Validações
  const nameError = validateName(data.name);
  const emailError = validateEmail(data.email);
  const phoneError = validatePhone(data.phone);

  if (nameError) {
    showFieldError('nameError', nameError);
    nameInput.classList.add('error');
  }
  if (emailError) {
    showFieldError('emailError', emailError);
    emailInput.classList.add('error');
  }
  if (phoneError) {
    showFieldError('phoneError', phoneError);
    phoneInput.classList.add('error');
  }

  if (nameError || emailError || phoneError) {
    showError('Por favor, corrija os erros no formulário.');
    return;
  }

  if (!data.consent) {
    showError('Você precisa aceitar o consentimento para continuar.');
    return;
  }

  // Honeypot check
  if (data.website) {
    showError('Erro inesperado. Tente novamente.');
    return;
  }

  try {
    setLoading(true);
    
    const response = await fetch(`${API_URL}/leads`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });

    const result = await response.json();

    if (response.ok && result.success) {
      showSuccess('Redirecionando...');
      // Redireciona para página de obrigado com parâmetro de download
      setTimeout(() => {
        window.location.href = `obrigado.html?download=1&email=${encodeURIComponent(data.email)}`;
      }, 500);
    } else {
      throw new Error(result.message || 'Falha ao enviar. Tente novamente.');
    }
  } catch (err) {
    console.error('Erro ao enviar formulário:', err);
    
    // Verificar se é erro de conexão
    if (err.message.includes('fetch') || err.message.includes('Failed to fetch')) {
      showError('Não foi possível conectar ao servidor. Verifique se o backend está rodando.');
    } else {
      showError(err.message || 'Não foi possível enviar agora. Tente mais tarde.');
    }
    
    setLoading(false);
  }
});

// Animações suaves ao scroll
const observerOptions = {
  threshold: 0.1,
  rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.style.opacity = '1';
      entry.target.style.transform = 'translateY(0)';
    }
  });
}, observerOptions);

// Observar elementos para animação
document.addEventListener('DOMContentLoaded', () => {
  const animatedElements = document.querySelectorAll('.form-card, .testimonial, .steps li');
  animatedElements.forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(20px)';
    el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(el);
  });
});

