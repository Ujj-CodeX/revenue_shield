<template>
  <div class="dashboard-wrapper" :class="{ 'theme-light': isLightMode }">
    <!-- Left Navigation Sidebar -->
    <Sidebar :healthScore="91" @toggle-theme="toggleTheme" :isLightMode="isLightMode" />

    <!-- Main Content Area -->
    <div class="main-viewport">
      <!-- Top Header -->
      <TopHeader 
        merchantName="Netflix India (Prod)"
        merchantId="MID-99210-NFLX"
        :alertCount="7"
        @toggle-theme="toggleTheme"
        :isLightMode="isLightMode"
      />

      <!-- Dashboard Body -->
      <main class="dashboard-main">
        <div class="dashboard-grid-container">
          
          <!-- ROW 1: KPI Metrics Overview -->
          <KpiMetrics :metrics="kpiData" />

          <!-- ROW 2: Standalone AI Shield Engine Flow (Real-time decision intelligence) -->
          <section class="engine-row-standalone">
            <AiShieldEngine :engineData="engineData" />
          </section>

          <!-- ROW 3: 4-Column Grid (Action Center, Hard Decline, Backtest Lab, AI Copilot) -->
          <section class="four-col-grid">
            <ActionCenter :recommendations="recommendations" @approve-action="handleApproveAction" />
            <HardDeclineIntelligence :declineData="hardDeclineData" @export-csv="handleExportCsv" />
            <BacktestLab :backtestStats="backtestStats" @rerun="handleRerunBacktest" />
            <AiCopilot :initialMessages="copilotMessages" />
          </section>

          <!-- ROW 4: 2-Column Grid (Systemic Pattern Detection, Audit Timeline) -->
          <section class="two-col-grid">
            <SystemicPatterns :patterns="systemicPatterns" />
            <AuditTimeline :events="auditEvents" />
          </section>

        </div>
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
// @ts-ignore - Vue package/types are not available in this workspace yet.
import { ref, reactive, Ref } from 'vue';

