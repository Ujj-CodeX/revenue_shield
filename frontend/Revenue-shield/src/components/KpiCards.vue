<template>
  <div class="row g-3 mb-4" id="kpi-cards-container">
    <!-- KPI 1: Revenue at Risk -->
    <div class="col-12 col-sm-6 col-xl-3" id="kpi-col-risk">
      <div class="kpi-card" id="kpi-card-risk">
        <div class="kpi-label" id="kpi-label-risk">REVENUE AT RISK</div>
        <div class="kpi-value text-terminal-red" id="kpi-val-risk">{{ metrics.revenueAtRisk }}</div>
        <div class="kpi-subtitle" id="kpi-sub-risk">{{ metrics.revenueAtRiskSubtitle }}</div>
      </div>
    </div>

    <!-- KPI 2: Recoverable Revenue -->
    <div class="col-12 col-sm-6 col-xl-3" id="kpi-col-recoverable">
      <div class="kpi-card" id="kpi-card-recoverable">
        <div class="kpi-label" id="kpi-label-recoverable">RECOVERABLE REVENUE</div>
        <div class="kpi-value text-terminal-green" id="kpi-val-recoverable">{{ metrics.recoverableRevenue }}</div>
        <div class="kpi-subtitle" id="kpi-sub-recoverable">{{ metrics.recoverableRevenueSubtitle }}</div>
      </div>
    </div>

    <!-- KPI 3: Recovery Rate -->
    <div class="col-12 col-sm-6 col-xl-3" id="kpi-col-rate">
      <div class="kpi-card" id="kpi-card-rate">
        <div class="kpi-label" id="kpi-label-rate">RECOVERY RATE</div>
        <div class="kpi-value text-terminal-green" id="kpi-val-rate">{{ metrics.recoveryRate }}</div>
        <div class="kpi-subtitle" id="kpi-sub-rate">{{ metrics.recoveryRateSubtitle }}</div>
      </div>
    </div>

    <!-- KPI 4: Useless Retries Avoided -->
    <div class="col-12 col-sm-6 col-xl-3" id="kpi-col-avoided">
      <div class="kpi-card" id="kpi-card-avoided">
        <div class="kpi-label" id="kpi-label-avoided">USELESS RETRIES AVOIDED</div>
        <div class="kpi-value text-terminal-amber" id="kpi-val-avoided">{{ metrics.uselessRetriesAvoided }}</div>
        <div class="kpi-subtitle" id="kpi-sub-avoided">{{ metrics.uselessRetriesAvoidedSubtitle }}</div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'KpiCards',
  props: {
    metrics: {
      type: Object,
      required: true
    }
  }
};
</script>
