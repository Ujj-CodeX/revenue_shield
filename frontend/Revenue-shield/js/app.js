/**
 * ==========================================================================
 * REVENUE SHIELD AI - OPERATIONAL INTELLIGENCE DASHBOARD
 * Pure Vanilla JavaScript Application (No frameworks, No backend)
 * Structured with modular data models for easy migration to Vue.js / Bootstrap
 * ==========================================================================
 */

document.addEventListener('DOMContentLoaded', () => {
  // Initialize all interactive dashboard modules
  initThemeToggle();
  initCopyMID();
  initDateRangePicker();
  initActionCenter();
  initHardDeclineExport();
  initSystemicPatternTabs();
  initBacktestLab();
  initAICopilot();
  initMobileNavigation();
});

/* ==========================================================================
   MODULE 1: THEME TOGGLE (Dark / Light Mode)
   ========================================================================== */
function initThemeToggle() {
  const themeToggleBtn = document.getElementById('theme-toggle-btn');
  if (!themeToggleBtn) return;

  // Set default dark mode or read from localStorage
  const currentTheme = localStorage.getItem('revenue_shield_theme') || 'dark';
  document.documentElement.setAttribute('data-theme', currentTheme);

  themeToggleBtn.addEventListener('click', () => {
    const activeTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = activeTheme === 'light' ? 'dark' : 'light';
    
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('revenue_shield_theme', newTheme);
    
    showToast(`Switched to ${newTheme === 'dark' ? 'Dark' : 'Light'} theme`);
  });
}

/* ==========================================================================
   MODULE 2: COPY MERCHANT ID (MID)
   ========================================================================== */
function initCopyMID() {
  const copyBtn = document.getElementById('copy-mid-btn');
  if (!copyBtn) return;

  copyBtn.addEventListener('click', () => {
    const midText = 'NETFLIX_IND_001';
    navigator.clipboard.writeText(midText).then(() => {
      showToast(`Copied ${midText} to clipboard!`);
    }).catch(() => {
      showToast(`Copied ${midText}`);
    });
  });
}

/* ==========================================================================
   MODULE 3: DATE RANGE PICKER DROPDOWN
   ========================================================================== */
function initDateRangePicker() {
  const datePickerBtn = document.getElementById('date-picker-btn');
  if (!datePickerBtn) return;

  const dateRanges = [
    '6 May 2025 - 12 May 2025',
    '1 May 2025 - 7 May 2025',
    'Last 24 Hours',
    'Last 30 Days',
    'This Month (May 2025)'
  ];
  let currentIndex = 0;

  datePickerBtn.addEventListener('click', () => {
    currentIndex = (currentIndex + 1) % dateRanges.length;
    const dateTextEl = document.getElementById('date-range-text');
    if (dateTextEl) {
      dateTextEl.textContent = dateRanges[currentIndex];
      showToast(`Dashboard filtered to: ${dateRanges[currentIndex]}`);
    }
  });
}

/* ==========================================================================
   MODULE 4: ACTION CENTER RECOMMENDATIONS
   ========================================================================== */
function initActionCenter() {
  // Detail toggle buttons
  const detailButtons = document.querySelectorAll('.btn-details-dropdown');
  detailButtons.forEach((btn) => {
    btn.addEventListener('click', (e) => {
      const card = e.target.closest('.action-item-card');
      if (!card) return;
      const detailsSection = card.querySelector('.action-details-expand');
      if (detailsSection) {
        detailsSection.classList.toggle('open');
        btn.innerHTML = detailsSection.classList.contains('open') 
          ? `Hide Details <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m18 15-6-6-6 6"/></svg>`
          : `View Details <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m6 9 6 6 6-6"/></svg>`;
      }
    });
  });

  // Approve Retry Buttons
  const approveButtons = document.querySelectorAll('.btn-approve-retry');
  approveButtons.forEach((btn) => {
    btn.addEventListener('click', (e) => {
      const card = e.target.closest('.action-item-card');
      btn.disabled = true;
      btn.textContent = '✓ Approved & Queued';
      btn.style.backgroundColor = 'var(--color-success)';
      btn.style.borderColor = 'transparent';
      showToast('Retry policy queued for execution at optimal window');
      
      // Decrement action count badge
      const badge = document.querySelector('.nav-badge');
      if (badge) {
        const count = parseInt(badge.textContent, 10);
        if (count > 0) badge.textContent = (count - 1).toString();
      }
    });
  });

  // Review Now Button
  const reviewButton = document.getElementById('btn-review-now');
  if (reviewButton) {
    reviewButton.addEventListener('click', () => {
      showToast('Opening 213 unstructured failure logs for automated classification analysis...');
    });
  }
}

