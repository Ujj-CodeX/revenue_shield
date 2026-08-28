<template>
  <aside class="sidebar-container">
    <!-- Brand Logo -->
    <div class="sidebar-brand">
      <div class="brand-icon">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2">
          <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
          <path d="m9 12 2 2 4-4"/>
        </svg>
      </div>
      <div class="brand-text">
        <span class="brand-title">PAYSHIELD</span>
        <span class="brand-sub">INTELLIGENCE</span>
      </div>
    </div>

    <!-- Navigation Links -->
    <nav class="sidebar-nav">
      <div class="nav-section-title">MAIN MENU</div>
      <a href="#overview" class="nav-link active">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <rect width="7" height="9" x="3" y="3" rx="1"/><rect width="7" height="5" x="14" y="3" rx="1"/>
          <rect width="7" height="9" x="14" y="12" rx="1"/><rect width="7" height="5" x="3" y="16" rx="1"/>
        </svg>
        <span>Overview</span>
      </a>

      <a href="#action-center" class="nav-link">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>
        </svg>
        <span>Action Center</span>
        <span class="nav-badge">12</span>
      </a>

      <a href="#systemic-patterns" class="nav-link">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M3 3v18h18"/><path d="m19 9-5 5-4-4-3 3"/>
        </svg>
        <span>Systemic Patterns</span>
      </a>

      <a href="#backtest" class="nav-link">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/>
        </svg>
        <span>Backtest Lab</span>
      </a>

      <a href="#audit" class="nav-link">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 14 14"/>
        </svg>
        <span>Audit Trail</span>
      </a>
    </nav>

    <!-- Health Widget -->
    <div class="sidebar-health-widget">
      <div class="health-widget-title">SYSTEM HEALTH SCORE</div>
      <div class="health-circle-wrap">
        <svg class="health-gauge" viewBox="0 0 36 36">
          <path class="gauge-bg" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"/>
          <path class="gauge-progress" stroke-dasharray="91, 100" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"/>
        </svg>
        <div class="health-score-val">
          <span class="score-number">{{ healthScore }}</span>
          <span class="score-grade">A+</span>
        </div>
      </div>
      <div class="health-caption">Optimal Recovery Flow</div>
    </div>
  </aside>
</template>

<script setup lang="ts">
defineProps<{
  healthScore: number;
  isLightMode: boolean;
}>();

defineEmits(['toggle-theme']);
</script>

<style scoped>
.sidebar-container {
  width: 240px;
  background-color: var(--bg-sidebar, #090d16);
  border-right: 1px solid var(--border-card, #1e293b);
  display: flex;
  flex-direction: column;
  padding: 20px 16px;
  gap: 24px;
}

.sidebar-brand {
  display: flex;
  align-items: center;
  gap: 10px;
}

.brand-icon {
  width: 34px;
  height: 34px;
  background: linear-gradient(135deg, #2563eb, #3b82f6);
  color: #fff;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.brand-text {
  display: flex;
  flex-direction: column;
}
.brand-title { font-size: 13px; font-weight: 800; letter-spacing: 0.8px; color: #f8fafc; }
.brand-sub { font-size: 9px; font-weight: 700; color: #3b82f6; letter-spacing: 1px; }

.sidebar-nav {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.nav-section-title {
  font-size: 9.5px;
  font-weight: 700;
  color: #64748b;
  letter-spacing: 0.8px;
  margin-bottom: 6px;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 9px 12px;
  border-radius: 8px;
  font-size: 12.5px;
  font-weight: 600;
  color: #94a3b8;
  text-decoration: none;
  transition: all 0.15s ease;
}

.nav-link:hover {
  background: rgba(255, 255, 255, 0.04);
  color: #f8fafc;
}

.nav-link.active {
  background: rgba(59, 130, 246, 0.12);
  color: #60a5fa;
  border: 1px solid rgba(59, 130, 246, 0.25);
}

.nav-badge {
  margin-left: auto;
  background: #2563eb;
  color: #fff;
  font-size: 10px;
  padding: 1px 6px;
  border-radius: 10px;
}

.sidebar-health-widget {
  margin-top: auto;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid var(--border-card, #1e293b);
  border-radius: 10px;
  padding: 14px;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.health-widget-title { font-size: 9.5px; font-weight: 700; color: #64748b; margin-bottom: 8px; }

.health-circle-wrap {
  position: relative;
  width: 72px;
  height: 72px;
}

.health-gauge {
  width: 100%;
  height: 100%;
  transform: rotate(-90deg);
}

.gauge-bg {
  fill: none;
  stroke: rgba(255, 255, 255, 0.05);
  stroke-width: 3.5;
}

.gauge-progress {
  fill: none;
  stroke: #10b981;
  stroke-width: 3.5;
  stroke-linecap: round;
}

.health-score-val {
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.score-number { font-size: 16px; font-weight: 800; color: #f8fafc; }
.score-grade { font-size: 9px; font-weight: 700; color: #34d399; }
.health-caption { font-size: 10.5px; color: #94a3b8; margin-top: 6px; }

@media (max-width: 1024px) {
  .sidebar-container {
    display: none;
  }
}
</style>
