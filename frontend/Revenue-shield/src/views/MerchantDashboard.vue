<template>
  <div class="d-flex w-100 min-vh-100 position-relative" id="terminal-app-root">
    <!-- Left Sidebar (Responsive Drawer on Mobile) -->
    <Sidebar 
      :merchant="merchant" 
      :is-open="isSidebarOpen"
      @close="isSidebarOpen = false"
    />

    <!-- Right Main Operations View -->
    <div class="d-flex flex-column grow min-vw-0 w-100" id="main-content-wrapper">
      <!-- Top Header Bar -->
      <HeaderBar 
        :merchant="merchant" 
        @refresh-data="handleRefresh"
        @open-date-picker="handleDatePicker"
        @toggle-sidebar="isSidebarOpen = !isSidebarOpen"
      />

      <!-- Dashboard Body -->
      <main class="p-2 p-sm-3 p-lg-4 grow" id="dashboard-main-area">
        <!-- 4 KPI Cards -->
        <KpiCards :metrics="kpiMetrics" />

        <!-- 2 Column Grid for Operations & Reports -->
        <div class="row g-3 g-lg-4" id="dashboard-grid">
          <!-- Left Main Column (Failed Payments Table & Backtest Panel) -->
          <div class="col-12 col-xl-8" id="left-main-column">
            <!-- Main Failed Payments Table -->
            <FailedPaymentsTable 
              :payments="failedPayments" 
              @view-all="handleViewAllPayments"
            />

            <!-- Backtest Simulation Panel -->
            <BacktestPanel :backtest="backtest" />
          </div>

          <!-- Right Column (Bucket Summary & Hard Decline Report) -->
          <div class="col-12 col-xl-4" id="right-side-column">
            <!-- Bucket Summary Panel -->
            <BucketSummary :summary="bucketSummary" />

            <!-- Hard Decline Report Panel -->
            <HardDeclineReport :report="hardDeclineReport" />
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

import {
  merchantContext,
  kpiMetrics,
  failedPaymentsData,
  bucketSummaryData,
  hardDeclineReportData,
  backtestData
} from '@/data/mockData.js';

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
  data() {
    return {
      merchant: { ...merchantContext },
      kpiMetrics: { ...kpiMetrics },
      failedPayments: [...failedPaymentsData],
      bucketSummary: { ...bucketSummaryData },
      hardDeclineReport: { ...hardDeclineReportData },
      backtest: { ...backtestData },
      isSidebarOpen: false
    };
  },
  methods: {
    handleRefresh() {
      const now = new Date();
      const options = { day: '2-digit', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit', hour12: true, timeZone: 'Asia/Kolkata' };
      this.merchant.dataAsOf = `${now.toLocaleDateString('en-GB', options)} IST`;
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