// Type Interfaces
interface KPIData {
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

interface ClassificationBucket {
  count: number;
  pct: string;
}

interface ClassificationData {
  hardDecline: ClassificationBucket;
  softDecline: ClassificationBucket;
  uncertain: ClassificationBucket;
}

interface GateBucket {
  count: number;
  pct: string;
}

interface GateData {
  proceed: GateBucket;
  skip: GateBucket;
}

interface RetryIntelligenceData {
  scheduledRetries: number;
  timingOptimized: string;
}

interface RecoveryOutcome {
  amount: string;
  pct: string;
}

interface AlertData {
  title: string;
  message: string;
  target: string;
}

interface EngineData {
  failedPayments: number;
  classification: ClassificationData;
  evGate: GateData;
  retryIntelligence: RetryIntelligenceData;
  outcomes: OutcomeSummary;
  alert: AlertData;
}

interface RecommendationBase {
  id: number;
  type: string;
  tagClass: string;
  confidence: number;
  confidenceClass: string;
  title: string;
  reason: string;
  details: string;
  approved: boolean;
}

interface Recommendation extends RecommendationBase {
  expectedRecovery?: string;
  risk?: string;
}

interface ReviewRecommendation extends RecommendationBase {
  transactionsCount: number;
}

type RecommendationItem = Recommendation | ReviewRecommendation;

interface OutcomeSummary {
  recovered: RecoveryOutcome;
  notRecovered: RecoveryOutcome;
}

interface HardDeclineReason {
  code: string;
  count: string;
  pct: string;
}

interface HardDeclineData {
  totalCount: string;
  percentOfTotal: string;
  expectedLoss: string;
  reasons: HardDeclineReason[];
  exportFilename: string;
}

interface BacktestStats {
  policyRevenue: string;
  policyRate: string;
  naiveRevenue: string;
  naiveRate: string;
  avoidedRetries: string | number;
  avoidedPct: string;
  precision: string;
  recall: string;
  roi: string;
}

interface CopilotMessage {
  sender: string;
  text: string;
}

interface BankPattern {
  name: string;
  score: number;
  scoreType: string;
  trend: number[];
  failureRate: string;
  status: string;
  statusClass: string;
}

interface SystemicPatternsData {
  banks: BankPattern[];
}

interface AuditEvent {
  time: string;
  event: string;
  details: string;
  confidence: string;
  outcome: string;
  outcomeClass: string;
}
import Sidebar from './components/Sidebar.vue';
import TopHeader from './components/TopHeader.vue';
import KpiMetrics from './components/KpiMetrics.vue';
import AiShieldEngine from './components/AiShieldEngine.vue';
import ActionCenter from './components/ActionCenter.vue';
import HardDeclineIntelligence from './components/HardDeclineIntelligence.vue';
import BacktestLab from './components/BacktestLab.vue';
import AiCopilot from './components/AiCopilot.vue';
import SystemicPatterns from './components/SystemicPatterns.vue';
import AuditTimeline from './components/AuditTimeline.vue';

// Theme Reactive State
const isLightMode = ref<boolean>(false);
const toggleTheme = (): void => {
  isLightMode.value = !isLightMode.value;
};

// KPI Data
const kpiData = reactive<KPIData>({
  recoveredRevenue: '₹1,27,31,860',
  recoveredTrend: '+18.4%',
  netRecoveryRate: '32.7%',
  netRateTrend: '+4.2%',
  marginImprovement: '₹18,42,000',
  marginTrend: '+12.1%',
  retriesAvoided: '12,842',
  avoidedTrend: '+21.9%',
  criticalAlerts: 7
});

// AI Shield Engine Graph Data
const engineData = reactive<EngineData>({
  failedPayments: 45812,
  classification: {
    hardDecline: { count: 18765, pct: '40.9%' },
    softDecline: { count: 21634, pct: '47.2%' },
    uncertain: { count: 5413, pct: '11.8%' }
  },
  evGate: {
    proceed: { count: 12842, pct: '59.3%' },
    skip: { count: 8792, pct: '40.7%' }
  },
  retryIntelligence: {
    scheduledRetries: 8921,
    timingOptimized: 'Salary pattern + Bank health + Gateway signal'
  },
  outcomes: {
    recovered: { amount: '₹1,27,31,860', pct: '32.7%' },
    notRecovered: { amount: '₹2,61,41,120', pct: '67.3%' }
  },
  alert: {
    title: 'SYSTEMIC ALERT',
    message: 'HDFC Bank showing high failure spike in last 2 hours',
    target: '#systemic-patterns'
  }
});

// Action Center Recommendations
const recommendations = ref<RecommendationItem[]>([
  {
    id: 1,
    type: 'RETRY RECOMMENDED',
    tagClass: 'tag-retry',
    confidence: 82,
    confidenceClass: 'conf-high',
    title: 'Retry on 06 May 2025, 10:30 AM',
    reason: 'Salary credit pattern detected (most recoveries on 5–7th)',
    expectedRecovery: '₹38,420',
    risk: 'Low',
    details: 'Target Batch: 142 Subscriptions • Peak Window: 10:15–11:00 AM • Algorithm: Multi-armed Bandit Policy #04',
    approved: false
  },
  {
    id: 2,
    type: 'RETRY RECOMMENDED',
    tagClass: 'tag-retry',
    confidence: 74,
    confidenceClass: 'conf-high',
    title: 'Retry on 06 May 2025, 09:15 AM',
    reason: 'Network timeout issue resolved',
    expectedRecovery: '₹11,200',
    risk: 'Low',
    details: 'Target Batch: 28 Subscriptions • Gateway Route: Razorpay Direct • Error Code: 504_TIMEOUT_RESOLVED',
    approved: false
  },
  {
    id: 3,
    type: 'REVIEW REQUIRED',
    tagClass: 'tag-review',
    confidence: 42,
    confidenceClass: 'conf-med',
    title: 'Unstructured Failure Anomaly',
    reason: 'Unstructured failure reason',
    transactionsCount: 213,
    details: 'Raw Gateway Code: ERR_UNSPECIFIED_NONCE • Merchant Mandate verification required before auto-retry.',
    approved: false
  }
]);

const handleApproveAction = (item: RecommendationItem): void => {
  item.approved = true;
};

// Hard Decline Intelligence
const hardDeclineData = reactive<HardDeclineData>({
  totalCount: '18,765',
  percentOfTotal: '40.9%',
  expectedLoss: '₹1,83,14,000',
  reasons: [
    { code: 'CARD_EXPIRED', count: '6,842', pct: '36.4%' },
    { code: 'MANDATE_REVOKED', count: '4,281', pct: '22.8%' },
    { code: 'ACCOUNT_CLOSED', count: '3,921', pct: '20.9%' },
    { code: 'CUSTOMER_BLOCKED', count: '1,872', pct: '10.0%' },
    { code: 'OTHER', count: '1,849', pct: '9.9%' }
  ],
  exportFilename: 'Netflix_Hard_Declines_12May2025.csv'
});

const handleExportCsv = (): void => {
  const csvContent = "data:text/csv;charset=utf-8," 
    + "Reason,Count,Percentage\n"
    + hardDeclineData.reasons.map(e => `${e.code},${e.count},${e.pct}`).join("\n");
  const encodedUri = encodeURI(csvContent);
  const link: HTMLAnchorElement = document.createElement("a");
  link.setAttribute("href", encodedUri);
  link.setAttribute("download", hardDeclineData.exportFilename);
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
};

// Backtest Lab
const backtestStats = reactive<BacktestStats>({
  policyRevenue: '₹1,27,31,860',
  policyRate: '32.7%',
  naiveRevenue: '₹78,64,210',
  naiveRate: '20.2%',
  avoidedRetries: '12,842',
  avoidedPct: '45.6%',
  precision: '0.81',
  recall: '0.76',
  roi: '2.31x'
});

const handleRerunBacktest = (): void => {
  backtestStats.avoidedRetries = (12842 + Math.floor(Math.random() * 80)).toLocaleString();
  backtestStats.roi = (2.31 + (Math.random() * 0.08 - 0.04)).toFixed(2) + 'x';
};

// AI Copilot Messages
const copilotMessages = ref<CopilotMessage[]>([
  {
    sender: 'copilot',
    text: 'HDFC failures rose 18.7% between 08:00–10:00 IST due to gateway throttling. 142 soft failures are queued for auto-retry at 10:30 AM.'
  }
]);

// Systemic Patterns
const systemicPatterns = reactive<SystemicPatternsData>({
  banks: [
    { name: 'HDFC Bank', score: 28, scoreType: 'red', trend: [3, 5, 11, 8, 14], failureRate: '18.7%', status: 'Degrading', statusClass: 'status-degrading' },
    { name: 'ICICI Bank', score: 63, scoreType: 'amber', trend: [5, 8, 6, 12, 10], failureRate: '9.2%', status: 'Watch', statusClass: 'status-watch' },
    { name: 'SBI', score: 72, scoreType: 'amber', trend: [8, 7, 9, 7, 8], failureRate: '6.1%', status: 'Watch', statusClass: 'status-watch' },
    { name: 'Axis Bank', score: 85, scoreType: 'green', trend: [12, 10, 11, 6, 3], failureRate: '3.2%', status: 'Healthy', statusClass: 'status-healthy' },
    { name: 'Kotak Bank', score: 92, scoreType: 'green', trend: [14, 11, 12, 5, 2], failureRate: '2.1%', status: 'Healthy', statusClass: 'status-healthy' }
  ]
});

// Audit Timeline
const auditEvents = ref<AuditEvent[]>([
  { time: '10:31:12 AM', event: 'Classification', details: 'Soft Decline detected', confidence: '0.82', outcome: 'Soft Decline', outcomeClass: 'outcome-soft' },
  { time: '10:31:13 AM', event: 'EV Gate', details: 'EV ₹18,400 > 0', confidence: '0.79', outcome: 'Proceed', outcomeClass: 'outcome-proceed' },
  { time: '10:31:14 AM', event: 'Retry Scheduled', details: '06 May, 10:30 AM', confidence: '0.82', outcome: 'Scheduled', outcomeClass: 'outcome-scheduled' },
  { time: '10:31:20 AM', event: 'Retry Attempted', details: 'Gateway: Razorpay', confidence: '0.82', outcome: 'Success', outcomeClass: 'outcome-success' },
  { time: '10:31:21 AM', event: 'Payment Recovered', details: '₹18,400 recovered', confidence: '0.82', outcome: 'Recovered', outcomeClass: 'outcome-recovered' }
]);
</script>

<style scoped>
.dashboard-wrapper {
  display: flex;
  min-height: 100vh;
  background-color: var(--bg-app, #0a0e17);
  color: var(--text-primary, #f1f5f9);
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
}

.main-viewport {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.dashboard-main {
  flex: 1;
  padding: 20px 24px 32px;
  overflow-y: auto;
}

.dashboard-grid-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
  max-width: 1720px;
  margin: 0 auto;
}

/* Standalone Engine Row */
.engine-row-standalone {
  width: 100%;
}

/* 4-Column Grid */
.four-col-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  align-items: stretch;
}

/* 2-Column Grid */
.two-col-grid {
  display: grid;
  grid-template-columns: 1.1fr 1fr;
  gap: 16px;
  align-items: stretch;
}

@media (max-width: 1400px) {
  .four-col-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  .two-col-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 1100px) {
  .four-col-grid {
    grid-template-columns: 1fr;
  }
}
</style>
