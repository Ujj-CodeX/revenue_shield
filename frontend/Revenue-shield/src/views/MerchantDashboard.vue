<template>
  <div class="d-flex w-100 min-vh-100 position-relative" id="terminal-app-root">
    <!-- Left Sidebar (Responsive Drawer on Mobile) -->
    <Sidebar 
      :merchant="activeMerchant" 
      :is-open="isSidebarOpen"
      @close="isSidebarOpen = false"
    />

    <!-- Right Main Operations View -->
    <div class="d-flex flex-column grow min-vw-0 w-100" id="main-content-wrapper">
      <!-- Top Header Bar -->
      <HeaderBar 
        :merchant="activeMerchant" 
        @refresh-data="handleRefresh"
        @open-date-picker="handleDatePicker"
        @toggle-sidebar="isSidebarOpen = !isSidebarOpen"
      />

      <!-- Dashboard Body -->
      <main class="p-2 p-sm-3 p-lg-4 grow" id="dashboard-main-area">
        <!-- 4 KPI Cards -->
        <KpiCards :metrics="activeKpiMetrics" />

        <!-- 2 Column Grid for Operations & Reports -->
        <div class="row g-3 g-lg-4" id="dashboard-grid">
          <!-- Left Main Column (Failed Payments Table & Backtest Panel) -->
          <div class="col-12 col-xl-8" id="left-main-column">
            <!-- Main Failed Payments Table -->
            <FailedPaymentsTable 
  :payments="activeFailedPayments" 
  @view-all="handleViewAllPayments"
/>

            <!-- Backtest Simulation Panel -->
            <BacktestPanel :backtest="activeBacktest" @rerun="handleRerun" />
          </div>

          <!-- Right Column (Bucket Summary & Hard Decline Report) -->
          <div class="col-12 col-xl-4" id="right-side-column">
            <!-- Bucket Summary Panel -->
            <BucketSummary :summary="activeBucketSummary" />

            <!-- Hard Decline Report Panel -->
            <HardDeclineReport 
              :report="activeHardDeclineReport" 
              :payments="activeFailedPayments"
              :merchant="activeMerchant"
            />
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script>
import Sidebar from '@/components/SideBar.vue';
import HeaderBar from '@/components/HeaderBar.vue';
import KpiCards from '@/components/KpiCards.vue';
import FailedPaymentsTable from '@/components/FailedPaymentsTable.vue';
import BucketSummary from '@/components/BucketSummary.vue';
import HardDeclineReport from '@/components/HardDeclineReport.vue';
import BacktestPanel from '@/components/BacktestPanel.vue';

const API_BASE = import.meta.env.VITE_API_BASE || '';

export default {
  name: 'MerchantDashboard',
  components: {
    Sidebar,
    HeaderBar,
    KpiCards,
    FailedPaymentsTable,
    BucketSummary,
    HardDeclineReport,
    BacktestPanel
  },
  props: {
    merchant: { type: Object, default: () => null },
    kpiMetrics: { type: Object, default: () => null },
    failedPayments: { type: Array, default: () => null },
    bucketSummary: { type: Object, default: () => null },
    hardDeclineReport: { type: Object, default: () => null },
    backtest: { type: Object, default: () => null },
  },
  emits: ['rerun'],
  data() {
    return {
      internalMerchant: {},
      internalKpiMetrics: {},
      internalFailedPayments: [],
      internalBucketSummary: { hardDeclines: { count: '-', percentage: '-' }, softDeclines: { count: '-', percentage: '-' }, uncertain: { count: '-', percentage: '-' }, scheduledRetries: '-', resolvedRecovered: '-', resolvedNotRecovered: '-', skippedByEvGate: '-' },
      internalHardDeclineReport: { topReasons: [] },
      internalBacktest: {},
      isSidebarOpen: false,
      loading: false,
      error: null
    };
  },
  computed: {
    activeMerchant() {
      return (this.merchant && Object.keys(this.merchant).length > 0) ? this.merchant : this.internalMerchant;
    },
    activeKpiMetrics() {
      return (this.kpiMetrics && Object.keys(this.kpiMetrics).length > 0) ? this.kpiMetrics : this.internalKpiMetrics;
    },
    activeFailedPayments() {
      return (this.failedPayments && this.failedPayments.length > 0) ? this.failedPayments : this.internalFailedPayments;
    },
    activeBucketSummary() {
      return (this.bucketSummary && Object.keys(this.bucketSummary).length > 0) ? this.bucketSummary : this.internalBucketSummary;
    },
    activeHardDeclineReport() {
      return (this.hardDeclineReport && Object.keys(this.hardDeclineReport).length > 0) ? this.hardDeclineReport : this.internalHardDeclineReport;
    },
    activeBacktest() {
      return (this.backtest && Object.keys(this.backtest).length > 0) ? this.backtest : this.internalBacktest;
    }
  },
  mounted() {
    if (!this.merchant || !this.merchant.merchantName) {
      this.fetchDashboard();
    }
  },
  methods: {
    handleRerun() {
      this.$emit('rerun');
    },
    async fetchDashboard() {
      this.loading = true;
      this.error = null;
      try {
        const res = await fetch(`${API_BASE}/api/dashboard/`);
        if (!res.ok) throw new Error(`API returned ${res.status}`);
        const data = await res.json();
        this.internalMerchant = data.merchantContext;
        this.internalKpiMetrics = data.kpiMetrics;
        this.internalFailedPayments = data.failedPaymentsData;
        this.internalBucketSummary = data.bucketSummaryData;
        this.internalHardDeclineReport = data.hardDeclineReportData;
        this.internalBacktest = data.backtestData;
      } catch (e) {
        this.error = e.message;
      } finally {
        this.loading = false;
      }
    },
    handleRefresh() {
      this.$emit('rerun');
    },
    handleDatePicker() {
      // Date range trigger handler
    },
    handleViewAllPayments() {
      // View all trigger handler
    }
  }
};
</script>