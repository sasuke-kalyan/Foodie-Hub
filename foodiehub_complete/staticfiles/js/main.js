// ===== DARK MODE =====
const darkToggle = document.getElementById('darkModeToggle');
const root = document.documentElement;

function applyTheme(dark) {
  if (dark) {
    root.setAttribute('data-bs-theme', 'dark');
    document.body.classList.add('dark-mode');
    if (darkToggle) darkToggle.innerHTML = '<i class="fas fa-sun"></i>';
  } else {
    root.setAttribute('data-bs-theme', 'light');
    document.body.classList.remove('dark-mode');
    if (darkToggle) darkToggle.innerHTML = '<i class="fas fa-moon"></i>';
  }
  localStorage.setItem('darkMode', dark ? '1' : '0');
}

const savedDark = localStorage.getItem('darkMode');
applyTheme(savedDark === '1');

if (darkToggle) {
  darkToggle.addEventListener('click', () => {
    const isDark = root.getAttribute('data-bs-theme') === 'dark';
    applyTheme(!isDark);
  });
}

// ===== AUTO DISMISS ALERTS =====
document.addEventListener('DOMContentLoaded', function () {
  setTimeout(() => {
    document.querySelectorAll('.alert').forEach(alert => {
      try { new bootstrap.Alert(alert).close(); } catch(e) {}
    });
  }, 4000);

  // ===== WISHLIST AJAX =====
  document.querySelectorAll('.wishlist-btn').forEach(btn => {
    btn.addEventListener('click', function (e) {
      e.preventDefault();
      fetch(this.href, { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
        .then(r => r.json())
        .then(data => {
          const icon = this.querySelector('i');
          if (data.status === 'added') {
            icon.classList.replace('far', 'fas');
            this.classList.add('btn-danger');
            this.classList.remove('btn-outline-danger');
          } else {
            icon.classList.replace('fas', 'far');
            this.classList.remove('btn-danger');
            this.classList.add('btn-outline-danger');
          }
        });
    });
  });

  // ===== PRINT RECEIPT =====
  const printBtn = document.getElementById('printReceiptBtn');
  if (printBtn) {
    printBtn.addEventListener('click', () => window.print());
  }
});
// ===== VOICE SEARCH =====
// Add this to static/js/main.js (append at bottom)

function initVoiceSearch() {
  const micBtn = document.getElementById('voiceMicBtn');
  const searchInput = document.getElementById('voiceSearchInput');
  if (!micBtn || !searchInput) return;

  if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
    micBtn.style.display = 'none';
    return;
  }

  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  const recognition = new SpeechRecognition();
  recognition.continuous = false;
  recognition.interimResults = true;
  recognition.lang = document.documentElement.lang === 'te' ? 'te-IN' :
                     document.documentElement.lang === 'hi' ? 'hi-IN' : 'en-IN';

  let isListening = false;

  micBtn.addEventListener('click', () => {
    if (isListening) {
      recognition.stop();
      return;
    }
    recognition.start();
    isListening = true;
    micBtn.innerHTML = '<span style="color:#dc3545;font-size:16px;">&#9632;</span>';
    micBtn.title = 'Click to stop';
    searchInput.placeholder = 'Listening...';
  });

  recognition.onresult = (event) => {
    const transcript = Array.from(event.results)
      .map(r => r[0].transcript).join('');
    searchInput.value = transcript;
    if (event.results[event.results.length - 1].isFinal) {
      searchInput.form?.submit();
    }
  };

  recognition.onend = () => {
    isListening = false;
    micBtn.innerHTML = '&#127908;';
    micBtn.title = 'Voice search';
    searchInput.placeholder = searchInput.dataset.placeholder || 'Search restaurants or food...';
  };

  recognition.onerror = (e) => {
    isListening = false;
    micBtn.innerHTML = '&#127908;';
    if (e.error === 'not-allowed') {
      alert('Microphone permission denied. Please allow microphone access.');
    }
  };
}

document.addEventListener('DOMContentLoaded', initVoiceSearch);
// ===== ACCESSIBILITY TOOLBAR =====
// Append to static/js/main.js

function initAccessibilityToolbar() {
  const toolbar = document.createElement('div');
  toolbar.className = 'a11y-toolbar';
  toolbar.setAttribute('role', 'toolbar');
  toolbar.setAttribute('aria-label', 'Accessibility options');

  const settings = JSON.parse(localStorage.getItem('a11y') || '{}');

  const buttons = [
    { id: 'large-text',    icon: 'A+',   title: 'Large text',     cls: 'large-text' },
    { id: 'high-contrast', icon: '◑',    title: 'High contrast',  cls: 'high-contrast' },
    { id: 'reduce-motion', icon: '⏸',   title: 'Reduce motion',  cls: 'reduce-motion' },
    { id: 'dyslexia',      icon: 'Dy',   title: 'Dyslexia font',  cls: 'dyslexia-mode' },
  ];

  buttons.forEach(({ id, icon, title, cls }) => {
    const btn = document.createElement('button');
    btn.className = 'a11y-btn' + (settings[id] ? ' active' : '');
    btn.innerHTML = `<span style="font-size:11px;font-weight:700;">${icon}</span>`;
    btn.title = title;
    btn.setAttribute('aria-label', title);
    btn.setAttribute('aria-pressed', settings[id] ? 'true' : 'false');

    if (settings[id]) document.body.classList.add(cls);

    btn.addEventListener('click', () => {
      const isActive = document.body.classList.toggle(cls);
      btn.classList.toggle('active', isActive);
      btn.setAttribute('aria-pressed', isActive ? 'true' : 'false');
      settings[id] = isActive;
      localStorage.setItem('a11y', JSON.stringify(settings));
    });

    toolbar.appendChild(btn);
  });

  // Text size slider
  const sizeBtn = document.createElement('button');
  sizeBtn.className = 'a11y-btn';
  sizeBtn.title = 'Reset accessibility';
  sizeBtn.innerHTML = '<span style="font-size:11px;">↺</span>';
  sizeBtn.addEventListener('click', () => {
    buttons.forEach(({ cls }) => document.body.classList.remove(cls));
    toolbar.querySelectorAll('.a11y-btn').forEach(b => {
      b.classList.remove('active');
      b.setAttribute('aria-pressed', 'false');
    });
    localStorage.removeItem('a11y');
  });
  toolbar.appendChild(sizeBtn);

  document.body.appendChild(toolbar);

  // Keyboard navigation detection
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Tab') document.body.classList.add('keyboard-mode');
  });
  document.addEventListener('mousedown', () => {
    document.body.classList.remove('keyboard-mode');
  });
}

document.addEventListener('DOMContentLoaded', initAccessibilityToolbar);
