<template>
  <div id="revenue-shield-root" class="w-100 min-vh-100 text-terminal-main bg-terminal-main">
    <!-- State 1: Hero / Landing Screen -->
    <HeroSection 
      v-if="currentState === 'hero'"
      @start="goToSelectMerchant"
    />

    <!-- State 2: Merchant Selection Screen -->
    <MerchantSelect 
      v-else-if="currentState === 'select-merchant'"
      @select-merchant="onSelectMerchant"
      @back="goToHero"
    />

    <!-- State 3: Staged Loading Overlay (Initial Ingestion) -->
    <LoadingOverlay 
      v-else-if="currentState === 'loading'"
      :active="true"
      :merchant-id="selectedMerchantId"
      :seed="currentSeed"
      mode="initial"
      @complete="onInitialLoadComplete"
    />

    <!-- State 4: Merchant Dashboard View with In-Place Rerun Overlay -->
    <div 
      v-else-if="currentState === 'dashboard'" 
      class="position-relative w-100 min-vh-100"
      id="dashboard-wrapper"
    >
      <!-- Quick Navigation Bar for Switching Merchant / Returning to Analysis -->
      <div class="quick-nav-bar d-flex align-items-center justify-content-between px-3 py-2 font-mono fs-8" id="quick-nav-bar">
        <div class="d-flex align-items-center gap-2">
          <span class="text-terminal-green fw-bold">&#9632; REVENUE SHIELD AI</span>
          <span class="text-terminal-muted">|</span>
          <span class="text-terminal-bright">{{ dashboardData?.merchantContext?.merchantName || selectedMerchantId }}</span>
          <span class="badge-plan-sm">{{ dashboardData?.merchantContext?.plan || 'Active' }}</span>
        </div>
        <div class="d-flex align-items-center gap-2">
          <button 
            type="button" 
            class="btn-nav-switch" 
            id="btn-switch-merchant" 
            @click="goToSelectMerchant"
          >
            &#8644; Switch Merchant
          </button>
          <button 
            type="button" 
            class="btn-nav-switch" 
            id="btn-return-hero" 
            @click="goToHero"
          >
            &#8634; Restart Analysis
          </button>
        </div>
      </div>

      <!-- Main Operational Merchant Dashboard -->
      <MerchantDashboard 
        v-if="dashboardData"
        :merchant="dashboardData.merchantContext"
        :kpi-metrics="dashboardData.kpiMetrics"
        :failed-payments="dashboardData.failedPaymentsData"
        :bucket-summary="dashboardData.bucketSummaryData"
        :hard-decline-report="dashboardData.hardDeclineReportData"
        :backtest="dashboardData.backtestData"
        @rerun="triggerRerunBacktest"
      />

      <!-- Staged Loading Overlay for In-Place Backtest Re-Runs (Does not leave dashboard) -->
      <LoadingOverlay 
        v-if="isRerunLoading"
        :active="isRerunLoading"
        :merchant-id="selectedMerchantId"
        :seed="rerunSeed"
        mode="rerun"
        @complete="onRerunComplete"
      />
    </div>
  </div>
</template>

<script>
import HeroSection from './components/HeroSection.vue';
import MerchantSelect from './components/MerchantSelect.vue';
import LoadingOverlay from './components/LoadingOverlay.vue';
import MerchantDashboard from './views/MerchantDashboard.vue';

export default {
  name: 'App',
  components: {
    HeroSection,
    MerchantSelect,
    LoadingOverlay,
    MerchantDashboard
  },
  data() {
    return {
      currentState: 'hero', // 'hero' -> 'select-merchant' -> 'loading' -> 'dashboard'
      selectedMerchantId: 'MERCH_001',
      currentSeed: 42,
      dashboardData: null,
      isRerunLoading: false,
      rerunSeed: null
    };
  },
  methods: {
    goToHero() {
      this.currentState = 'hero';
    },
    goToSelectMerchant() {
      this.currentState = 'select-merchant';
    },
    onSelectMerchant(merchantId) {
      this.selectedMerchantId = merchantId;
      this.currentSeed = 42;
      this.currentState = 'loading';
    },
    onInitialLoadComplete(data) {
      if (data) {
        this.dashboardData = data;
      }
      this.currentState = 'dashboard';
    },
    triggerRerunBacktest(payload) {
      const seed = (payload && payload.seed) ? payload.seed : Math.floor(Math.random() * 10000) + 1;
      this.rerunSeed = seed;
      this.isRerunLoading = true;
    },
    onRerunComplete(updatedData) {
      if (updatedData) {
        this.dashboardData = updatedData;
      }
      this.isRerunLoading = false;
    }
  }
};
</script>

<style scoped>
.quick-nav-bar {
  background-color: var(--bg-panel-header, #0B101D);
  border-bottom: 1px solid var(--border-color, #1D2738);
  color: var(--text-muted, #6C7A9C);
}

.badge-plan-sm {
  background: rgba(77, 163, 255, 0.12);
  border: 1px solid rgba(77, 163, 255, 0.3);
  color: var(--accent-blue, #4DA3FF);
  padding: 1px 6px;
  font-size: 10px;
}

.btn-nav-switch {
  background: transparent;
  border: 1px solid var(--border-color, #1D2738);
  color: var(--text-muted, #6C7A9C);
  font-family: var(--font-mono, monospace);
  font-size: 11px;
  padding: 3px 10px;
  cursor: pointer;
  transition: all 0.15s ease;
}

.btn-nav-switch:hover {
  color: var(--accent-green, #7CFC6A);
  border-color: var(--accent-green, #7CFC6A);
  background: rgba(124, 252, 106, 0.05);
}

.fs-8 {
  font-size: 0.72rem;
}
</style>
