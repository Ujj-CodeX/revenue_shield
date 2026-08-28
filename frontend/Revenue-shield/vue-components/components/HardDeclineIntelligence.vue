<template>
  <div class="card hard-decline-card">
    <div class="card-header">
      <div>
        <span class="card-title">HARD DECLINE INTELLIGENCE</span>
        <span class="card-subtitle">Last 7 days</span>
      </div>
    </div>

    <div class="hard-decline-body">
      <div class="hd-stat-block">
        <span class="hd-stat-title">Hard Declines</span>
        <span class="hd-stat-num">{{ declineData.totalCount }}</span>
        <span class="hd-stat-pct">✕ {{ declineData.percentOfTotal }} of total failures</span>
      </div>

      <div class="hd-loss-block">
        <span class="hd-loss-lbl">Expected Revenue Loss</span>
        <span class="hd-loss-val">{{ declineData.expectedLoss }}</span>
      </div>

      <div class="hd-reasons-list">
        <div class="hd-reasons-header">Top Hard Decline Reasons</div>
        
        <div v-for="item in declineData.reasons" :key="item.code" class="hd-reason-item">
          <span class="hd-reason-name">{{ item.code }}</span>
          <span class="hd-reason-stats">{{ item.count }} <span class="hd-reason-pct">({{ item.pct }})</span></span>
        </div>
      </div>

      <button class="btn-download-csv" @click="$emit('export-csv')">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2">
          <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
          <polyline points="7 10 12 15 17 10"/>
          <line x1="12" y1="15" x2="12" y2="3"/>
        </svg>
        Download CSV Report
      </button>

      <div class="csv-filename-sub">
        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
          <polyline points="14 2 14 8 20 8"/>
        </svg>
        <span>{{ declineData.exportFilename }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  declineData: any
}>();

defineEmits(['export-csv']);
</script>

<style scoped>
.card {
  background-color: var(--bg-card, #0f172a);
  border: 1px solid var(--border-card, #1e293b);
  border-radius: 12px;
  display: flex;
  flex-direction: column;
}

.card-header {
  padding: 14px 16px 10px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.card-title {
  font-size: 12.5px;
  font-weight: 700;
  letter-spacing: 0.4px;
  color: var(--text-primary, #f8fafc);
  text-transform: uppercase;
}

.card-subtitle {
  font-size: 11px;
  color: var(--text-muted, #64748b);
  margin-left: 6px;
}

.hard-decline-body {
  padding: 12px 16px 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.hd-stat-block {
  background: rgba(239, 68, 68, 0.08);
  border: 1px solid rgba(239, 68, 68, 0.2);
  border-radius: 8px;
  padding: 10px 12px;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.hd-stat-title { font-size: 10.5px; font-weight: 600; color: #fca5a5; }
.hd-stat-num { font-size: 20px; font-weight: 800; color: #f87171; }
.hd-stat-pct { font-size: 11px; color: #fca5a5; }

.hd-loss-block {
  display: flex;
  flex-direction: column;
  gap: 2px;
}
.hd-loss-lbl { font-size: 10.5px; color: #64748b; }
.hd-loss-val { font-size: 15px; font-weight: 700; color: #f8fafc; }

.hd-reasons-list {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.hd-reasons-header {
  font-size: 11px;
  font-weight: 700;
  color: #94a3b8;
  margin-bottom: 2px;
}

.hd-reason-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 11px;
  padding: 4px 0;
  border-bottom: 1px dashed rgba(255, 255, 255, 0.05);
}

.hd-reason-name {
  color: #e2e8f0;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
  font-size: 10.5px;
}

.hd-reason-stats {
  color: #94a3b8;
}

.hd-reason-pct {
  color: #64748b;
  font-size: 10px;
}

.btn-download-csv {
  width: 100%;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid var(--border-card, #1e293b);
  color: #f8fafc;
  padding: 8px 12px;
  border-radius: 6px;
  font-size: 11.5px;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  cursor: pointer;
  transition: all 0.15s ease;
  margin-top: 4px;
}

.btn-download-csv:hover {
  background: rgba(255, 255, 255, 0.08);
  border-color: #3b82f6;
}

.csv-filename-sub {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 10px;
  color: #64748b;
  justify-content: center;
}
</style>
