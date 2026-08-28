<template>
  <div class="card card-engine-flow">
    <div class="card-header">
      <div class="card-header-left">
        <div>
          <div class="header-title-row">
            <span class="card-title">AI SHIELD ENGINE</span>
            <span class="live-badge">Live</span>
          </div>
          <div class="card-subtitle">Real-time decision intelligence flow</div>
        </div>
      </div>
      <button class="card-action-btn" @click="emitInsights">View Engine Insights</button>
    </div>

    <!-- Interactive Node Graph Flow -->
    <div class="engine-flow-container">
      
      <!-- Node 1: Failed Payments -->
      <div class="flow-step">
        <div class="flow-node-box node-blue">
          <span class="flow-tag text-blue">FAILED PAYMENTS</span>
          <span class="flow-sub" style="margin-top: 10px;">Total</span>
          <span class="flow-val">{{ engineData.failedPayments.toLocaleString() }}</span>
          <span class="flow-sub">100%</span>
        </div>
      </div>

      <div class="flow-arrow-divider">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M5 12h14M12 5l7 7-7 7"/>
        </svg>
      </div>

      <!-- Node 2: Classification -->
      <div class="flow-step">
        <span class="step-label">CLASSIFICATION</span>
        <div class="flow-group">
          <div class="flow-node-box node-danger">
            <span class="flow-tag text-red">HARD DECLINE</span>
            <span class="flow-val">{{ engineData.classification.hardDecline.count.toLocaleString() }}</span>
            <span class="flow-sub">{{ engineData.classification.hardDecline.pct }}</span>
          </div>
          <div class="flow-node-box node-warning">
            <span class="flow-tag text-amber">SOFT DECLINE</span>
            <span class="flow-val">{{ engineData.classification.softDecline.count.toLocaleString() }}</span>
            <span class="flow-sub">{{ engineData.classification.softDecline.pct }}</span>
          </div>
          <div class="flow-node-box node-purple">
            <span class="flow-tag text-purple">UNCERTAIN</span>
            <span class="flow-val">{{ engineData.classification.uncertain.count.toLocaleString() }}</span>
            <span class="flow-sub">{{ engineData.classification.uncertain.pct }}</span>
          </div>
        </div>
      </div>

      <div class="flow-arrow-divider">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#ef4444" stroke-width="2">
          <path d="M5 12h14M12 5l7 7-7 7"/>
        </svg>
      </div>

      <!-- Node 3: Expected Value Gate -->
      <div class="flow-step">
        <span class="step-label">EXPECTED VALUE GATE</span>
        <div class="flow-group">
          <div class="flow-node-box node-success">
            <span class="flow-tag text-green">PROCEED</span>
            <span class="flow-val">{{ engineData.evGate.proceed.count.toLocaleString() }}</span>
            <span class="flow-sub">{{ engineData.evGate.proceed.pct }}</span>
          </div>
          <div class="flow-node-box node-dark">
            <span class="flow-tag text-muted">SKIP</span>
            <span class="flow-val">{{ engineData.evGate.skip.count.toLocaleString() }}</span>
            <span class="flow-sub">{{ engineData.evGate.skip.pct }}</span>
          </div>
        </div>
      </div>

      <div class="flow-arrow-divider">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2">
          <path d="M5 12h14M12 5l7 7-7 7"/>
        </svg>
      </div>

      <!-- Node 4: Retry Intelligence -->
      <div class="flow-step">
        <span class="step-label">RETRY INTELLIGENCE</span>
        <div class="flow-group">
          <div class="flow-node-box node-blue">
            <span class="flow-tag text-blue">SCHEDULED RETRIES</span>
            <span class="flow-val">{{ engineData.retryIntelligence.scheduledRetries.toLocaleString() }}</span>
          </div>
          <div class="flow-node-box timing-box">
            <span class="flow-tag" style="font-size: 9px; color: var(--text-muted, #64748b);">TIMING OPTIMIZED</span>
            <span class="flow-sub" style="font-size: 9.5px; line-height: 1.3; color: var(--text-secondary, #94a3b8);">{{ engineData.retryIntelligence.timingOptimized }}</span>
          </div>
        </div>
      </div>

      <div class="flow-arrow-divider">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#3b82f6" stroke-width="2">
          <path d="M5 12h14M12 5l7 7-7 7"/>
        </svg>
      </div>

      <!-- Node 5: Outcomes -->
      <div class="flow-step">
        <span class="step-label">OUTCOMES</span>
        <div class="flow-group">
          <div class="flow-node-box node-success">
            <span class="flow-tag text-green">RECOVERED</span>
            <span class="flow-val">{{ engineData.outcomes.recovered.amount }}</span>
            <span class="flow-sub">{{ engineData.outcomes.recovered.pct }}</span>
          </div>
          <div class="flow-node-box node-dark">
            <span class="flow-tag text-muted">NOT RECOVERED</span>
            <span class="flow-val">{{ engineData.outcomes.notRecovered.amount }}</span>
            <span class="flow-sub">{{ engineData.outcomes.notRecovered.pct }}</span>
          </div>
        </div>
      </div>

    </div>

    <!-- Systemic Alert Bottom Ribbon -->
    <div class="systemic-alert-ribbon">
      <div class="alert-ribbon-left">
        <span class="alert-ribbon-icon">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
            <line x1="12" y1="8" x2="12" y2="12"/>
            <line x1="12" y1="16" x2="12.01" y2="16"/>
          </svg>
        </span>
        <div>
          <span class="alert-ribbon-tag">{{ engineData.alert.title }}</span>
          <span class="alert-ribbon-msg">{{ engineData.alert.message }}</span>
        </div>
      </div>
      <a :href="engineData.alert.target" class="alert-ribbon-link">
        View Patterns
        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
          <path d="M5 12h14M12 5l7 7-7 7"/>
        </svg>
      </a>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  engineData: any
}>();

