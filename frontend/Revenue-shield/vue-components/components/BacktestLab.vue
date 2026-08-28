<template>
  <div class="card card-backtest-lab">
    <div class="card-header">
      <div>
        <span class="card-title">BACKTEST LAB</span>
        <span class="card-subtitle">Baseline: Naive Retry</span>
      </div>
    </div>

    <div class="backtest-body">
      <!-- Comparison Box -->
      <div class="backtest-vs-card">
        <div class="bt-side">
          <span class="bt-lbl">Policy Recovery</span>
          <span class="bt-val">{{ backtestStats.policyRevenue }}</span>
          <span class="bt-rate rate-green">↗ {{ backtestStats.policyRate }} <span class="rate-sub">rate</span></span>
        </div>
        <span class="vs-badge">VS</span>
        <div class="bt-side text-right">
          <span class="bt-lbl">Naive Revenue</span>
          <span class="bt-val">{{ backtestStats.naiveRevenue }}</span>
          <span class="bt-rate rate-muted">↗ {{ backtestStats.naiveRate }} rate</span>
        </div>
      </div>

      <!-- 2x2 Metric Grid -->
      <div class="backtest-metric-grid">
        <div class="bt-stat-cell">
          <span class="bt-stat-lbl">Retries Avoided</span>
          <span class="bt-stat-num">{{ backtestStats.avoidedRetries }}</span>
          <span class="bt-stat-sub">↗ {{ backtestStats.avoidedPct }}</span>
        </div>
        <div class="bt-stat-cell">
          <span class="bt-stat-lbl">Precision</span>
          <span class="bt-stat-num">{{ backtestStats.precision }}</span>
        </div>
        <div class="bt-stat-cell">
          <span class="bt-stat-lbl">Recall</span>
          <span class="bt-stat-num">{{ backtestStats.recall }}</span>
        </div>
        <div class="bt-stat-cell">
          <span class="bt-stat-lbl">ROI</span>
          <span class="bt-stat-num">{{ backtestStats.roi }}</span>
          <span class="bt-stat-sub text-dim">Ops return</span>
        </div>
      </div>

      <!-- Re-run Button -->
      <button class="btn-rerun-backtest" @click="$emit('rerun')">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M21.5 2v6h-6M21.34 15.57a10 10 0 1 1-.57-8.38l5.67-5.67"/>
        </svg>
        Re-run Backtest
      </button>

      <div class="backtest-sub-note">Results recompute live</div>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  backtestStats: any
}>();

defineEmits(['rerun']);
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

.backtest-body {
  padding: 12px 16px 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.backtest-vs-card {
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid var(--border-card, #1e293b);
  border-radius: 8px;
  padding: 10px 12px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.bt-side {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.text-right {
  text-align: right;
}

.bt-lbl { font-size: 10px; color: #64748b; }
.bt-val { font-size: 13.5px; font-weight: 700; color: #f8fafc; }
.bt-rate { font-size: 10.5px; font-weight: 600; }
.rate-green { color: #34d399; }
.rate-muted { color: #64748b; }
.rate-sub { color: #64748b; font-weight: 400; }

.vs-badge {
  font-size: 10px;
  font-weight: 800;
  color: #64748b;
  background: rgba(255, 255, 255, 0.05);
  padding: 3px 6px;
  border-radius: 4px;
}

.backtest-metric-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
}

.bt-stat-cell {
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid var(--border-card, #1e293b);
  border-radius: 6px;
  padding: 8px 10px;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.bt-stat-lbl { font-size: 10px; color: #64748b; }
.bt-stat-num { font-size: 15px; font-weight: 700; color: #f8fafc; }
.bt-stat-sub { font-size: 10px; color: #34d399; }
.text-dim { color: #64748b; }

.btn-rerun-backtest {
  background: #2563eb;
  color: #fff;
  border: none;
  padding: 8px 12px;
  border-radius: 6px;
  font-size: 11.5px;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  cursor: pointer;
  margin-top: 4px;
}

.backtest-sub-note {
  font-size: 10px;
  color: #64748b;
  text-align: center;
}
</style>
