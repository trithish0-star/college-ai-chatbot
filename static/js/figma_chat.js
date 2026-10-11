/**
 * College Chatbot Using AI - Dedicated Figma AI Chatbot Workspace
 * Mirrors the uploaded Figma layout (media_1791698291521.png)
 * Now with fully functional, verified Document Viewer modals & local routes!
 */

document.addEventListener('DOMContentLoaded', () => {
  const chatStream = document.getElementById('chatMessagesStream');
  const chatContainer = document.getElementById('figmaChatConversation');
  const chatInput = document.getElementById('figmaChatInput');
  const sendBtn = document.getElementById('figmaSendBtn');
  const newChatBtn = document.getElementById('btnNewChat');
  const promptCards = document.querySelectorAll('.figma-prompt-card');
  const promptGrid = document.getElementById('figmaPromptGrid');
  const watermarkBg = document.getElementById('figmaWatermarkBg');
  const rightDocsList = document.getElementById('rightDocsList');
  const fullscreenBtn = document.getElementById('figmaFullscreenToggle');
  const themeToggle = document.getElementById('themeToggle');
  const sidebarToggle = document.getElementById('mobileSidebarToggle');
  const sidebar = document.getElementById('figmaSidebar');

  // Modal elements
  const modalEl = document.getElementById('docPreviewModal');
  const modalInstance = modalEl ? new bootstrap.Modal(modalEl) : null;
  const modalTitle = document.getElementById('modalDocTitle');
  const modalCategory = document.getElementById('modalDocCategory');
  const modalBody = document.getElementById('modalDocBody');
  const modalOpenFull = document.getElementById('modalDocOpenFull');

  let currentSessionId = localStorage.getItem('college_figma_session') || ('figma_sess_' + Math.random().toString(36).substring(2, 9));
  localStorage.setItem('college_figma_session', currentSessionId);
  let hasInteracted = false;

  // Real, working verified documents pool
  const defaultDocs = [
    { 
      slug: "admission-portal", 
      title: "Admission Application 2026", 
      desc: "TNEA Single Window & Management Quota Registration", 
      icon: "bi-mortarboard-fill", 
      link: "/document/admission-portal" 
    },
    { 
      slug: "cse-fees", 
      title: "CSE Fee Structure PDF", 
      desc: "Annual tuition, lab, exam fees breakdown & bank challan", 
      icon: "bi-cash-coin", 
      link: "/document/cse-fees" 
    },
    { 
      slug: "hostel-guide", 
      title: "Hostel & Mess Rules Handbook", 
      desc: "Boys & girls room layout, 4-time buffet mess menu & rent", 
      icon: "bi-building-fill", 
      link: "/document/hostel-guide" 
    },
    { 
      slug: "placement-report", 
      title: "Placement Statistics Report", 
      desc: "85%+ placement, ₹14.5 LPA highest CTC, TCS/Infosys/Zoho offers", 
      icon: "bi-briefcase-fill", 
      link: "/document/placement-report" 
    },
    { 
      slug: "bus-routes", 
      title: "College Bus Routes & Timings", 
      desc: "35+ bus fleet stages across Chennai & stage tariff", 
      icon: "bi-bus-front-fill", 
      link: "/document/bus-routes" 
    },
    { 
      slug: "exam-schedule", 
      title: "Semester Examination Schedule", 
      desc: "Anna University Autonomous calendar, timetable & rules", 
      icon: "bi-calendar2-check-fill", 
      link: "/document/exam-schedule" 
    }
  ];

  renderRightDocs(defaultDocs);

  // Expose global openDocPreview function for chat bubbles
  window.openDocPreview = openDocPreview;

  // New Chat Click
  if (newChatBtn) {
    newChatBtn.addEventListener('click', () => {
      currentSessionId = 'figma_sess_' + Math.random().toString(36).substring(2, 9);
      localStorage.setItem('college_figma_session', currentSessionId);
      hasInteracted = false;
      chatStream.innerHTML = '';
      if (promptGrid) promptGrid.style.display = 'grid';
      if (watermarkBg) watermarkBg.style.display = 'block';
      renderRightDocs(defaultDocs);
      chatInput.focus();
    });
  }

  // Suggestion Prompt Cards Click
  promptCards.forEach(card => {
    card.addEventListener('click', () => {
      const q = card.getAttribute('data-query');
      if (q) {
        sendMessage(q);
      }
    });
  });

  // Mobile Sidebar Toggle
  if (sidebarToggle && sidebar) {
    sidebarToggle.addEventListener('click', () => {
      sidebar.classList.toggle('mobile-open');
    });
  }

  // Fullscreen Toggle
  if (fullscreenBtn) {
    fullscreenBtn.addEventListener('click', () => {
      if (!document.fullscreenElement) {
        document.documentElement.requestFullscreen().catch(err => console.log(err));
        fullscreenBtn.innerHTML = '<i class="bi bi-fullscreen-exit"></i>';
      } else {
        document.exitFullscreen();
        fullscreenBtn.innerHTML = '<i class="bi bi-arrows-fullscreen"></i>';
      }
    });
  }

  // Dark/Light Theme Toggle
  if (themeToggle) {
    themeToggle.addEventListener('click', () => {
      const current = document.documentElement.getAttribute('data-theme');
      const next = current === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', next);
      localStorage.setItem('figma_theme', next);
      themeToggle.innerHTML = next === 'dark' ? '<i class="bi bi-sun-fill text-warning"></i>' : '<i class="bi bi-moon-stars-fill text-secondary"></i>';
    });

    const savedTheme = localStorage.getItem('figma_theme');
    if (savedTheme) {
      document.documentElement.setAttribute('data-theme', savedTheme);
      themeToggle.innerHTML = savedTheme === 'dark' ? '<i class="bi bi-sun-fill text-warning"></i>' : '<i class="bi bi-moon-stars-fill text-secondary"></i>';
    }
  }

  // Send Event Listeners
  if (sendBtn && chatInput) {
    sendBtn.addEventListener('click', () => {
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

    if (!hasInteracted) {
      hasInteracted = true;
      if (promptGrid) promptGrid.style.display = 'none';
      if (watermarkBg) watermarkBg.style.opacity = '0.04';
    }

    appendFigmaMessage(text, 'user', {
      timestamp: formatTime(new Date()),
      language: detectTanglish(text) ? 'Tanglish' : 'English'
    });

    chatInput.value = '';
    showFigmaTyping();

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
      removeFigmaTyping();

      if (data.success) {
        appendFigmaMessage(data.answer, 'bot', {
          timestamp: data.timestamp || formatTime(new Date()),
          category: data.category,
          confidence: data.confidence,
          language: data.language,
          doc_link: data.doc_link,
          doc_title: data.doc_title,
          matched: data.matched
        });

        // Update right sidebar with relevant document or portal
        updateRightSidebarWithResult(data);
      } else {
        appendFigmaMessage("I encountered an issue processing your query. Please try again.", 'bot', {
          timestamp: formatTime(new Date())
        });
      }
    } catch (err) {
      removeFigmaTyping();
      console.error('Fetch error:', err);
      appendFigmaMessage("Connection lost. Please verify server status.", 'bot', {
        timestamp: formatTime(new Date())
      });
    }
  }

  function appendFigmaMessage(text, sender, meta = {}) {
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

    // Quick Action Doc Link in bubble (now interactive!)
    if (meta.doc_link && meta.doc_title && sender === 'bot') {
      const docCard = document.createElement('div');
      docCard.className = 'mt-2 pt-2 border-top';
      
      const slug = extractSlug(meta.doc_link);
      docCard.innerHTML = `
        <button type="button" class="btn btn-sm text-start p-0 d-inline-flex align-items-center gap-2 text-decoration-none fw-semibold border-0 bg-transparent" 
                style="font-size:0.84rem; color:#0d9488; cursor:pointer;"
                onclick="window.openDocPreview('${slug}')">
          <i class="bi bi-file-earmark-arrow-down-fill text-teal"></i>
          <span class="text-decoration-underline">${meta.doc_title}</span>
          <i class="bi bi-eye-fill ms-1 small"></i>
        </button>
      `;
      bubble.appendChild(docCard);
    }

    const metaBar = document.createElement('div');
    metaBar.className = 'msg-meta-bar';
    metaBar.innerHTML = `<span>${meta.timestamp || 'Now'}</span>`;

    if (meta.category) {
      metaBar.innerHTML += `<span class="msg-tag-badge">${meta.category}</span>`;
    }
    if (meta.confidence) {
      metaBar.innerHTML += `<span class="msg-lang-badge">${Math.round(meta.confidence * 100)}% Confidence</span>`;
    }
    if (meta.language) {
      metaBar.innerHTML += `<span class="msg-lang-badge">${meta.language}</span>`;
    }

    // Audio text-to-speech button for bot
    if (sender === 'bot') {
      const speakBtn = document.createElement('button');
      speakBtn.className = 'btn btn-sm btn-link p-0 text-muted ms-2';
      speakBtn.title = 'Read Aloud';
      speakBtn.innerHTML = '<i class="bi bi-volume-up"></i>';
      speakBtn.onclick = () => speakText(text);
      metaBar.appendChild(speakBtn);

      const copyBtn = document.createElement('button');
      copyBtn.className = 'btn btn-sm btn-link p-0 text-muted ms-2';
      copyBtn.title = 'Copy Answer';
      copyBtn.innerHTML = '<i class="bi bi-clipboard"></i>';
      copyBtn.onclick = () => {
        navigator.clipboard.writeText(text);
        copyBtn.innerHTML = '<i class="bi bi-check text-success"></i>';
        setTimeout(() => copyBtn.innerHTML = '<i class="bi bi-clipboard"></i>', 1800);
      };
      metaBar.appendChild(copyBtn);
    }

    contentWrapper.appendChild(bubble);
    contentWrapper.appendChild(metaBar);

    row.appendChild(avatar);
    row.appendChild(contentWrapper);

    chatStream.appendChild(row);
    scrollToBottom();
  }

  function showFigmaTyping() {
    const indicator = document.createElement('div');
    indicator.id = 'figmaTypingIndicator';
    indicator.className = 'message-bubble-row bot';
    indicator.innerHTML = `
      <div class="msg-avatar bot"><i class="bi bi-robot"></i></div>
      <div class="typing-dots-indicator">
        <span class="typing-dot"></span>
        <span class="typing-dot"></span>
        <span class="typing-dot"></span>
      </div>
    `;
    chatStream.appendChild(indicator);
    scrollToBottom();
  }

  function removeFigmaTyping() {
    const el = document.getElementById('figmaTypingIndicator');
    if (el) el.remove();
  }

  function scrollToBottom() {
    chatContainer.scrollTop = chatContainer.scrollHeight;
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

  function speakText(text) {
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.rate = 1.0;
      utterance.pitch = 1.0;
      window.speechSynthesis.speak(utterance);
    }
  }

  function extractSlug(urlOrSlug) {
    if (!urlOrSlug) return 'admission-portal';
    let s = urlOrSlug.replace('/document/', '').replace('.pdf', '').replace('https://example.edu/', '').replace('http://localhost:5000/document/', '');
    if (s.includes('cse')) return 'cse-fees';
    if (s.includes('hostel')) return 'hostel-guide';
    if (s.includes('placement')) return 'placement-report';
    if (s.includes('bus') || s.includes('transport')) return 'bus-routes';
    if (s.includes('exam')) return 'exam-schedule';
    if (s.includes('canteen')) return 'canteen-menu';
    return s || 'admission-portal';
  }

  async function openDocPreview(slugOrUrl) {
    const slug = extractSlug(slugOrUrl);
    try {
      const res = await fetch(`/api/document/${slug}`);
      const data = await res.json();
      if (data.success && data.document) {
        const doc = data.document;
        if (modalTitle) modalTitle.textContent = doc.title;
        if (modalCategory) modalCategory.textContent = `${doc.category} • Ref: ${doc.ref_no}`;
        if (modalBody) {
          modalBody.innerHTML = `
            <div class="p-3 bg-light rounded-3 border mb-3">
              <span class="badge bg-teal text-white mb-2" style="background-color: #0d9488;">${doc.badge}</span>
              <p class="small text-muted mb-0">${doc.summary}</p>
            </div>
            ${doc.content_html}
          `;
        }
        if (modalOpenFull) {
          modalOpenFull.href = `/document/${doc.slug}`;
        }
        if (modalInstance) {
          modalInstance.show();
        }
      }
    } catch (err) {
      console.error('Error fetching document preview:', err);
      // Fallback navigation
      window.open(`/document/${slug}`, '_blank');
    }
  }

  function updateRightSidebarWithResult(data) {
    if (data.doc_link && data.doc_title) {
      const slug = extractSlug(data.doc_link);
      const newDoc = {
        slug: slug,
        title: data.doc_title,
        desc: `Verified college document for category: ${data.category}`,
        icon: getCategoryIcon(data.category),
        link: `/document/${slug}`
      };
      // Prepend to list
      const currentDocs = [newDoc, ...defaultDocs.filter(d => d.slug !== slug)];
      renderRightDocs(currentDocs);
    }
  }

  function getCategoryIcon(cat) {
    switch (cat) {
      case 'Fees': return 'bi-cash-coin';
      case 'Admissions': return 'bi-mortarboard-fill';
      case 'Hostel': return 'bi-building-fill';
      case 'Placements': return 'bi-briefcase-fill';
      case 'Transport': return 'bi-bus-front-fill';
      case 'Examinations': return 'bi-calendar2-check-fill';
      case 'Courses': return 'bi-book-half';
      default: return 'bi-file-earmark-text-fill';
    }
  }

  function renderRightDocs(docs) {
    if (!rightDocsList) return;
    rightDocsList.innerHTML = '';
    docs.slice(0, 6).forEach(doc => {
      const card = document.createElement('div');
      card.className = 'doc-link-card';
      card.style.cursor = 'pointer';
      card.setAttribute('role', 'button');
      card.onclick = (e) => {
        e.preventDefault();
        openDocPreview(doc.slug || doc.link);
      };

      card.innerHTML = `
        <div class="doc-icon-box">
          <i class="bi ${doc.icon}"></i>
        </div>
        <div class="doc-link-info flex-grow-1">
          <h5 class="d-flex align-items-center justify-content-between">
            <span>${doc.title}</span>
            <i class="bi bi-box-arrow-up-right text-muted small ms-1"></i>
          </h5>
          <p>${doc.desc}</p>
        </div>
      `;
      rightDocsList.appendChild(card);
    });
  }
});
