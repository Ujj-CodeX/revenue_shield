<template>
  <div class="merchant-select-screen min-vh-100 d-flex flex-column justify-content-between p-3 p-md-5" id="merchant-select-root">
    <!-- Top System Header -->
    <header class="d-flex flex-wrap align-items-center justify-content-between border-bottom border-dark pb-3 mb-4" id="merchant-select-header">
      <div class="d-flex align-items-center gap-3">
        <button 
          type="button" 
          class="btn-back-nav font-mono fs-8" 
          id="btn-back-to-hero" 
          @click="$emit('back')"
        >
          &larr; BACK
        </button>
        <span class="text-terminal-muted font-mono fs-8 d-none d-sm-inline">|</span>
        <div class="text-terminal-bright fw-bold font-mono fs-7">
          STEP 01 // SELECT RECURRING BILLING MERCHANT
        </div>
      </div>
      <div class="font-mono fs-8 text-terminal-muted mt-2 mt-sm-0">
        ENDPOINT: <span class="text-terminal-green">GET /api/merchants/</span> &bull; 
        RECORDS: <span class="text-terminal-bright">{{ merchants.length }}</span>
      </div>
    </header>

    <!-- Main Content Area -->
    <main class="container-xl my-auto py-3" id="merchant-select-main">
      <div class="text-center mb-4">
        <div class="terminal-tag mb-2">
          <span class="text-terminal-green">&#9658; TARGET ACQUISITION</span>
          <span class="mx-2 text-terminal-muted">|</span>
          <span class="text-terminal-muted">SELECT PORTFOLIO FOR OPERATIONAL AUDIT</span>
        </div>
        <h2 class="text-terminal-bright font-mono fw-bold fs-3 mb-2">Choose a Merchant for Recovery Analysis</h2>
        <p class="text-terminal-muted font-mono fs-7 max-w-600 mx-auto">
          Select a recurring subscription portfolio to run classification, EV policy gating, and counterfactual recovery backtesting.
        </p>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="text-center py-5 font-mono" id="merchants-loading">
        <div class="spinner-border text-terminal-green mb-3" role="status">
          <span class="visually-hidden">Loading merchants...</span>
        </div>
        <div class="text-terminal-muted fs-7">FETCHING /api/merchants/...</div>
      </div>

      <!-- Error State with Retry -->
      <div v-else-if="error" class="text-center py-4 font-mono" id="merchants-error">
        <div class="text-danger mb-2">API NOTICE: {{ error }}</div>
        <button type="button" class="btn-terminal-outline btn-sm" @click="loadMerchants">RETRY FETCH</button>
      </div>

      <!-- Selectable Merchants Grid -->
      <div v-else class="merchants-grid" id="merchants-grid">
        <div 
          v-for="merchant in merchants" 
          :key="merchant.id" 
          class="merchant-card" 
          :id="`merchant-card-${merchant.id}`"
          @click="handleSelect(merchant.id)"
        >
          <!-- 1. Merchant Name -->
          <h3 class="merchant-name text-terminal-bright font-mono fs-5 fw-bold mb-2">
            {{ merchant.name }}
          </h3>

          <!-- 2. MERCH_ID + Status badge -->
          <div class="d-flex align-items-center justify-content-between mb-2">
            <span class="badge-merchant-id font-mono">{{ merchant.id }}</span>
            <span class="badge-status-dot font-mono">
              <span class="dot-green"></span> ACTIVE
            </span>
          </div>

          <!-- 3. Industry tag + Tier tag -->
          <div class="d-flex flex-wrap align-items-center gap-2 mb-3">
            <span class="badge-industry font-mono">{{ merchant.industry }}</span>
            <span class="badge-plan font-mono">{{ merchant.plan }} Tier</span>
          </div>

          <!-- 4. Cohort / Gateway metadata block -->
          <div class="merchant-card-stats p-2 mb-3 font-mono fs-8">
            <div class="d-flex justify-content-between text-terminal-muted mb-1">
              <span>SIMULATION COHORT</span>
              <span class="text-terminal-bright">200 Users / 4 Mo</span>
            </div>
            <div class="d-flex justify-content-between text-terminal-muted">
              <span>GATEWAY INTEGRATION</span>
              <span class="text-terminal-green">DIRECT // EV GATED</span>
            </div>
          </div>

          <!-- 5. Action Button -->
          <button 
            type="button" 
            class="btn-select-merchant font-mono fs-8 fw-bold w-100 mt-auto"
            :id="`btn-select-${merchant.id}`"
          >
            <span>SELECT MERCHANT & ANALYZE</span>
            <span class="btn-arrow">&rarr;</span>
          </button>
        </div>
      </div>
    </main>

    <!-- Footer Status -->
    <footer class="border-top border-dark pt-3 font-mono fs-8 text-terminal-muted d-flex flex-wrap justify-content-between align-items-center" id="merchant-select-footer">
      <div>AUTOMATED SELECTION PROFILES CONFIGURED</div>
      <div>READY FOR STAGED INGESTION</div>
    </footer>
  </div>