/* ==========================================================================
   MODULE 5: HARD DECLINE CSV EXPORT GENERATOR
   ========================================================================== */
function initHardDeclineExport() {
  const exportBtn = document.getElementById('btn-download-csv');
  if (!exportBtn) return;

  exportBtn.addEventListener('click', () => {
    const csvContent = [
      'Transaction_ID,Date_Time,Customer_MID,Failure_Reason,Amount_INR,Bank,Gateway,Retry_Eligible',
      'TXN_9841284,2025-05-12 10:14:22,NETFLIX_IND_001,CARD_EXPIRED,649,HDFC,Razorpay,FALSE',
      'TXN_9841285,2025-05-12 10:15:01,NETFLIX_IND_001,MANDATE_REVOKED,499,ICICI,Razorpay,FALSE',
      'TXN_9841286,2025-05-12 10:16:45,NETFLIX_IND_001,ACCOUNT_CLOSED,649,SBI,Razorpay,FALSE',
      'TXN_9841287,2025-05-12 10:18:12,NETFLIX_IND_001,CUSTOMER_BLOCKED,199,Axis,Razorpay,FALSE',
      'TXN_9841288,2025-05-12 10:20:30,NETFLIX_IND_001,CARD_EXPIRED,649,Kotak,Razorpay,FALSE',
      'TXN_9841289,2025-05-12 10:22:11,NETFLIX_IND_001,OTHER,499,HDFC,Razorpay,FALSE'
    ].join('\n');

    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const downloadLink = document.createElement('a');
    downloadLink.setAttribute('href', url);
    downloadLink.setAttribute('download', 'Netflix_Hard_Declines_12May2025.csv');
    document.body.appendChild(downloadLink);
    downloadLink.click();
    document.body.removeChild(downloadLink);
    URL.revokeObjectURL(url);

    showToast('Downloaded Netflix_Hard_Declines_12May2025.csv');
  });
}

/* ==========================================================================
   MODULE 6: SYSTEMIC PATTERN DETECTION (Tabs)
   ========================================================================== */
const PATTERN_DATA = {
  banks: [
    { name: 'HDFC Bank', score: 28, scoreType: 'red', trend: 'down', failureRate: '18.7%', status: 'Degrading', statusType: 'degrading' },
    { name: 'ICICI Bank', score: 63, scoreType: 'amber', trend: 'down', failureRate: '9.2%', status: 'Watch', statusType: 'watch' },
    { name: 'SBI', score: 72, scoreType: 'amber', trend: 'flat', failureRate: '6.1%', status: 'Watch', statusType: 'watch' },
    { name: 'Axis Bank', score: 85, scoreType: 'green', trend: 'up', failureRate: '3.2%', status: 'Healthy', statusType: 'healthy' },
    { name: 'Kotak Bank', score: 92, scoreType: 'green', trend: 'up', failureRate: '2.1%', status: 'Healthy', statusType: 'healthy' }
  ],
  gateways: [
    { name: 'Razorpay Direct', score: 89, scoreType: 'green', trend: 'up', failureRate: '2.8%', status: 'Healthy', statusType: 'healthy' },
    { name: 'PayU Recurring', score: 64, scoreType: 'amber', trend: 'down', failureRate: '8.7%', status: 'Watch', statusType: 'watch' },
    { name: 'Juspay Router', score: 94, scoreType: 'green', trend: 'up', failureRate: '1.9%', status: 'Healthy', statusType: 'healthy' },
    { name: 'BillDesk SI', score: 41, scoreType: 'red', trend: 'down', failureRate: '14.2%', status: 'Degrading', statusType: 'degrading' }
  ],
  methods: [
    { name: 'UPI AutoPay', score: 91, scoreType: 'green', trend: 'up', failureRate: '2.4%', status: 'Healthy', statusType: 'healthy' },
    { name: 'Cards e-Mandate', score: 68, scoreType: 'amber', trend: 'flat', failureRate: '7.9%', status: 'Watch', statusType: 'watch' },
    { name: 'NetBanking SI', score: 38, scoreType: 'red', trend: 'down', failureRate: '16.5%', status: 'Degrading', statusType: 'degrading' },
    { name: 'NACH / eNACH', score: 82, scoreType: 'green', trend: 'up', failureRate: '4.1%', status: 'Healthy', statusType: 'healthy' }
  ]
};

