<template>
  <header class="top-header">
    <div class="merchant-identity">
      <div class="merchant-avatar">N</div>
      <div class="merchant-details">
        <div class="merchant-top-row">
          <span class="merchant-name">{{ merchantName }}</span>
          <span class="live-badge">Live Gateway</span>
        </div>
        <div class="merchant-mid-row">
          <span>{{ merchantId }}</span>
        </div>
      </div>
    </div>

    <div class="header-actions">
      <!-- Date Filter -->
      <button class="date-picker-btn">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <rect width="18" height="18" x="3" y="4" rx="2" ry="2"/>
          <line x1="16" y1="2" x2="16" y2="6"/>
          <line x1="8" y1="2" x2="8" y2="6"/>
          <line x1="3" y1="10" x2="21" y2="10"/>
        </svg>
        <span>Last 7 Days (06 May - 12 May 2025)</span>
      </button>

      <!-- Theme Switcher -->
      <button class="header-icon-btn" @click="$emit('toggle-theme')" :title="isLightMode ? 'Switch to Dark' : 'Switch to Light'">
        <svg v-if="!isLightMode" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="12" cy="12" r="5"/>
          <line x1="12" y1="1" x2="12" y2="3"/>
          <line x1="12" y1="21" x2="12" y2="23"/>
          <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/>
          <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/>
          <line x1="1" y1="12" x2="3" y2="12"/>
          <line x1="21" y1="12" x2="23" y2="12"/>
          <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/>
          <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/>
        </svg>
        <svg v-else width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>
        </svg>
      </button>

      <!-- Notification Alerts -->
      <button class="header-icon-btn" title="Alerts">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/>
          <path d="M10.3 21a1.94 1.94 0 0 0 3.4 0"/>
        </svg>
        <span class="alert-dot" v-if="alertCount > 0">{{ alertCount }}</span>
      </button>
    </div>
  </header>
</template>

<script setup lang="ts">
defineProps<{
  merchantName: string;
  merchantId: string;
  alertCount: number;
  isLightMode: boolean;
}>();

defineEmits(['toggle-theme']);
</script>

<style scoped>
.top-header {
  height: 60px;
  background-color: var(--bg-header, #0b0f19);
  border-bottom: 1px solid var(--border-card, #1e293b);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
}

.merchant-identity {
  display: flex;
  align-items: center;
  gap: 12px;
}

.merchant-avatar {
  width: 32px;
  height: 32px;
  background-color: #000;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #e50914;
  font-weight: 900;
  font-size: 18px;
  border: 1px solid rgba(229, 9, 20, 0.3);
}

.merchant-name {
  font-size: 14px;
  font-weight: 700;
  color: #f8fafc;
}

.live-badge {
  display: inline-flex;
  align-items: center;
  font-size: 10px;
  font-weight: 600;
  color: #10b981;
  background-color: rgba(16, 185, 129, 0.12);
  border: 1px solid rgba(16, 185, 129, 0.3);
  padding: 1px 6px;
  border-radius: 10px;
  margin-left: 8px;
}

.merchant-mid-row {
  font-size: 10.5px;
  color: #64748b;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 10px;
}

.date-picker-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  background-color: rgba(255, 255, 255, 0.03);
  border: 1px solid var(--border-card, #1e293b);
  padding: 6px 12px;
  border-radius: 6px;
  font-size: 12px;
  color: #f8fafc;
  cursor: pointer;
}

.header-icon-btn {
  width: 34px;
  height: 34px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: rgba(255, 255, 255, 0.03);
  border: 1px solid var(--border-card, #1e293b);
  border-radius: 6px;
  color: #94a3b8;
  position: relative;
  cursor: pointer;
}

.header-icon-btn:hover {
  color: #f8fafc;
}

.alert-dot {
  position: absolute;
  top: -4px;
  right: -4px;
  background-color: #ef4444;
  color: #fff;
  font-size: 9px;
  font-weight: 800;
  padding: 1px 4px;
  border-radius: 8px;
}
</style>
