<template>
  <div class="card card-action-center">
    <div class="card-header">
      <div>
        <span class="card-title">ACTION CENTER</span>
        <span class="card-subtitle">{{ recommendations.length }} recommendations</span>
      </div>
      <a href="#action-center-full" class="card-action-link">
        View All
        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
          <path d="M5 12h14M12 5l7 7-7 7"/>
        </svg>
      </a>
    </div>

    <div class="action-cards-list">
      <div 
        v-for="item in recommendations" 
        :key="item.id" 
        class="action-item-card"
        :class="{ 'item-approved': item.approved }"
      >
        <div class="action-card-top">
          <span class="action-pill-tag" :class="item.tagClass">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
              <rect v-if="item.tagClass === 'tag-retry'" width="18" height="18" x="3" y="4" rx="2" ry="2"/>
              <path v-else d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/>
            </svg>
            {{ item.type }}
          </span>
          <div class="confidence-badge">
            <span class="confidence-label">Confidence</span>
            <span class="confidence-val" :class="item.confidenceClass">{{ item.confidence }}%</span>
          </div>
        </div>

        <div class="action-title">{{ item.title }}</div>
        <div class="action-reason"><span class="meta-lbl">Reason:</span> {{ item.reason }}</div>

        <div class="action-meta-row">
          <div v-if="item.expectedRecovery" class="meta-group">
            <span class="meta-lbl">Expected Recovery</span>
            <span class="meta-val">{{ item.expectedRecovery }}</span>
          </div>
          <div v-if="item.transactionsCount" class="meta-group">
            <span class="meta-lbl">Transactions</span>
            <span class="meta-val">{{ item.transactionsCount }}</span>
          </div>
          <div v-if="item.risk" class="meta-group">
            <span class="meta-lbl">Risk</span>
            <span class="risk-indicator"><span class="risk-dot"></span> {{ item.risk }}</span>
          </div>
        </div>

        <div class="action-buttons-row">
          <button 
            v-if="item.type === 'RETRY RECOMMENDED'" 
            class="btn-primary-action"
            :disabled="item.approved"
            @click="$emit('approve-action', item)"
          >
            {{ item.approved ? 'Approved ✓' : 'Approve Retry' }}
          </button>
          <button 
            v-else 
            class="btn-outline-action"
            @click="handleReview"
          >
            Review Now
          </button>
          
          <button class="btn-details-dropdown" @click="toggleDetails(item.id)">
            Details
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="m6 9 6 6 6-6"/>
            </svg>
          </button>
        </div>

        <!-- Collapsible Details -->
        <div v-if="expandedDetails[item.id]" class="action-details-expand">
          {{ item.details }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// @ts-expect-error Vue is resolved by the application's build environment.
import { reactive } from 'vue';

defineProps<{
  recommendations: Array<any>
}>();

defineEmits(['approve-action']);

const expandedDetails = reactive<Record<number, boolean>>({});

const toggleDetails = (id: number) => {
  expandedDetails[id] = !expandedDetails[id];
};

const handleReview = () => {
  window.alert("Opening Merchant Mandate Review Console...");
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
  padding: 14px 16px 10px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.card-title {
  font-size: 12.5px;
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

.action-cards-list {
  padding: 12px 14px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  overflow-y: auto;
  max-height: 480px;
}

.action-item-card {
  background-color: rgba(255, 255, 255, 0.02);
  border: 1px solid var(--border-card, #1e293b);
  border-radius: 8px;
  padding: 12px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.action-card-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.action-pill-tag {
  font-size: 9.5px;
  font-weight: 700;
  padding: 2px 7px;
  border-radius: 4px;
  display: inline-flex;
  align-items: center;
  gap: 4px;
}

.tag-retry { background: rgba(59, 130, 246, 0.15); color: #60a5fa; border: 1px solid rgba(59, 130, 246, 0.3); }
.tag-review { background: rgba(245, 158, 11, 0.15); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.3); }

.confidence-badge {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 10.5px;
}
.confidence-label { color: #64748b; }
.conf-high { color: #34d399; font-weight: 700; }
.conf-med { color: #fbbf24; font-weight: 700; }

.action-title { font-size: 12.5px; font-weight: 600; color: #f8fafc; }
.action-reason { font-size: 11px; color: #94a3b8; line-height: 1.35; }
.meta-lbl { color: #64748b; }
.meta-val { color: #f8fafc; font-weight: 600; }

.action-meta-row {
  display: flex;
  align-items: center;
  gap: 14px;
  font-size: 11px;
}

.risk-indicator {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  color: #34d399;
}
.risk-dot { width: 5px; height: 5px; border-radius: 50%; background-color: #34d399; }

.action-buttons-row {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 4px;
}

.btn-primary-action {
  flex: 1;
  background-color: #2563eb;
  color: #fff;
  border: none;
  padding: 6px 10px;
  border-radius: 6px;
  font-size: 11.5px;
  font-weight: 600;
  cursor: pointer;
}
.btn-primary-action:disabled {
  background-color: rgba(16, 185, 129, 0.3);
  color: #34d399;
  cursor: default;
}

.btn-outline-action {
  flex: 1;
  background-color: transparent;
  color: #f8fafc;
  border: 1px solid #334155;
  padding: 6px 10px;
  border-radius: 6px;
  font-size: 11.5px;
  font-weight: 600;
  cursor: pointer;
}

.btn-details-dropdown {
  background: transparent;
  border: 1px solid transparent;
  color: #64748b;
  font-size: 11px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 3px;
}

.action-details-expand {
  font-size: 10.5px;
  color: #94a3b8;
  background: rgba(0, 0, 0, 0.3);
  padding: 8px 10px;
  border-radius: 6px;
  line-height: 1.4;
  border-left: 2px solid #3b82f6;
}
</style>