function initSystemicPatternTabs() {
  const tabs = document.querySelectorAll('.tab-pill');
  const tableBody = document.getElementById('pattern-table-body');
  const tableHeader = document.getElementById('pattern-header-name');
  if (!tabs.length || !tableBody) return;

  tabs.forEach((tab) => {
    tab.addEventListener('click', () => {
      tabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');

      const tabType = tab.getAttribute('data-tab');
      renderPatternTable(tabType);
    });
  });

  function renderPatternTable(type) {
    const items = PATTERN_DATA[type] || PATTERN_DATA.banks;
    if (tableHeader) {
      tableHeader.textContent = type === 'banks' ? 'BANK' : type === 'gateways' ? 'GATEWAY' : 'PAYMENT METHOD';
    }

    tableBody.innerHTML = items.map(item => `
      <tr>
        <td><strong>${item.name}</strong></td>
        <td>
          <span class="score-indicator">
            <span class="score-dot ${item.scoreType}"></span>
            ${item.score}
          </span>
        </td>
        <td>
          <svg width="48" height="16" viewBox="0 0 48 16" fill="none">
            ${item.trend === 'down' 
              ? '<path d="M2 3 L14 5 L26 11 L38 8 L46 14" stroke="#ef4444" stroke-width="1.8" stroke-linecap="round"/>' 
              : item.trend === 'flat' 
              ? '<path d="M2 8 L14 7 L26 9 L38 7 L46 8" stroke="#f59e0b" stroke-width="1.8" stroke-linecap="round"/>'
              : '<path d="M2 14 L14 10 L26 12 L38 5 L46 2" stroke="#10b981" stroke-width="1.8" stroke-linecap="round"/>'}
          </svg>
        </td>
        <td>${item.failureRate}</td>
        <td>
          <span class="status-badge status-${item.statusType}">${item.status}</span>
        </td>
      </tr>
    `).join('');
  }
}

/* ==========================================================================
   MODULE 7: BACKTEST LAB RE-RUN ENGINE
   ========================================================================== */
function initBacktestLab() {
  const rerunBtn = document.getElementById('btn-rerun-backtest');
  if (!rerunBtn) return;

  rerunBtn.addEventListener('click', () => {
    rerunBtn.classList.add('computing');
    rerunBtn.innerHTML = `
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M21.5 2v6h-6M21.34 15.57a10 10 0 1 1-.57-8.38l5.67-5.67"/>
      </svg>
      Computing 45,812 Transactions...
    `;

    setTimeout(() => {
      rerunBtn.classList.remove('computing');
      rerunBtn.innerHTML = `
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M21.5 2v6h-6M21.34 15.57a10 10 0 1 1-.57-8.38l5.67-5.67"/>
        </svg>
        Re-run Backtest
      `;

      // Update Backtest ROI & avoided retries slightly to show dynamic simulation
      const avoidedEl = document.getElementById('bt-avoided-count');
      const roiEl = document.getElementById('bt-roi-val');
      if (avoidedEl) avoidedEl.textContent = '12,842';
      if (roiEl) roiEl.textContent = '2.34x';

      showToast('Backtest completed! Decision policy validated against baseline.');
    }, 900);
  });
}

/* ==========================================================================
   MODULE 8: AI COPILOT INTERACTIVE ASSISTANT
   ========================================================================== */
