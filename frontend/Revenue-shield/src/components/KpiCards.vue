<template>
  <header class="terminal-header" id="terminal-header">
    <!-- Left: Mobile Toggle, Breadcrumb, Title, Metadata -->
    <div class="d-flex align-items-start gap-2" id="header-left-wrapper">
      <!-- Mobile Sidebar Toggle -->
      <button 
        type="button" 
        class="terminal-icon-btn mobile-menu-toggle d-lg-none mt-1" 
        id="btn-toggle-sidebar" 
        aria-label="Toggle Navigation"
        @click="$emit('toggle-sidebar')"
      >
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="square" stroke-linejoin="miter">
          <line x1="3" y1="6" x2="21" y2="6"></line>
          <line x1="3" y1="12" x2="21" y2="12"></line>
          <line x1="3" y1="18" x2="21" y2="18"></line>
        </svg>
      </button>

      <div id="header-left-section">
        <div class="breadcrumb-nav" id="header-breadcrumb">
          <span>Merchant Workspace</span>
          <span class="mx-1">&gt;</span>
          <span class="text-terminal-bright">Overview</span>
        </div>

        <div class="header-title-row flex-wrap" id="header-title-row">
          <h1 class="merchant-name-title" id="header-merchant-name">{{ merchant.merchantName }}</h1>
          <span class="status-badge-active" id="header-status-badge">{{ merchant.status }}</span>
        </div>

        <div class="header-metadata-row flex-wrap" id="header-metadata-row">
          <span>MID: {{ merchant.merchantId }}</span>
          <span class="d-none d-sm-inline">|</span>
          <span>Industry: {{ merchant.industry }}</span>
          <span class="d-none d-sm-inline">|</span>
          <span>Plan: {{ merchant.plan }}</span>
        </div>
      </div>
    </div>

    <!-- Right: Date Range Selector & Data As Of Box -->
    <div class="header-right-controls" id="header-right-section">
      <!-- Date Range Selector Box -->
      <div class="terminal-control-box" id="date-range-box">
        <span id="date-range-display">{{ merchant.dateRange }}</span>
        <button class="terminal-icon-btn" id="btn-calendar" title="Select Date Range" @click="$emit('open-date-picker')">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="square" stroke-linejoin="miter">
            <rect x="3" y="4" width="18" height="18" rx="0" ry="0"></rect>
            <line x1="16" y1="2" x2="16" y2="6"></line>
            <line x1="8" y1="2" x2="8" y2="6"></line>
            <line x1="3" y1="10" x2="21" y2="10"></line>
          </svg>
        </button>
      </div>

      <!-- Data As Of & Seed / Run ID Box -->
      <div class="terminal-control-box meta-box" id="meta-info-box">
        <div class="d-flex align-items-center justify-content-between w-100 gap-2">
          <span class="text-terminal-main text-nowrap" id="data-as-of-text">Data as of: {{ merchant.dataAsOf }}</span>
          <button class="terminal-icon-btn" id="btn-refresh-data" title="Refresh Live State" @click="$emit('refresh-data')">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="square" stroke-linejoin="miter">
              <path d="M21.5 2v6h-6M21.34 15.57a10 10 0 1 1-.57-8.38l5.67-5.67"></path>
            </svg>
          </button>
        </div>
        <div class="d-flex align-items-center gap-2 flex-wrap" id="seed-run-id-row">
          <span class="text-terminal-green fw-bold text-nowrap" id="seed-value-display">Seed: {{ merchant.seed }}</span>
          <span class="text-terminal-muted">|</span>
          <span class="text-terminal-muted text-nowrap" id="backtest-run-id-display">Backtest Run ID: {{ merchant.backtestRunId }}</span>
        </div>
      </div>
    </div>
  </header>
</template>

<script>
export default {
  name: 'HeaderBar',
  props: {
    merchant: {
      type: Object,
      required: true
    }
  },
  emits: ['refresh-data', 'open-date-picker', 'toggle-sidebar']
};
</script>