const emit = defineEmits(['insights']);
const emitInsights = () => {
  emit('insights');
};
</script>

<style scoped>
.card {
  background-color: var(--bg-card, #0f172a);
  border: 1px solid var(--border-card, #1e293b);
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.card-header {
  padding: 16px 20px 12px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.header-title-row {
  display: flex;
  align-items: center;
  gap: 8px;
}

.card-title {
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 0.4px;
  color: var(--text-primary, #f8fafc);
  text-transform: uppercase;
}

.card-subtitle {
  font-size: 11.5px;
  color: var(--text-muted, #64748b);
  margin-top: 2px;
}

.live-badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 10.5px;
  font-weight: 600;
  color: #10b981;
  background-color: rgba(16, 185, 129, 0.12);
  border: 1px solid rgba(16, 185, 129, 0.3);
  padding: 1px 7px;
  border-radius: 12px;
}

.card-action-btn {
  font-size: 11px;
  font-weight: 600;
  color: var(--text-secondary, #94a3b8);
  background-color: rgba(255, 255, 255, 0.03);
  border: 1px solid var(--border-card, #1e293b);
  padding: 5px 10px;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.15s ease;
}

.card-action-btn:hover {
  color: #f8fafc;
  border-color: #3b82f6;
}

.engine-flow-container {
  padding: 20px 24px 22px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  overflow-x: auto;
}

.flow-step {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  flex: 1;
  min-width: 140px;
}

.step-label {
  font-size: 9.5px;
  font-weight: 700;
  letter-spacing: 0.6px;
  color: var(--text-muted, #64748b);
  text-transform: uppercase;
}

.flow-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
  width: 100%;
}

.flow-node-box {
  background-color: rgba(255, 255, 255, 0.02);
  border: 1px solid var(--border-card, #1e293b);
  border-radius: 8px;
  padding: 10px 12px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  transition: all 0.2s ease;
}

.flow-node-box:hover {
  transform: translateY(-2px);
}

.node-blue { border-color: rgba(59, 130, 246, 0.4); background: rgba(59, 130, 246, 0.06); }
.node-danger { border-color: rgba(239, 68, 68, 0.4); background: rgba(239, 68, 68, 0.06); }
.node-warning { border-color: rgba(245, 158, 11, 0.4); background: rgba(245, 158, 11, 0.06); }
.node-purple { border-color: rgba(168, 85, 247, 0.4); background: rgba(168, 85, 247, 0.06); }
.node-success { border-color: rgba(16, 185, 129, 0.4); background: rgba(16, 185, 129, 0.06); }
.node-dark { border-color: rgba(255, 255, 255, 0.06); background: rgba(0, 0, 0, 0.2); }

.flow-tag { font-size: 10px; font-weight: 700; letter-spacing: 0.3px; }
.text-blue { color: #60a5fa; }
.text-red { color: #f87171; }
.text-amber { color: #fbbf24; }
.text-purple { color: #c084fc; }
.text-green { color: #34d399; }
.text-muted { color: #64748b; }

.flow-val { font-size: 14px; font-weight: 700; color: #f8fafc; margin: 2px 0 1px; }
.flow-sub { font-size: 10.5px; color: #64748b; }

.flow-arrow-divider {
  display: flex;
  align-items: center;
  color: #475569;
  opacity: 0.8;
}

.systemic-alert-ribbon {
  background: rgba(239, 68, 68, 0.1);
  border-top: 1px solid rgba(239, 68, 68, 0.25);
  padding: 10px 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.alert-ribbon-left {
  display: flex;
  align-items: center;
  gap: 10px;
}

.alert-ribbon-icon {
  color: #ef4444;
  display: flex;
  align-items: center;
}

.alert-ribbon-tag {
  font-size: 10px;
  font-weight: 800;
  color: #f87171;
  background: rgba(239, 68, 68, 0.2);
  padding: 2px 6px;
  border-radius: 4px;
  margin-right: 8px;
}

.alert-ribbon-msg {
  font-size: 12px;
  color: #fca5a5;
}

.alert-ribbon-link {
  font-size: 11.5px;
  font-weight: 600;
  color: #f87171;
  display: inline-flex;
  align-items: center;
  gap: 4px;
  text-decoration: none;
}
</style>