const COPILOT_KNOWLEDGE = {
  'Why did HDFC failures spike?': 'HDFC Bank is exhibiting an 18.7% failure rate over the last 2 hours. Root cause: Core banking OTP/Mandate sync timeout (Error Code: ERR_HDFC_CBS_TIMEDOUT). Recommendation: Auto-route non-mandate retries to 06 May 10:30 AM post-clearing.',
  'Explain this recommendation': 'Recommendation #1 targets 213 transactions categorized as Soft Declines. Analysis shows users receiving salary deposits between the 5th and 7th have an 82% higher success probability when retried during the 10:30 AM banking settlement window.',
  'Why was this marked hard decline?': 'Hard declines (18,765 transactions) represent terminal terminal failure codes such as CARD_EXPIRED (36.4%) and MANDATE_REVOKED (22.8%). Retrying these violates card network rules and incurs avoidable operational gateway fees.',
  'Show top recovery opportunities': 'Top recoverable revenue is ₹2,92,18,400 with 34.2% recovery potential. Primary recovery vectors: (1) Salary credit timing alignment (₹38.4k batch), (2) Network timeout re-dispatch (₹11.2k batch), (3) Bank clearing window synchronization.'
};

function initAICopilot() {
  const chips = document.querySelectorAll('.copilot-chip');
  const input = document.getElementById('copilot-query-input');
  const sendBtn = document.getElementById('btn-send-copilot');
  const msgContainer = document.getElementById('copilot-messages-container');
  const chipsContainer = document.getElementById('copilot-chips-container');
  const closeBtn = document.getElementById('btn-copilot-close');

  if (!input || !sendBtn || !msgContainer) return;

  chips.forEach((chip) => {
    chip.addEventListener('click', () => {
      const question = chip.textContent.trim();
      handleCopilotQuestion(question);
    });
  });

  sendBtn.addEventListener('click', () => {
    const question = input.value.trim();
    if (question) {
      handleCopilotQuestion(question);
      input.value = '';
    }
  });

  input.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
      const question = input.value.trim();
      if (question) {
        handleCopilotQuestion(question);
        input.value = '';
      }
    }
  });

  if (closeBtn) {
    closeBtn.addEventListener('click', () => {
      const card = document.getElementById('copilot-card');
      if (card) {
        card.style.opacity = '0.5';
        showToast('AI Copilot minimized.');
      }
    });
  }

  function handleCopilotQuestion(question) {
    msgContainer.classList.add('has-messages');
    
    // Add user message
    const userBubble = document.createElement('div');
    userBubble.className = 'chat-msg user';
    userBubble.textContent = question;
    msgContainer.appendChild(userBubble);
    msgContainer.scrollTop = msgContainer.scrollHeight;

    // AI Assistant response with realistic typing delay
    setTimeout(() => {
      const response = COPILOT_KNOWLEDGE[question] || 
        `Analysis for "${question}": Decision engine analyzed current transaction flow across 45,812 records. Soft decline recovery probability is optimal within the next 4-hour clearing window.`;
      
      const aiBubble = document.createElement('div');
      aiBubble.className = 'chat-msg assistant';
      aiBubble.textContent = response;
      msgContainer.appendChild(aiBubble);
      msgContainer.scrollTop = msgContainer.scrollHeight;
    }, 450);
  }
}

/* ==========================================================================
   MODULE 9: MOBILE SIDEBAR TOGGLE
   ========================================================================== */
function initMobileNavigation() {
  const toggleBtn = document.getElementById('mobile-menu-toggle');
  const sidebar = document.querySelector('.sidebar');
  if (!toggleBtn || !sidebar) return;

  toggleBtn.addEventListener('click', () => {
    sidebar.classList.toggle('open');
  });

  // Close sidebar when clicking outside on mobile
  document.addEventListener('click', (e) => {
    if (sidebar.classList.contains('open') && 
        !sidebar.contains(e.target) && 
        !toggleBtn.contains(e.target)) {
      sidebar.classList.remove('open');
    }
  });
}

/* ==========================================================================
   TOAST HELPER NOTIFICATION
   ========================================================================== */
function showToast(message) {
  let container = document.querySelector('.toast-container');
  if (!container) {
    container = document.createElement('div');
    container.className = 'toast-container';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  toast.className = 'toast';
  toast.innerHTML = `
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#10b981" stroke-width="2.5">
      <path d="M20 6 9 17l-5-5"/>
    </svg>
    <span>${message}</span>
  `;

  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(10px)';
    toast.style.transition = 'all 0.25s ease';
    setTimeout(() => {
      if (toast.parentNode) toast.parentNode.removeChild(toast);
    }, 300);
  }, 3200);
}
