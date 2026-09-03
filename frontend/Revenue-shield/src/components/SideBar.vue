<template>
  <div>
    <!-- Mobile Backdrop -->
    <div 
      v-if="isOpen" 
      class="sidebar-backdrop d-lg-none" 
      id="sidebar-backdrop"
      @click="$emit('close')"
    ></div>

    <!-- Terminal Sidebar -->
    <aside 
      class="terminal-sidebar" 
      :class="{ 'is-open': isOpen }" 
      id="sidebar-container"
    >
      <!-- Mobile Close Button -->
      <button 
        type="button" 
        class="terminal-icon-btn sidebar-close-btn d-lg-none" 
        id="btn-close-sidebar" 
        aria-label="Close Sidebar"
        @click="$emit('close')"
      >
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="square" stroke-linejoin="miter">
          <line x1="18" y1="6" x2="6" y2="18"></line>
          <line x1="6" y1="6" x2="18" y2="18"></line>
        </svg>
      </button>

      <!-- Brand Header -->
      <div class="brand-header" id="brand-header">
        <div class="brand-title" id="brand-title">
          <svg class="brand-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 2L3 6V11C3 16.55 6.84 21.74 12 23C17.16 21.74 21 16.55 21 11V6L12 2Z" stroke="#7CFC6A" stroke-width="1.8" stroke-linecap="square" stroke-linejoin="miter"/>
            <path d="M12 7V13L15 16" stroke="#7CFC6A" stroke-width="1.8" stroke-linecap="square"/>
            <path d="M8.5 11.5L12 8L15.5 11.5" stroke="#7CFC6A" stroke-width="1.5" stroke-linecap="square"/>
          </svg>
          <span>REVENUE SHIELD AI</span>
        </div>
        <div class="brand-subtitle" id="brand-subtitle">
          Operational Intelligence Copilot for Recurring Payment Recovery
        </div>
      </div>

      <!-- Navigation Section -->
      <div class="mb-4" id="nav-section">
        <div class="sidebar-section-title" id="nav-section-title">NAVIGATION</div>
        <nav class="d-flex flex-column" id="terminal-nav">
          <a href="#" class="nav-terminal-item active" id="nav-overview" @click.prevent="$emit('close')">
            <div class="d-flex align-items-center gap-2">
              <span class="text-terminal-green">&gt;_</span>
              <span>OVERVIEW</span>
            </div>
          </a>
        </nav>
      </div>

      <!-- Merchant Context Section -->
      <div class="mb-4" id="merchant-context-section">
        <div class="sidebar-section-title" id="context-section-title">MERCHANT CONTEXT</div>
        <div class="merchant-context-list" id="context-list">
          <div class="context-row" id="ctx-row-merchant">
            <span class="context-label">Merchant</span>
            <span class="context-value merchant-active" id="ctx-merchant-name">{{ merchant.merchantName }}</span>
          </div>
          <div class="context-row" id="ctx-row-mid">
            <span class="context-label">Merchant ID</span>
            <span class="context-value" id="ctx-merchant-id">{{ merchant.merchantId }}</span>
          </div>
          <div class="context-row" id="ctx-row-industry">
            <span class="context-label">Industry</span>
            <span class="context-value" id="ctx-industry">{{ merchant.industry }}</span>
          </div>
          <div class="context-row" id="ctx-row-plan">
            <span class="context-label">Plan</span>
            <span class="context-value" id="ctx-plan">{{ merchant.plan }}</span>
          </div>
          <div class="context-row" id="ctx-row-status">
            <span class="context-label">Status</span>
            <span class="context-value status-active" id="ctx-status">{{ merchant.status }}</span>
          </div>
          <div class="context-row" id="ctx-row-onboarded">
            <span class="context-label">Onboarded On</span>
            <span class="context-value" id="ctx-onboarded">{{ merchant.onboardedDate }}</span>
          </div>
        </div>
      </div>

      <!-- Bottom Help Box & Copyright -->
      <div class="sidebar-footer-box" id="sidebar-help-box">
        <div class="help-title" id="help-box-title">NEED HELP?</div>
        <div class="help-links" id="help-box-links">
          <a href="#docs" id="link-docs" @click.prevent>Read docs</a>
          <span class="text-terminal-muted mx-1">|</span>
          <a href="#ops" id="link-ops" @click.prevent>Contact ops</a>
        </div>
      </div>

      <div class="sidebar-copyright" id="sidebar-copyright">
        &copy; 2025 Razorpay &bull; Internal Use Only
      </div>
    </aside>
  </div>
</template>

<script>
export default {
  name: 'Sidebar',
  props: {
    merchant: {
      type: Object,
      required: true
    },
    isOpen: {
      type: Boolean,
      default: false
    }
  },
  emits: ['close']
};
</script>
