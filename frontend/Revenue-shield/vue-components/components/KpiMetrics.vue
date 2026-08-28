<template>
  <section class="kpi-grid">
    <!-- 1. Recovered Revenue -->
    <div class="kpi-card">
      <div class="kpi-header">
        <span class="kpi-title">RECOVERED REVENUE</span>
      </div>
      <div class="kpi-value-row">
        <span class="kpi-value">{{ metrics.recoveredRevenue }}</span>
      </div>
      <div class="kpi-footer">
        <span class="trend-badge up-green">
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <path d="m18 15-6-6-6 6"/>
          </svg>
          {{ metrics.recoveredTrend }} <span class="trend-sub">vs last 7 days</span>
        </span>
        <svg class="kpi-sparkline" viewBox="0 0 60 20">
          <path d="M0 15 L 12 12 L 24 14 L 36 8 L 48 10 L 60 3" fill="none" stroke="#10b981" stroke-width="2" stroke-linecap="round"/>
        </svg>
      </div>
    </div>

    <!-- 2. Net Recovery Rate -->
    <div class="kpi-card">
      <div class="kpi-header">
        <span class="kpi-title">NET RECOVERY RATE</span>
      </div>
      <div class="kpi-value-row">
        <span class="kpi-value">{{ metrics.netRecoveryRate }}</span>
      </div>
      <div class="kpi-footer">
        <span class="trend-badge up-green">
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <path d="m18 15-6-6-6 6"/>
          </svg>
          {{ metrics.netRateTrend }} <span class="trend-sub">vs last 7 days</span>
        </span>
        <svg class="kpi-sparkline" viewBox="0 0 60 20">
          <path d="M0 16 L 15 13 L 30 11 L 45 7 L 60 4" fill="none" stroke="#10b981" stroke-width="2" stroke-linecap="round"/>
        </svg>
      </div>
    </div>

    <!-- 3. Margin Improvement -->
    <div class="kpi-card">
      <div class="kpi-header">
        <span class="kpi-title">MARGIN IMPROVEMENT</span>
      </div>
      <div class="kpi-value-row">
        <span class="kpi-value">{{ metrics.marginImprovement }}</span>
      </div>
      <div class="kpi-footer">
        <span class="trend-badge up-green">
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <path d="m18 15-6-6-6 6"/>
          </svg>
          {{ metrics.marginTrend }} <span class="trend-sub">vs last 7 days</span>
        </span>
        <svg class="kpi-sparkline" viewBox="0 0 60 20">
          <path d="M0 14 L 14 15 L 28 9 L 42 10 L 60 4" fill="none" stroke="#10b981" stroke-width="2" stroke-linecap="round"/>
        </svg>
      </div>
    </div>

    <!-- 4. Useless Retries Avoided -->
    <div class="kpi-card">
      <div class="kpi-header">
        <span class="kpi-title">USELESS RETRIES AVOIDED</span>
      </div>
      <div class="kpi-value-row">
        <span class="kpi-value">{{ metrics.retriesAvoided }}</span>
      </div>
      <div class="kpi-footer">
        <span class="trend-badge up-green">
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <path d="m18 15-6-6-6 6"/>
          </svg>
          {{ metrics.avoidedTrend }} <span class="trend-sub">vs last 7 days</span>
        </span>
        <svg class="kpi-sparkline" viewBox="0 0 60 20">
          <path d="M0 16 L 15 18 L 30 16 L 40 8 L 50 12 L 60 6" fill="none" stroke="#10b981" stroke-width="2" stroke-linecap="round"/>
        </svg>
      </div>
    </div>

    <!-- 5. Critical Alerts -->
    <div class="kpi-card alert-card">
      <div class="kpi-header">
        <span class="kpi-title alert-title">CRITICAL ALERTS</span>
      </div>
      <div class="kpi-value-row">
        <span class="kpi-value alert-val">{{ metrics.criticalAlerts }}</span>
      </div>
      <div class="kpi-footer">
        <span class="alert-subtext">
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"/>
            <polyline points="12 6 12 12 16 14"/>
          </svg>
          Requires attention
        </span>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
defineProps<{
  metrics: {
    recoveredRevenue: string;
    recoveredTrend: string;
    netRecoveryRate: string;
    netRateTrend: string;
    marginImprovement: string;
    marginTrend: string;
    retriesAvoided: string;
    avoidedTrend: string;
    criticalAlerts: number;
  }
}>();
</script>

<style scoped>
.kpi-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 14px;
}

.kpi-card {
  background-color: var(--bg-card, #0f172a);
  border: 1px solid var(--border-card, #1e293b);
  border-radius: 12px;
  padding: 16px 18px 14px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.kpi-title {
  font-size: 11px;
  font-weight: 700;
  color: #94a3b8;
  letter-spacing: 0.5px;
}

.kpi-value-row {
  margin: 10px 0 8px;
}

.kpi-value {
  font-size: 22px;
  font-weight: 800;
  color: #f8fafc;
  letter-spacing: -0.5px;
}

.kpi-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.trend-badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 11px;
  font-weight: 700;
}
.up-green { color: #34d399; }
.trend-sub { color: #64748b; font-weight: 400; font-size: 10px; }

.kpi-sparkline {
  width: 54px;
  height: 18px;
}

.alert-card {
  border-color: rgba(239, 68, 68, 0.4);
  background: rgba(239, 68, 68, 0.05);
}

.alert-title { color: #f87171; }
.alert-val { color: #ef4444; }
.alert-subtext {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 11px;
  color: #fca5a5;
}

@media (max-width: 1300px) {
  .kpi-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}
@media (max-width: 900px) {
  .kpi-grid {
    grid-template-columns: 1fr;
  }
}
</style>
