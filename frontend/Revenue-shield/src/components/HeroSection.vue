<template>
  <div class="hero-screen min-vh-100 d-flex flex-column justify-content-between p-3 p-md-5" id="hero-section-root">
    <!-- Top System Telemetry Bar -->
    <header class="d-flex flex-wrap align-items-center justify-content-between border-bottom border-dark pb-3 mb-4" id="hero-header">
      <div class="d-flex align-items-center gap-3">
        <div class="terminal-shield-icon">
          <span class="pulse-dot"></span>
          <span class="icon-bracket">[</span>&#9632;<span class="icon-bracket">]</span>
        </div>
        <div>
          <div class="text-terminal-bright fw-bold tracking-wider fs-6 font-mono">REVENUE_SHIELD // SYSTEM_OPS</div>
          <div class="text-terminal-muted fs-8 font-mono">KERNEL V2.5.4 &bull; STOCHASTIC POLICY ENGINE</div>
        </div>
      </div>
      <div class="d-flex align-items-center gap-3 mt-2 mt-sm-0 font-mono fs-8">
        <span class="badge-status-live">&#9679; CLASSIFIER: ACTIVE</span>
        <span class="text-terminal-muted d-none d-md-inline">ENV: PRODUCTION</span>
        <span class="text-terminal-muted">LATENCY: 14ms</span>
      </div>
    </header>

    <!-- Main Hero Presentation -->
    <main class="hero-body container-xl my-auto py-4" id="hero-main-content">
      <div class="row align-items-center g-5">
        <div class="col-lg-7">
          <div class="terminal-tag mb-3">
            <span class="text-terminal-green">&#9654; SYSTEM INITIALIZATION</span>
            <span class="mx-2 text-terminal-muted">|</span>
            <span class="text-terminal-muted">ID: RS-CORE-902</span>
          </div>

          <h1 class="hero-title text-terminal-bright mb-3" id="hero-main-title">
            Revenue Shield AI <span class="text-terminal-green">—</span> <br />
            <span class="hero-subtitle">Operational Intelligence Copilot for Recurring Payment Recovery</span>
          </h1>

          <p class="hero-explainer text-terminal-muted mb-4 fs-6" id="hero-explainer-text">
            Identifies recoverable failed payments, avoids unnecessary retries, and proves recovery impact via counterfactual backtesting.
          </p>

          <div class="hero-action-group d-flex flex-wrap align-items-center gap-3 mb-4">
            <button 
              type="button" 
              class="btn-hero-primary" 
              id="btn-hero-start" 
              @click="$emit('start')"
            >
              <span class="btn-icon">&#9658;</span>
              <span>START ANALYSIS</span>
            </button>
            <div class="d-flex align-items-center gap-2 text-terminal-muted font-mono fs-8">
              <span class="text-terminal-green">&#10003;</span> Zero Setup &bull; Deterministic Seeds &bull; EV Gated
            </div>
          </div>

          <!-- Feature Matrix -->
          <div class="row g-3 pt-2 font-mono fs-7">
            <div class="col-sm-4">
              <div class="hero-spec-card">
                <div class="spec-label">STAGE 1 // CLASSIFIER</div>
                <div class="spec-value text-terminal-green">HARD / SOFT / UNCERTAIN</div>
                <div class="spec-desc">Deterministic rule tables + fallback triage</div>
              </div>
            </div>
            <div class="col-sm-4">
              <div class="hero-spec-card">
                <div class="spec-label">STAGE 2 // POLICY GATE</div>
                <div class="spec-value text-terminal-green">EV-POSITIVE RETRIES</div>
                <div class="spec-desc">Filters money-losing retries & bank outages</div>
              </div>
            </div>
            <div class="col-sm-4">
              <div class="hero-spec-card">
                <div class="spec-label">STAGE 3 // MEASUREMENT</div>
                <div class="spec-value text-terminal-green">BACKTEST PROOF</div>
                <div class="spec-desc">Mathematical lift vs naive baseline</div>
              </div>
            </div>
          </div>
        </div>

        <!-- Right Side Live Telemetry Preview Terminal -->
        <div class="col-lg-5">
          <div class="hero-terminal-window">
            <div class="terminal-window-header d-flex align-items-center justify-content-between">
              <div class="d-flex align-items-center gap-2">
                <span class="dot-red"></span>
                <span class="dot-yellow"></span>
                <span class="dot-green"></span>
                <span class="window-title ms-2 font-mono fs-8 text-terminal-muted">ops_console // live_metrics.log</span>
              </div>
              <span class="badge-tag font-mono fs-9">STANDALONE READY</span>
            </div>
            <div class="terminal-window-body font-mono fs-8 p-3">
              <div class="log-row">
                <span class="text-terminal-muted">[idle]</span>
                <span class="text-terminal-cyan ms-1">SYS_INGESTION:</span>
                <span class="text-terminal-main ms-1">Synthetic customer population initializing&hellip;</span>
              </div>
              <div class="log-row">
                <span class="text-terminal-muted">[idle]</span>
                <span class="text-terminal-green ms-1">GATEWAY_OBSERVABLE:</span>
                <span class="text-terminal-main ms-1">Awaiting live gateway event stream&hellip;</span>
              </div>
              <div class="log-row">
                <span class="text-terminal-muted">[idle]</span>
                <span class="text-terminal-amber ms-1">EV_GATE:</span>
                <span class="text-terminal-main ms-1">Standing by &mdash; no retries evaluated yet</span>
              </div>
              <div class="log-row">
                <span class="text-terminal-muted">[idle]</span>
                <span class="text-terminal-green ms-1">POLICY_ENGINE:</span>
                <span class="text-terminal-bright ms-1">Idle &mdash; press Start Analysis to run</span>
              </div>
              <div class="log-row-divider my-2"></div>
              <div class="metric-preview-block p-2">
                <div class="d-flex justify-content-between text-terminal-muted fs-8 mb-1">
                  <span>POLICY VS NAIVE BASELINE</span>
                  <span class="text-terminal-green fw-bold">COMPUTED LIVE ON START</span>
                </div>
                <div class="fs-7 text-terminal-bright fw-bold">₹ Recovered &bull; Lift % &bull; Retries Avoided %</div>
                <div class="fs-8 text-terminal-muted mt-1">Generated fresh from the backend when you press Start Analysis &mdash; nothing on this screen is precomputed.</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- Footer Terminal Bar -->
    <footer class="border-top border-dark pt-3 font-mono fs-8 text-terminal-muted d-flex flex-wrap justify-content-between align-items-center" id="hero-footer">
      <div>REVENUE SHIELD CORE ENGINE &bull; VERSION 2.5 &bull; STRICT RECOVERY AUDIT</div>
      <div class="mt-1 mt-sm-0">STOCHASTIC SEED READY &bull; PRESS START ANALYSIS TO INITIALIZE</div>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'HeroSection',
  emits: ['start']
};
</script>

