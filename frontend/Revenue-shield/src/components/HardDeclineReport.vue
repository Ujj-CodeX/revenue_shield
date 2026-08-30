<template>
  <div class="terminal-panel mb-4" id="failed-payments-panel">
    <div class="terminal-panel-header" id="failed-payments-header">
      <span>FAILED PAYMENTS</span>
      <span class="subtitle">(THIS WEEK)</span>
    </div>

    <div class="table-responsive terminal-table-responsive" id="failed-payments-table-wrap">
      <table class="table terminal-table align-middle" id="failed-payments-table">
        <thead>
          <tr id="table-head-row">
            <th scope="col" class="text-nowrap" id="th-customer-id">CUSTOMER ID</th>
            <th scope="col" class="text-nowrap" id="th-reason-code">REASON CODE</th>
            <th scope="col" class="text-nowrap" id="th-bucket">BUCKET</th>
            <th scope="col" class="text-nowrap" id="th-confidence">CONFIDENCE</th>
            <th scope="col" class="text-nowrap" id="th-retry-date">RETRY DATE</th>
            <th scope="col" class="text-nowrap" id="th-status">STATUS</th>
            <th scope="col" class="text-end text-nowrap" id="th-expected-recovery">EXPECTED RECOVERY</th>
          </tr>
        </thead>
        <tbody id="table-body">
          <tr v-for="(payment, index) in payments" :key="payment.customerId || index" :id="`payment-row-${index}`">
            <!-- Customer ID -->
            <td class="text-terminal-bright fw-medium text-nowrap" :id="`td-cust-${index}`">
              {{ payment.customerId }}
            </td>

            <!-- Reason Code -->
            <td class="text-terminal-main text-nowrap" :id="`td-reason-${index}`">
              {{ payment.reasonCode }}
            </td>

            <!-- Bucket (HARD: Red, SOFT: Amber, UNCERTAIN: Yellow) -->
            <td class="text-nowrap" :id="`td-bucket-${index}`">
              <span :class="getBucketClass(payment.bucket)">
                {{ payment.bucket }}
              </span>
            </td>

            <!-- Confidence -->
            <td class="text-terminal-main text-nowrap" :id="`td-confidence-${index}`">
              {{ payment.confidence }}
            </td>

            <!-- Retry Date -->
            <td class="text-terminal-main text-nowrap" :id="`td-retry-date-${index}`">
              {{ payment.retryDate }}
            </td>

            <!-- Status (Retry Recommended: Green, No Retry: Red, Manual Review: Amber) -->
            <td class="text-nowrap" :id="`td-status-${index}`">
              <span :class="getStatusClass(payment.status)">
                {{ payment.status }}
              </span>
            </td>

            <!-- Expected Recovery -->
            <td class="text-end text-terminal-bright fw-medium text-nowrap" :id="`td-recovery-${index}`">
              {{ payment.expectedRecovery }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Table Footer: Pagination info & View All link -->
    <div class="table-footer-info flex-column flex-sm-row gap-2" id="table-footer-info">
      <span id="showing-entries-count">Showing 1 to 10 of 250 entries</span>
      <a href="#all-payments" class="table-footer-link" id="link-view-all-payments" @click.prevent="$emit('view-all')">
        View all failed payments &rarr;
      </a>
    </div>
  </div>
</template>

<script>
export default {
  name: 'FailedPaymentsTable',
  props: {
    payments: {
      type: Array,
      required: true
    }
  },
  emits: ['view-all'],
  methods: {
    getBucketClass(bucket) {
      const b = (bucket || '').toUpperCase();
      if (b === 'HARD') return 'bucket-hard';
      if (b === 'SOFT') return 'bucket-soft';
      if (b === 'UNCERTAIN') return 'bucket-uncertain';
      return 'text-terminal-muted';
    },
    getStatusClass(status) {
      const s = (status || '').toUpperCase();
      if (s === 'RETRY RECOMMENDED') return 'status-retry';
      if (s === 'NO RETRY') return 'status-no-retry';
      if (s === 'MANUAL REVIEW') return 'status-manual-review';
      return 'text-terminal-muted';
    }
  }
};
</script>
