<template>
  <div class="card card-audit-timeline">
    <div class="card-header">
      <div>
        <span class="card-title">AUDIT TIMELINE</span>
        <span class="card-subtitle">Live Feed</span>
      </div>
      <a href="#audit-full" class="card-action-link">
        Full Audit Trail
        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
          <path d="M5 12h14M12 5l7 7-7 7"/>
        </svg>
      </a>
    </div>

    <div class="table-responsive">
      <table class="custom-table audit-table">
        <thead>
          <tr>
            <th>TIME (IST)</th>
            <th>EVENT</th>
            <th>DETAILS</th>
            <th>CONFIDENCE</th>
            <th>OUTCOME</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(ev, idx) in events" :key="idx">
            <td class="time-cell">{{ ev.time }}</td>
            <td>{{ ev.event }}</td>
            <td class="details-cell">{{ ev.details }}</td>
            <td class="conf-cell">{{ ev.confidence }}</td>
            <td>
              <span class="outcome-badge" :class="ev.outcomeClass">{{ ev.outcome }}</span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="card-footer-link">
      <a href="#timeline-full">
        View full timeline
        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
          <path d="M5 12h14M12 5l7 7-7 7"/>
        </svg>
      </a>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  events: Array<{
    time: string;
    event: string;
    details: string;
    confidence: string;
    outcome: string;
    outcomeClass: string;
  }>
}>();
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

.card-action-link {
  font-size: 11px;
  font-weight: 600;
  color: #3b82f6;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 4px;
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

.time-cell {
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
  font-size: 10.5px;
  color: #94a3b8;
}

.details-cell {
  color: #cbd5e1;
}

.conf-cell {
  font-weight: 600;
}

.outcome-badge {
  font-size: 9.5px;
  font-weight: 700;
  padding: 2px 6px;
  border-radius: 4px;
}

.outcome-soft { background: rgba(245, 158, 11, 0.15); color: #fbbf24; }
.outcome-proceed { background: rgba(59, 130, 246, 0.15); color: #60a5fa; }
.outcome-scheduled { background: rgba(168, 85, 247, 0.15); color: #c084fc; }
.outcome-success { background: rgba(16, 185, 129, 0.15); color: #34d399; }
.outcome-recovered { background: rgba(16, 185, 129, 0.2); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.3); }

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