<style scoped>
.hero-screen {
  background-color: var(--bg-main, #070B14);
  color: var(--text-main, #D8DEE9);
  position: relative;
  overflow-x: hidden;
}

.terminal-shield-icon {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  color: var(--accent-green, #7CFC6A);
  font-family: var(--font-mono, monospace);
  font-weight: 700;
}

.pulse-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: var(--accent-green, #7CFC6A);
  box-shadow: 0 0 8px var(--accent-green, #7CFC6A);
  display: inline-block;
  animation: pulse-glow 2s infinite ease-in-out;
}

@keyframes pulse-glow {
  0%, 100% { opacity: 0.9; transform: scale(1); }
  50% { opacity: 0.4; transform: scale(0.85); }
}

.badge-status-live {
  color: var(--accent-green, #7CFC6A);
  border: 1px solid rgba(124, 252, 106, 0.3);
  padding: 3px 8px;
  background: rgba(124, 252, 106, 0.06);
}

.terminal-tag {
  display: inline-flex;
  align-items: center;
  background: #0B101D;
  border: 1px solid var(--border-color, #1D2738);
  padding: 4px 10px;
  font-family: var(--font-mono, monospace);
  font-size: 11px;
}

.hero-title {
  font-family: var(--font-mono, monospace);
  font-size: clamp(24px, 3.5vw, 36px);
  line-height: 1.25;
  font-weight: 700;
  letter-spacing: -0.02em;
}

.hero-subtitle {
  color: var(--text-main, #D8DEE9);
  font-size: clamp(18px, 2.2vw, 24px);
  font-weight: 500;
}

.hero-explainer {
  max-width: 680px;
  line-height: 1.6;
}

.btn-hero-primary {
  background-color: var(--accent-green, #7CFC6A);
  color: #070B14;
  border: 1px solid var(--accent-green, #7CFC6A);
  font-family: var(--font-mono, monospace);
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 0.08em;
  padding: 12px 28px;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 10px;
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
  box-shadow: 0 0 16px rgba(124, 252, 106, 0.25);
}

.btn-hero-primary:hover {
  background-color: #92FF83;
  box-shadow: 0 0 24px rgba(124, 252, 106, 0.45);
  transform: translateY(-1px);
}

.btn-hero-primary:active {
  transform: translateY(0);
}

.hero-spec-card {
  background: var(--bg-panel, #0E1422);
  border: 1px solid var(--border-color, #1D2738);
  padding: 14px;
  transition: border-color 0.2s ease;
}

.hero-spec-card:hover {
  border-color: var(--accent-green, #7CFC6A);
}

.spec-label {
  font-size: 9px;
  color: var(--text-muted, #6C7A9C);
  letter-spacing: 0.06em;
  margin-bottom: 4px;
}

.spec-value {
  font-weight: 700;
  font-size: 11px;
  margin-bottom: 4px;
}

.spec-desc {
  font-size: 10px;
  color: var(--text-muted, #6C7A9C);
  line-height: 1.4;
}

.hero-terminal-window {
  background: var(--bg-panel, #0E1422);
  border: 1px solid var(--border-color, #1D2738);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
}

.terminal-window-header {
  background: var(--bg-panel-header, #0B101D);
  padding: 10px 14px;
  border-bottom: 1px solid var(--border-color, #1D2738);
}

.dot-red { width: 8px; height: 8px; border-radius: 50%; background: #FF5C5C; display: inline-block; }
.dot-yellow { width: 8px; height: 8px; border-radius: 50%; background: #FFC857; display: inline-block; }
.dot-green { width: 8px; height: 8px; border-radius: 50%; background: #7CFC6A; display: inline-block; }

.badge-tag {
  background: rgba(108, 122, 156, 0.15);
  color: var(--text-muted, #6C7A9C);
  padding: 2px 6px;
  border: 1px solid var(--border-color, #1D2738);
}

.log-row {
  margin-bottom: 6px;
  line-height: 1.4;
}

.log-row-divider {
  border-top: 1px dashed var(--border-color, #1D2738);
}

.metric-preview-block {
  background: #070B14;
  border: 1px solid rgba(124, 252, 106, 0.3);
}

.fs-7 { font-size: 0.75rem; }
.fs-8 { font-size: 0.7rem; }
.fs-9 { font-size: 0.62rem; }
</style>