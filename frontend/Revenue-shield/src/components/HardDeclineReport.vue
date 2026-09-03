<template>
  <div class="terminal-panel mb-4" id="hard-decline-report-panel">
    <div class="terminal-panel-header" id="hard-decline-report-header">
      <span>HARD DECLINE REPORT</span>
      <span class="subtitle">(AUDIT &amp; EXPORT)</span>
    </div>

    <!-- Summary Stats -->
    <div class="summary-kv-list mb-3" id="hard-decline-stats">
      <div class="summary-kv-item" id="hd-row-count">
        <span class="summary-kv-label">Total Hard Declines</span>
        <span class="summary-kv-value text-terminal-red" id="hd-val-count">
          {{ displayCount }}
        </span>
      </div>

      <div class="summary-kv-item" id="hd-row-loss">
        <span class="summary-kv-label">Expected Revenue Loss</span>
        <span class="summary-kv-value text-terminal-red" id="hd-val-loss">
          {{ displayLoss }}
        </span>
      </div>

      <div class="summary-kv-item" id="hd-row-retries">
        <span class="summary-kv-label">Retries Attempted</span>
        <span class="summary-kv-value text-terminal-bright" id="hd-val-retries">
          0 <span class="fw-normal text-terminal-muted">(EV Gated // Suppressed)</span>
        </span>
      </div>
    </div>

    <!-- Top Reasons Breakdown -->
    <div v-if="topReasonsList && topReasonsList.length" class="mb-3" id="hard-decline-reasons-wrap">
      <div class="summary-divider mb-2"></div>
      <div class="font-mono fs-8 text-terminal-muted fw-bold mb-2">
        TOP FAILURE REASONS
      </div>
      <div class="summary-kv-list" id="hard-decline-reasons-list">
        <div 
          v-for="(item, idx) in topReasonsList" 
          :key="item.reasonCode || idx" 
          class="summary-kv-item"
          :id="`hd-reason-item-${idx}`"
        >
          <span class="summary-kv-label text-terminal-main font-mono">{{ formatReason(item.reasonCode) }}</span>
          <span class="summary-kv-value text-terminal-amber font-mono">
            {{ item.count }} <span class="fw-normal text-terminal-muted">({{ item.percentage }})</span>
          </span>
        </div>
      </div>
    </div>

    <div class="summary-divider mb-3"></div>

    <!-- CSV Export Section -->
    <div class="csv-export-section" id="csv-export-section">
      <div class="d-flex justify-content-between align-items-center mb-2 font-mono fs-8">
        <span class="text-terminal-muted">EXPORT TARGET:</span>
        <span class="text-terminal-bright text-truncate ms-2" :title="computedFileName">{{ computedFileName }}</span>
      </div>

      <!-- Action Button for Client-Side Blob CSV Generation -->
      <button 
        type="button" 
        class="btn-terminal-outline w-100 font-mono d-flex align-items-center justify-content-center gap-2"
        id="btn-download-hard-decline-csv"
        @click="downloadHardDeclineCsv"
        :disabled="isDownloading"
      >
        <svg v-if="!downloadSuccess" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="square">
          <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
          <polyline points="7 10 12 15 17 10"></polyline>
          <line x1="12" y1="15" x2="12" y2="3"></line>
        </svg>
        <svg v-else width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="square">
          <polyline points="20 6 9 17 4 12"></polyline>
        </svg>
        <span>{{ downloadSuccess ? 'CSV GENERATED &amp; DOWNLOADED' : 'DOWNLOAD HARD DECLINE CSV' }}</span>
      </button>

      <div class="text-center font-mono fs-8 text-terminal-muted mt-2">
        {{ hardRecordsCount }} records ready &bull; No retry / Manual review
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HardDeclineReport',
  props: {
    report: {
      type: Object,
      default: () => ({})
    },
    payments: {
      type: Array,
      default: () => []
    },
    merchant: {
      type: Object,
      default: () => ({})
    }
  },
  data() {
    return {
      isDownloading: false,
      downloadSuccess: false
    };
  },
  computed: {
    hardPaymentsList() {
      const fromPayments = (this.payments || []).filter(
        p => (p.bucket || '').toUpperCase() === 'HARD'
      );
      if (fromPayments.length > 0) {
        return fromPayments;
      }
      // Fallback records if payments array has not arrived yet
      return [
        { customerId: 'CUST_98373', reasonCode: 'CARD_EXPIRED', expectedRecovery: '₹0', amount: '₹14,200', bucket: 'HARD' },
        { customerId: 'CUST_98374', reasonCode: 'MANDATE_REVOKED', expectedRecovery: '₹0', amount: '₹8,900', bucket: 'HARD' },
        { customerId: 'CUST_98376', reasonCode: 'ACCOUNT_CLOSED', expectedRecovery: '₹0', amount: '₹12,450', bucket: 'HARD' },
        { customerId: 'CUST_98378', reasonCode: 'INVALID_MANDATE', expectedRecovery: '₹0', amount: '₹6,300', bucket: 'HARD' }
      ];
    },
    hardRecordsCount() {
      return this.hardPaymentsList.length;
    },
    displayCount() {
      return (this.report && this.report.hardDeclinesCount) || String(this.hardRecordsCount);
    },
    displayLoss() {
      return (this.report && this.report.expectedRevenueLoss) || '₹1,83,14,000';
    },
    topReasonsList() {
      if (this.report && this.report.topReasons && this.report.topReasons.length > 0) {
        return this.report.topReasons;
      }
      // Compute from hardPaymentsList
      const counts = {};
      this.hardPaymentsList.forEach(p => {
        const code = p.reasonCode || 'CARD_EXPIRED';
        counts[code] = (counts[code] || 0) + 1;
      });
      const total = this.hardPaymentsList.length || 1;
      return Object.keys(counts).map(k => ({
        reasonCode: k,
        count: String(counts[k]),
        percentage: `${((counts[k] / total) * 100).toFixed(1)}%`
      }));
    },
    computedFileName() {
      const mid = (this.merchant && (this.merchant.merchantId || this.merchant.id)) || 
                  (this.report && this.report.merchantId) || 
                  'NETFLIX_IND_001';
      const seed = (this.merchant && this.merchant.seed) || 
                   (this.report && this.report.seed) || 
                   42;
      return `hard_declines_${mid}_${seed}.csv`;
    }
  },
  methods: {
    formatReason(code) {
      if (!code) return 'OTHER';
      return code.replace(/_/g, ' ');
    },
    downloadHardDeclineCsv() {
      try {
        this.isDownloading = true;
        const hardList = this.hardPaymentsList;

        // CSV Header as requested:
        // Customer ID, Reason Code, Amount if available, Failure Reason, Recommended Action = "No Retry - Manual Review"
        const headers = ["Customer ID", "Reason Code", "Amount", "Failure Reason", "Recommended Action"];

        const rows = hardList.map(p => {
          const custId = p.customerId || '';
          const reasonCode = p.reasonCode || 'HARD_DECLINE';
          const amount = p.amount || p.expectedRecovery || '₹0';
          const failureReason = reasonCode ? reasonCode.replace(/_/g, ' ') : 'Hard Invalidation';
          const action = 'No Retry - Manual Review';
          return [custId, reasonCode, amount, failureReason, action];
        });

        const csvRows = [
          headers.join(','),
          ...rows.map(row => 
            row.map(val => {
              const str = String(val == null ? '' : val);
              if (str.includes(',') || str.includes('"') || str.includes('\n')) {
                return `"${str.replace(/"/g, '""')}"`;
              }
              return str;
            }).join(',')
          )
        ];

        const csvContent = csvRows.join('\r\n');
        const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', this.computedFileName);
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);

        this.downloadSuccess = true;
        setTimeout(() => {
          this.downloadSuccess = false;
          this.isDownloading = false;
        }, 2200);
      } catch (err) {
        console.error('Error generating CSV download:', err);
        this.isDownloading = false;
      }
    }
  }
};
</script>

<style scoped>
.fs-8 {
  font-size: 0.72rem;
}

.csv-export-section {
  background: #0B101D;
  border: 1px solid var(--border-color, #1D2738);
  padding: 12px;
}
</style>
