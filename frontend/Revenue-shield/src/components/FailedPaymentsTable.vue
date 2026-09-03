<template>
  <div class="terminal-panel mb-4" id="failed-payments-panel">
    <div class="terminal-panel-header d-flex justify-content-between align-items-center" id="failed-payments-header">
      <div>
        <span>FAILED PAYMENTS</span>
        <span class="subtitle">(THIS WEEK)</span>
      </div>
      <span class="font-mono fs-8 text-terminal-muted">
        TOTAL: <strong class="text-terminal-bright">{{ totalRows }}</strong>
      </span>
    </div>

    <!-- Scrollable container with min-width table to avoid column clipping -->
    <div class="table-responsive terminal-table-responsive" id="failed-payments-table-wrap">
      <table class="table terminal-table align-middle mb-0" id="failed-payments-table">
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
          <tr 
            v-for="(payment, index) in paginatedPayments" 
            :key="payment.customerId || (startIndex + index)" 
            :id="`payment-row-${startIndex + index}`"
          >
            <!-- Customer ID -->
            <td class="text-terminal-bright fw-medium text-nowrap font-mono" :id="`td-cust-${startIndex + index}`">
              {{ payment.customerId }}
            </td>

            <!-- Reason Code -->
            <td class="text-terminal-main text-nowrap font-mono" :id="`td-reason-${startIndex + index}`">
              {{ payment.reasonCode }}
            </td>

            <!-- Bucket (HARD: Red, SOFT: Amber, UNCERTAIN: Yellow) -->
            <td class="text-nowrap font-mono" :id="`td-bucket-${startIndex + index}`">
              <span :class="getBucketClass(payment.bucket)">
                {{ payment.bucket }}
              </span>
            </td>

            <!-- Confidence -->
            <td class="text-terminal-main text-nowrap font-mono" :id="`td-confidence-${startIndex + index}`">
              {{ payment.confidence }}
            </td>

            <!-- Retry Date -->
            <td class="text-terminal-main text-nowrap font-mono" :id="`td-retry-date-${startIndex + index}`">
              {{ payment.retryDate }}
            </td>

            <!-- Status (Retry Recommended: Green, No Retry: Red, Manual Review: Amber) -->
            <td class="text-nowrap font-mono" :id="`td-status-${startIndex + index}`">
              <span :class="getStatusClass(payment.status)">
                {{ payment.status }}
              </span>
            </td>

            <!-- Expected Recovery -->
            <td class="text-end text-terminal-bright fw-medium text-nowrap font-mono" :id="`td-recovery-${startIndex + index}`">
              {{ payment.expectedRecovery }}
            </td>
          </tr>
          <tr v-if="paginatedPayments.length === 0">
            <td colspan="7" class="text-center py-4 text-terminal-muted font-mono">
              NO FAILED PAYMENT RECORDS FOUND
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Table Footer: Working Client-Side Pagination & Controls -->
    <div class="table-footer-info d-flex flex-wrap align-items-center justify-content-between p-2 pt-3 gap-3 font-mono fs-8" id="table-footer-info">
      <!-- Showing Entries Count & Page Size Selector -->
      <div class="d-flex flex-wrap align-items-center gap-3">
        <span id="showing-entries-count" class="text-terminal-muted">
          {{ showingText }}
        </span>

        <div class="d-flex align-items-center gap-1">
          <label for="page-size-select" class="text-terminal-muted fs-8 mb-0">Rows:</label>
          <select 
            id="page-size-select" 
            v-model.number="pageSize" 
            class="terminal-select-sm"
          >
            <option :value="10">10</option>
            <option :value="15">15</option>
            <option :value="25">25</option>
          </select>
        </div>
      </div>

      <!-- Pagination Controls (Prev / Next & Page indicator) -->
      <div class="d-flex align-items-center gap-2">
        <button 
          type="button" 
          class="btn-pagination" 
          id="btn-prev-page"
          :disabled="currentPage <= 1"
          @click="prevPage"
        >
          &larr; Prev
        </button>

        <span class="pagination-page-indicator text-terminal-bright" id="pagination-page-indicator">
          Page {{ currentPage }} / {{ totalPages }}
        </span>

        <button 
          type="button" 
          class="btn-pagination" 
          id="btn-next-page"
          :disabled="currentPage >= totalPages"
          @click="nextPage"
        >
          Next &rarr;
        </button>

        <span class="text-terminal-muted mx-1">|</span>

        <a href="#all-payments" class="table-footer-link" id="link-view-all-payments" @click.prevent="handleViewAll">
          View all failed payments &rarr;
        </a>
      </div>
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
  data() {
    return {
      currentPage: 1,
      pageSize: 10
    };
  },
  computed: {
    totalRows() {
      return (this.payments && this.payments.length) || 0;
    },
    totalPages() {
      return Math.max(1, Math.ceil(this.totalRows / this.pageSize));
    },
    startIndex() {
      if (this.totalRows === 0) return 0;
      return (this.currentPage - 1) * this.pageSize;
    },
    endIndex() {
      return Math.min(this.startIndex + this.pageSize, this.totalRows);
    },
    paginatedPayments() {
      if (!this.payments) return [];
      return this.payments.slice(this.startIndex, this.endIndex);
    },
    showingText() {
      if (this.totalRows === 0) return 'Showing 0 to 0 of 0 entries';
      return `Showing ${this.startIndex + 1} to ${this.endIndex} of ${this.totalRows} entries`;
    }
  },
  watch: {
    payments() {
      if (this.currentPage > this.totalPages) {
        this.currentPage = 1;
      }
    },
    pageSize() {
      this.currentPage = 1;
    }
  },
  methods: {
    prevPage() {
      if (this.currentPage > 1) {
        this.currentPage--;
      }
    },
    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++;
      }
    },
    handleViewAll() {
      this.pageSize = 25;
      this.currentPage = 1;
      this.$emit('view-all');
    },
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

<style scoped>
#failed-payments-table-wrap {
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
}

#failed-payments-table {
  min-width: 860px;
  width: 100%;
}

.terminal-select-sm {
  background: #0B101D;
  border: 1px solid var(--border-color, #1D2738);
  color: var(--text-bright, #F0F4FC);
  font-family: var(--font-mono, monospace);
  font-size: 11px;
  padding: 2px 6px;
  cursor: pointer;
  outline: none;
}

.terminal-select-sm:focus {
  border-color: var(--accent-green, #7CFC6A);
}

.btn-pagination {
  background: #0B101D;
  border: 1px solid var(--border-color, #1D2738);
  color: var(--text-main, #D8DEE9);
  font-family: var(--font-mono, monospace);
  font-size: 11px;
  padding: 2px 8px;
  cursor: pointer;
  transition: all 0.15s ease;
}

.btn-pagination:hover:not(:disabled) {
  border-color: var(--accent-green, #7CFC6A);
  color: var(--accent-green, #7CFC6A);
  background: rgba(124, 252, 106, 0.08);
}

.btn-pagination:disabled {
  opacity: 0.35;
  cursor: not-allowed;
  border-color: #141C2B;
}

.pagination-page-indicator {
  font-family: var(--font-mono, monospace);
  font-size: 11px;
  color: var(--text-bright, #F0F4FC);
  padding: 0 4px;
}

.fs-8 {
  font-size: 0.72rem;
}
</style>
