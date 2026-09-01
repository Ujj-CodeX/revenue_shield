<template>
  <div class="terminal-panel" id="backtest-panel">
    <div class="terminal-panel-header" id="backtest-header">
      <span>BACKTEST</span>
      <span class="subtitle">(POLICY VS NAIVE RETRY EVERYTHING)</span>
    </div>

    <!-- Comparative Columns -->
    <div class="backtest-comparison-grid" id="backtest-comparison-grid">
      <!-- Col 1: Policy Recovered Revenue -->
      <div class="backtest-col" id="col-policy-revenue">
        <div class="backtest-metric-label" id="lbl-policy-revenue">POLICY RECOVERED REVENUE</div>
        <div class="backtest-metric-value text-terminal-green" id="val-policy-revenue">
          {{ backtest.policyRecoveredRevenue }}
        </div>
        <div class="backtest-metric-subtext" id="sub-policy-retries">
          From {{ backtest.policyRetries }} retries
        </div>
      </div>

      <!-- VS Indicator -->
      <div class="backtest-vs" id="backtest-vs-divider">VS</div>

      <!-- Col 2: Naive Retry Recovered Revenue -->
      <div class="backtest-col" id="col-naive-revenue">
        <div class="backtest-metric-label" id="lbl-naive-revenue">NAIVE RETRY RECOVERED REVENUE</div>
        <div class="backtest-metric-value text-terminal-red" id="val-naive-revenue">
          {{ backtest.naiveRetryRecoveredRevenue }}
        </div>
        <div class="backtest-metric-subtext" id="sub-naive-retries">
          From {{ backtest.naiveRetries }} retries
        </div>
      </div>

      <!-- Col 3: Improvement -->
      <div class="backtest-col" id="col-improvement">
        <div class="backtest-metric-label" id="lbl-improvement">IMPROVEMENT</div>
        <div class="backtest-metric-value text-terminal-green" id="val-improvement">
          {{ backtest.improvement }}
        </div>
        <div class="backtest-metric-subtext text-terminal-green" id="sub-improvement-pct">
          ({{ backtest.improvementPercentage }})
        </div>
      </div>
    </div>

    <!-- Bottom Actions & Retries Avoided -->
    <div class="backtest-actions-row flex-wrap" id="backtest-actions-row">
      <div id="retries-avoided-group">
        <div class="backtest-metric-label" id="lbl-retries-avoided">RETRIES AVOIDED</div>
        <div class="fs-5 fw-bold text-terminal-bright" id="val-retries-avoided">
          {{ backtest.retriesAvoided }} <span class="text-terminal-muted fs-6 fw-normal">({{ backtest.retriesAvoidedPercentage }})</span>
        </div>
      </div>

      <div class="mt-2 mt-sm-0" id="rerun-btn-wrap">
        <button 
          type="button" 
          class="btn-terminal-outline btn-sm" 
          id="btn-rerun-backtest" 
          :disabled="isRunning"
          @click="rerunBacktest"
        >
          <span v-if="!isRunning">&#9658; RE-RUN BACKTEST</span>
          <span v-else>&#8635; SIMULATING RUN...</span>
        </button>
      </div>
    </div>

    <!-- Footer metadata -->
    <div class="backtest-footer-info d-flex flex-wrap align-items-center gap-1" id="backtest-footer-info">
      <span>{{ backtest.baselineDescription }}</span>
      <span class="d-none d-sm-inline mx-1">|</span>
      <span class="text-terminal-green">Seed: {{ backtest.seed }}</span>
      <span class="d-none d-sm-inline mx-1">|</span>
      <span>Run ID: {{ currentRunId }}</span>
    </div>
  </div>
</template>

<script>
export default {
  name: 'BacktestPanel',
  props: {
    backtest: {
      type: Object,
      required: true
    }
  },
  emits: ['rerun'],
    data() {
    return {
      isRunning: false,
      currentRunId: this.backtest.runId
    };
  },
  methods: {
    async rerunBacktest() {
      this.isRunning = true;
      this.$emit('rerun');
      this.isRunning = false;
    }
  }

};
</script>
