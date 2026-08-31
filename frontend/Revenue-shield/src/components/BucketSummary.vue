<template>
  <div class="terminal-panel mb-4" id="bucket-summary-panel">
    <div class="terminal-panel-header" id="bucket-summary-header">
      <span>BUCKET SUMMARY</span>
      <span class="subtitle">(THIS WEEK)</span>
    </div>

    <div class="summary-kv-list" id="bucket-summary-list">
      <!-- Hard Declines -->
      <div class="summary-kv-item" id="summary-row-hard">
        <span class="summary-kv-label">Hard Declines</span>
        <span class="summary-kv-value text-terminal-red" id="summary-val-hard">
          {{ summary.hardDeclines.count }} <span class="fw-normal">({{ summary.hardDeclines.percentage }})</span>
        </span>
      </div>

      <!-- Soft Declines -->
      <div class="summary-kv-item" id="summary-row-soft">
        <span class="summary-kv-label">Soft Declines</span>
        <span class="summary-kv-value text-terminal-amber" id="summary-val-soft">
          {{ summary.softDeclines.count }} <span class="fw-normal">({{ summary.softDeclines.percentage }})</span>
        </span>
      </div>

      <!-- Uncertain -->
      <div class="summary-kv-item" id="summary-row-uncertain">
        <span class="summary-kv-label">Uncertain</span>
        <span class="summary-kv-value text-terminal-bright" id="summary-val-uncertain">
          {{ summary.uncertain.count }} <span class="fw-normal">({{ summary.uncertain.percentage }})</span>
        </span>
      </div>

      <!-- Divider -->
      <div class="summary-divider" id="summary-sep"></div>

      <!-- Scheduled Retries -->
      <div class="summary-kv-item" id="summary-row-scheduled">
        <span class="summary-kv-label">Scheduled Retries</span>
        <span class="summary-kv-value text-terminal-bright" id="summary-val-scheduled">
          {{ summary.scheduledRetries }}
        </span>
      </div>

      <!-- Resolved - Recovered -->
      <div class="summary-kv-item" id="summary-row-recovered">
        <span class="summary-kv-label">Resolved - Recovered</span>
        <span class="summary-kv-value text-terminal-green" id="summary-val-recovered">
          {{ summary.resolvedRecovered }}
        </span>
      </div>

      <!-- Resolved - Not Recovered -->
      <div class="summary-kv-item" id="summary-row-not-recovered">
        <span class="summary-kv-label">Resolved - Not Recovered</span>
        <span class="summary-kv-value text-terminal-red" id="summary-val-not-recovered">
          {{ summary.resolvedNotRecovered }}
        </span>
      </div>

      <!-- Skipped By EV Gate -->
      <div class="summary-kv-item" id="summary-row-ev-gate">
        <span class="summary-kv-label">Skipped By EV Gate</span>
        <span class="summary-kv-value text-terminal-amber" id="summary-val-ev-gate">
          {{ summary.skippedByEvGate }}
        </span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'BucketSummary',
  props: {
    summary: {
      type: Object,
      required: true
    }
  }
};
</script>
