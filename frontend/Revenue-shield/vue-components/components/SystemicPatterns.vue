<template>
  <div class="card card-systemic-patterns">
    <div class="card-header">
      <div>
        <span class="card-title">SYSTEMIC PATTERN DETECTION</span>
        <span class="card-subtitle">Last 24 hours</span>
      </div>
    </div>

    <!-- Tab Pills -->
    <div class="pattern-tabs">
      <button 
        v-for="tab in ['banks', 'gateways', 'methods']" 
        :key="tab"
        class="tab-pill" 
        :class="{ active: currentTab === tab }"
        @click="currentTab = tab"
      >
        {{ tab === 'banks' ? 'Banks' : (tab === 'gateways' ? 'Gateways' : 'Payment Methods') }}
      </button>
    </div>

    <!-- Table Content -->
    <div class="table-responsive">
      <table class="custom-table">
        <thead>
          <tr>
            <th>{{ currentTab === 'banks' ? 'BANK' : (currentTab === 'gateways' ? 'GATEWAY' : 'PAYMENT METHOD') }}</th>
            <th>HEALTH SCORE</th>
            <th>TREND (24H)</th>
            <th>FAILURE RATE</th>
            <th>STATUS</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in currentRows" :key="item.name">
            <td><strong>{{ item.name }}</strong></td>
            <td>
              <span class="score-indicator">
                <span class="score-dot" :class="item.scoreType"></span>
                {{ item.score }}
              </span>
            </td>
            <td>
              <svg width="48" height="16" viewBox="0 0 48 16" fill="none">
                <path 
                  :d="generateSparkline(item.trend)" 
                  :stroke="item.scoreType === 'green' ? '#10b981' : (item.scoreType === 'amber' ? '#f59e0b' : '#ef4444')" 
                  stroke-width="1.8" 
                  stroke-linecap="round"
                />
              </svg>
            </td>
            <td>{{ item.failureRate }}</td>
            <td>
              <span class="status-badge" :class="item.statusClass">{{ item.status }}</span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="card-footer-link">
      <a href="#all-patterns">
        View all {{ currentTab }} patterns
        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
          <path d="M5 12h14M12 5l7 7-7 7"/>
        </svg>
      </a>
    </div>
  </div>
</template>

<script setup lang="ts">
// @ts-ignore - Vue runtime is provided by the app build tooling
import { ref, computed } from 'vue'

const props = defineProps<{
  patterns?: any
}>();

const currentTab = ref('banks');

const bankRows = [
  { name: 'HDFC Bank', score: 28, scoreType: 'red', trend: [3, 5, 11, 8, 14], failureRate: '18.7%', status: 'Degrading', statusClass: 'status-degrading' },
  { name: 'ICICI Bank', score: 63, scoreType: 'amber', trend: [5, 8, 6, 12, 10], failureRate: '9.2%', status: 'Watch', statusClass: 'status-watch' },
  { name: 'SBI', score: 72, scoreType: 'amber', trend: [8, 7, 9, 7, 8], failureRate: '6.1%', status: 'Watch', statusClass: 'status-watch' },
  { name: 'Axis Bank', score: 85, scoreType: 'green', trend: [12, 10, 11, 6, 3], failureRate: '3.2%', status: 'Healthy', statusClass: 'status-healthy' },
  { name: 'Kotak Bank', score: 92, scoreType: 'green', trend: [14, 11, 12, 5, 2], failureRate: '2.1%', status: 'Healthy', statusClass: 'status-healthy' }
];

const gatewayRows = [
  { name: 'Razorpay Direct', score: 94, scoreType: 'green', trend: [14, 13, 12, 5, 2], failureRate: '1.9%', status: 'Healthy', statusClass: 'status-healthy' },
  { name: 'PayU India', score: 68, scoreType: 'amber', trend: [6, 9, 8, 11, 9], failureRate: '8.4%', status: 'Watch', statusClass: 'status-watch' },
  { name: 'Cashfree Engine', score: 89, scoreType: 'green', trend: [11, 10, 8, 6, 3], failureRate: '2.8%', status: 'Healthy', statusClass: 'status-healthy' },
  { name: 'Juspay Router', score: 91, scoreType: 'green', trend: [13, 11, 10, 5, 3], failureRate: '2.3%', status: 'Healthy', statusClass: 'status-healthy' }
];

const methodRows = [
  { name: 'UPI AutoPay', score: 88, scoreType: 'green', trend: [10, 12, 8, 5, 3], failureRate: '3.1%', status: 'Healthy', statusClass: 'status-healthy' },
  { name: 'Credit Cards (Tokenized)', score: 82, scoreType: 'green', trend: [9, 10, 11, 7, 4], failureRate: '4.8%', status: 'Healthy', statusClass: 'status-healthy' },
  { name: 'Debit Cards (e-Mandate)', score: 54, scoreType: 'amber', trend: [4, 7, 9, 12, 11], failureRate: '12.6%', status: 'Degrading', statusClass: 'status-degrading' },
  { name: 'NetBanking Mandates', score: 71, scoreType: 'amber', trend: [7, 8, 6, 8, 7], failureRate: '7.0%', status: 'Watch', statusClass: 'status-watch' }
];

const currentRows = computed(() => {
  if (currentTab.value === 'gateways') return gatewayRows;
  if (currentTab.value === 'methods') return methodRows;
  return props.patterns?.banks || bankRows;
});

const generateSparkline = (points: number[]) => {
  if (!points || points.length < 5) return 'M2 8 L14 7 L26 9 L38 7 L46 8';
  return `M2 ${points[0]} L14 ${points[1]} L26 ${points[2]} L38 ${points[3]} L46 ${points[4]}`;
};
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
  padding: 14px 18px 10px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.card-title {
  font-size: 13px;
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

.pattern-tabs {
  display: flex;
  gap: 6px;
  padding: 0 18px 10px;
}

.tab-pill {
  font-size: 11px;
  font-weight: 600;
  color: #94a3b8;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid var(--border-card, #1e293b);
  padding: 4px 10px;
  border-radius: 14px;
  cursor: pointer;
  transition: all 0.15s ease;
}

.tab-pill.active {
  background: #2563eb;
  color: #fff;
  border-color: #2563eb;
}

.table-responsive {
  padding: 0 14px;
  overflow-x: auto;
}

.custom-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 11.5px;
}

.custom-table th {
  text-align: left;
  padding: 8px 10px;
  font-size: 10px;
  font-weight: 700;
  color: #64748b;
  border-bottom: 1px solid var(--border-card, #1e293b);
  text-transform: uppercase;
}

.custom-table td {
  padding: 9px 10px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.03);
  color: #e2e8f0;
}

.score-indicator {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-weight: 700;
}

.score-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
}
.score-dot.green { background: #10b981; }
.score-dot.amber { background: #f59e0b; }
.score-dot.red { background: #ef4444; }

.status-badge {
  font-size: 10px;
  font-weight: 700;
  padding: 2px 7px;
  border-radius: 4px;
}
.status-healthy { background: rgba(16, 185, 129, 0.15); color: #34d399; }
.status-watch { background: rgba(245, 158, 11, 0.15); color: #fbbf24; }
.status-degrading { background: rgba(239, 68, 68, 0.15); color: #f87171; }

.card-footer-link {
  padding: 10px 18px 14px;
  margin-top: auto;
}
.card-footer-link a {
  font-size: 11px;
  font-weight: 600;
  color: #3b82f6;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 4px;
}
</style>