</template>

<script>
import { fetchMerchants } from '@/services/api';

export default {
  name: 'MerchantSelect',
  emits: ['select-merchant', 'back'],
  data() {
    return {
      merchants: [],
      loading: true,
      error: null
    };
  },
  async mounted() {
    await this.loadMerchants();
  },
  methods: {
    async loadMerchants() {
      this.loading = true;
      this.error = null;
      try {
        const data = await fetchMerchants();
        this.merchants = data;
      } catch (err) {
        this.error = err.message;
      } finally {
        this.loading = false;
      }
    },
    handleSelect(merchantId) {
      this.$emit('select-merchant', merchantId);
    }
  }
};
</script>

<style scoped>
.merchant-select-screen {
  background-color: var(--bg-main, #070B14);
  color: var(--text-main, #D8DEE9);
  position: relative;
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

.max-w-600 {
  max-width: 600px;
}

.btn-back-nav {
  background: transparent;
  border: 1px solid var(--border-color, #1D2738);
  color: var(--text-muted, #6C7A9C);
  padding: 4px 12px;
  cursor: pointer;
  transition: all 0.15s ease;
}

.btn-back-nav:hover {
  color: var(--text-bright, #F0F4FC);
  border-color: var(--accent-green, #7CFC6A);
}

.merchants-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 20px;
  max-width: 1120px;
  margin: 0 auto;
}

@media (min-width: 640px) {
  .merchants-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1024px) {
  .merchants-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

.merchant-card {
  background: var(--bg-panel, #0E1422);
  border: 1px solid var(--border-color, #1D2738);
  padding: 20px;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
  display: flex;
  flex-direction: column;
  min-height: 290px;
  box-sizing: border-box;
}

.merchant-card:hover {
  border-color: var(--accent-green, #7CFC6A);
  transform: translateY(-2px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4), 0 0 12px rgba(124, 252, 106, 0.15);
}

.merchant-card:hover .btn-select-merchant {
  background: rgba(124, 252, 106, 0.15);
  border-color: var(--accent-green, #7CFC6A);
  color: #92FF83;
}

.merchant-card:hover .btn-arrow {
  transform: translateX(4px);
}

.badge-merchant-id {
  font-size: 10px;
  color: var(--accent-green, #7CFC6A);
  background: rgba(124, 252, 106, 0.08);
  border: 1px solid rgba(124, 252, 106, 0.3);
  padding: 2px 8px;
}

.badge-status-dot {
  font-size: 10px;
  color: var(--text-muted, #6C7A9C);
  display: flex;
  align-items: center;
  gap: 5px;
}

.dot-green {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--accent-green, #7CFC6A);
  box-shadow: 0 0 6px var(--accent-green, #7CFC6A);
}

.merchant-name {
  line-height: 1.3;
}

.badge-industry {
  font-size: 10px;
  background: #0B101D;
  border: 1px solid var(--border-color, #1D2738);
  color: var(--text-main, #D8DEE9);
  padding: 2px 8px;
}

.badge-plan {
  font-size: 10px;
  background: rgba(77, 163, 255, 0.1);
  border: 1px solid rgba(77, 163, 255, 0.3);
  color: var(--accent-blue, #4DA3FF);
  padding: 2px 8px;
}

.merchant-card-stats {
  background: #070B14;
  border: 1px solid var(--border-color, #1D2738);
}

.btn-select-merchant {
  background: transparent;
  border: 1px solid var(--border-color, #1D2738);
  color: var(--text-muted, #6C7A9C);
  padding: 10px 14px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  cursor: pointer;
  transition: all 0.15s ease;
  margin-top: auto;
}

.btn-arrow {
  transition: transform 0.15s ease;
}

.fs-7 { font-size: 0.75rem; }
.fs-8 { font-size: 0.7rem; }
.fs-9 { font-size: 0.62rem; }
</style>
