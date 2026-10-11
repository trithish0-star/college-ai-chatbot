/**
 * College Chatbot Using AI - Main Website & Floating Chat Widget Scripts
 */

document.addEventListener('DOMContentLoaded', () => {
  // Elements
  const chatTrigger = document.getElementById('floatingChatTrigger');
  const chatPopup = document.getElementById('floatingChatPopup');
  const chatCloseBtn = document.getElementById('popupCloseBtn');
  const chatBody = document.getElementById('popupChatBody');
  const chatInput = document.getElementById('popupInput');
  const chatSendBtn = document.getElementById('popupSendBtn');
  const clearChatBtn = document.getElementById('popupClearBtn');
  const quickChips = document.querySelectorAll('.quick-chip-btn');
  
  let currentSessionId = localStorage.getItem('college_chat_session') || ('sess_' + Math.random().toString(36).substring(2, 9));
  localStorage.setItem('college_chat_session', currentSessionId);

  // Toggle Chat Popup
  if (chatTrigger && chatPopup) {
    chatTrigger.addEventListener('click', () => {
      chatPopup.classList.toggle('active');
      if (chatPopup.classList.contains('active')) {
        chatInput.focus();
        scrollToBottom();
      }
    });
  }

  if (chatCloseBtn && chatPopup) {
    chatCloseBtn.addEventListener('click', () => {
      chatPopup.classList.remove('active');
    });
  }

  // Quick Chips
  quickChips.forEach(chip => {
    chip.addEventListener('click', () => {
      const query = chip.getAttribute('data-query');
      if (query) {
        sendMessage(query);
      }
    });
  });

  // Clear Chat
  if (clearChatBtn) {
    clearChatBtn.addEventListener('click', async () => {
      try {
        await fetch('/api/chat/clear', { method: 'POST' });
        currentSessionId = 'sess_' + Math.random().toString(36).substring(2, 9);
        localStorage.setItem('college_chat_session', currentSessionId);
        chatBody.innerHTML = `
          <div class="message-bubble-row">
            <div class="msg-avatar bot"><i class="bi bi-robot"></i></div>
            <div class="msg-content-wrapper">
              <div class="msg-bubble bot">
                Hi! 👋 Welcome to your College Assistant. How can I help you today?<br><br>
                <small class="text-muted">Ask me anything about admissions, courses, fees, hostel facilities, transport, examinations, and placements in English or Tanglish.</small>
              </div>
              <div class="msg-meta-bar">
                <span>Just now</span>
                <span class="msg-tag-badge">AI Assistant</span>
              </div>
            </div>
          </div>
        `;
      } catch (err) {
        console.error('Error clearing chat:', err);
      }
    });
  }

  // Send Message Event Listeners
  if (chatSendBtn && chatInput) {
    chatSendBtn.addEventListener('click', () => {
      const q = chatInput.value.trim();
      if (q) sendMessage(q);
    });

    chatInput.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        const q = chatInput.value.trim();
        if (q) sendMessage(q);
      }
    });
  }

  // Send Message Logic
  async function sendMessage(text) {
    if (!text.trim()) return;

    // Append User Message
    appendMessage(text, 'user', {
      timestamp: formatTime(new Date()),
      language: detectTanglish(text) ? 'Tanglish' : 'English'
    });

    chatInput.value = '';
    showTypingIndicator();

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          query: text,
          session_id: currentSessionId
        })
      });

      const data = await response.json();
      removeTypingIndicator();

      if (data.success) {
        appendMessage(data.answer, 'bot', {
          timestamp: data.timestamp || formatTime(new Date()),
          category: data.category,
          confidence: data.confidence,
          language: data.language,
          doc_link: data.doc_link,
          doc_title: data.doc_title
        });
      } else {
        appendMessage("I'm sorry, I encountered a temporary problem. Please try again or reach the admission office.", 'bot', {
          timestamp: formatTime(new Date())
        });
      }
    } catch (error) {
      removeTypingIndicator();
      console.error('Chat error:', error);
      appendMessage("Network error: Could not reach the chatbot server. Please check your connection.", 'bot', {
        timestamp: formatTime(new Date())
      });
    }
  }

  function appendMessage(text, sender, meta = {}) {
    const row = document.createElement('div');
    row.className = `message-bubble-row ${sender}`;

    const avatar = document.createElement('div');
    avatar.className = `msg-avatar ${sender}`;
    avatar.innerHTML = sender === 'user' ? '<i class="bi bi-person-fill"></i>' : '<i class="bi bi-robot"></i>';

    const contentWrapper = document.createElement('div');
    contentWrapper.className = 'msg-content-wrapper';

    const bubble = document.createElement('div');
    bubble.className = `msg-bubble ${sender}`;
    bubble.innerHTML = text.replace(/\n/g, '<br>');

    // Optional document card if provided
    if (meta.doc_link && meta.doc_title && sender === 'bot') {
      const docBox = document.createElement('div');
      docBox.className = 'mt-2 pt-2 border-top';
      docBox.innerHTML = `
        <a href="${meta.doc_link}" target="_blank" class="d-inline-flex align-items-center gap-2 text-decoration-none font-weight-bold" style="font-size:0.8rem; color:#0d9488;">
          <i class="bi bi-file-earmark-text-fill"></i>
          <span>${meta.doc_title}</span>
          <i class="bi bi-box-arrow-up-right ms-1"></i>
        </a>
      `;
      bubble.appendChild(docBox);
    }

    const metaBar = document.createElement('div');
    metaBar.className = 'msg-meta-bar';
    metaBar.innerHTML = `<span>${meta.timestamp || 'Now'}</span>`;

    if (meta.category) {
      metaBar.innerHTML += `<span class="msg-tag-badge">${meta.category}</span>`;
    }
    if (meta.confidence && meta.confidence > 0) {
      metaBar.innerHTML += `<span class="msg-lang-badge">${Math.round(meta.confidence * 100)}% Match</span>`;
    }

    contentWrapper.appendChild(bubble);
    contentWrapper.appendChild(metaBar);

    row.appendChild(avatar);
    row.appendChild(contentWrapper);

    chatBody.appendChild(row);
    scrollToBottom();
  }

  function showTypingIndicator() {
    const indicator = document.createElement('div');
    indicator.id = 'floatingTypingIndicator';
    indicator.className = 'message-bubble-row bot';
    indicator.innerHTML = `
      <div class="msg-avatar bot"><i class="bi bi-robot"></i></div>
      <div class="typing-dots-indicator">
        <span class="typing-dot"></span>
        <span class="typing-dot"></span>
        <span class="typing-dot"></span>
      </div>
    `;
    chatBody.appendChild(indicator);
    scrollToBottom();
  }

  function removeTypingIndicator() {
    const el = document.getElementById('floatingTypingIndicator');
    if (el) el.remove();
  }

  function scrollToBottom() {
    chatBody.scrollTop = chatBody.scrollHeight;
  }

  function formatTime(d) {
    let hours = d.getHours();
    let minutes = d.getMinutes();
    const ampm = hours >= 12 ? 'PM' : 'AM';
    hours = hours % 12;
    hours = hours ? hours : 12;
    minutes = minutes < 10 ? '0' + minutes : minutes;
    return `${hours}:${minutes} ${ampm}`;
  }

  function detectTanglish(txt) {
    const markers = ['evlo', 'evalo', 'iruka', 'irukka', 'eppadi', 'venum', 'sollunga', 'enga', 'ku', 'la', 'ah'];
    const words = txt.toLowerCase().split(/\s+/);
    return words.some(w => markers.includes(w));
  }
});
