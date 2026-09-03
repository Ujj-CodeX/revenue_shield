<template>
  <transition name="terminal-fade">
    <div 
      v-if="visible" 
      class="loading-overlay-backdrop d-flex flex-column align-items-center justify-content-center"
      id="staged-loading-overlay"
    >
      <div class="loading-container text-center p-4 p-md-5" id="loading-container">
        <!-- Terminal Scan Ring Spinner -->
        <div class="spinner-wrapper mb-4">
          <div class="radar-outer-ring">
            <div class="radar-inner-ring">
              <div class="radar-center-core"></div>
            </div>
          </div>
          <div class="radar-scan-arm"></div>
        </div>

        <!-- Terminal Step Tag -->
        <div class="d-inline-flex align-items-center gap-2 mb-2 font-mono fs-8 text-terminal-muted">
          <span class="badge-stage-counter">
            STAGE [ {{ currentStepIndex + 1 }} / {{ messages.length }} ]
          </span>
          <span class="text-terminal-muted">&bull;</span>
          <span class="text-terminal-green text-uppercase font-mono">
            {{ mode === 'rerun' ? 'SIMULATION_RECALIBRATION' : 'INGESTION_PIPELINE' }}
          </span>
        </div>

        <!-- Single Line of Cycling Status Text -->
        <div class="status-message-wrapper my-2">
          <transition name="status-slide" mode="out-in">
            <div 
              :key="currentMessage" 
              class="status-message text-terminal-bright font-mono fs-5 fw-bold"
              id="loading-status-text"
            >
              {{ currentMessage }}
            </div>
          </transition>
        </div>

        <!-- Monospace Progress Bar -->
        <div class="progress-bar-track mt-3 mx-auto">
          <div 
            class="progress-bar-fill" 
            :style="{ width: `${progressPercentage}%` }"
          ></div>
        </div>

        <!-- Telemetry Details Subtitle -->
        <div class="mt-3 font-mono fs-8 text-terminal-muted">
          <span>MERCHANT: <strong class="text-terminal-bright">{{ merchantId }}</strong></span>
          <span class="mx-2">&bull;</span>
          <span>SEED: <strong class="text-terminal-green">{{ currentSeed }}</strong></span>
        </div>
      </div>
    </div>
  </transition>
</template>

<script>
import { fetchDashboard, runBacktest } from '@/services/api';

const INITIAL_MESSAGES = [
  "Loading merchant data...",
  "Generating payment failure scenarios...",
  "Creating synthetic customer profiles...",
  "Calculating revenue impact...",
  "Running policy engine...",
  "Comparing against naive baseline...",
  "Preparing dashboard..."
];

const RERUN_MESSAGES = [
  "Generating new simulation...",
  "Running recovery policy...",
  "Comparing against naive baseline...",
  "Refreshing dashboard..."
];

export default {
  name: 'LoadingOverlay',
  props: {
    active: {
      type: Boolean,
      default: true
    },
    merchantId: {
      type: String,
      default: 'MERCH_001'
    },
    seed: {
      type: [Number, String],
      default: 42
    },
    mode: {
      type: String,
      default: 'initial' // 'initial' | 'rerun'
    }
  },
  emits: ['complete'],
  data() {
    return {
      visible: this.active,
      currentStepIndex: 0,
      timer: null,
      cycleCompleted: false,
      apiResolved: false,
      apiData: null,
      stepDuration: 550, // 550ms per step (~500-600ms)
    };
  },
  computed: {
    messages() {
      return this.mode === 'rerun' ? RERUN_MESSAGES : INITIAL_MESSAGES;
    },
    currentMessage() {
      return this.messages[this.currentStepIndex] || this.messages[0];
    },
    progressPercentage() {
      return Math.round(((this.currentStepIndex + 1) / this.messages.length) * 100);
    },
    currentSeed() {
      return this.seed !== null && this.seed !== undefined ? this.seed : 42;
    }
  },
  watch: {
    active(newVal) {
      if (newVal) {
        this.startSequence();
      } else {
        this.visible = false;
        this.cleanup();
      }
    }
  },
  mounted() {
    if (this.active) {
      this.startSequence();
    }
  },
  beforeUnmount() {
    this.cleanup();
  },
  methods: {
    startSequence() {
      this.visible = true;
      this.currentStepIndex = 0;
      this.cycleCompleted = false;
      this.apiResolved = false;
      this.apiData = null;

      // Start asynchronous backend fetch
      this.executeFetch();

      // Start sequential message cycling
      this.runMessageCycle();
    },
    async executeFetch() {
      try {
        let result;
        if (this.mode === 'rerun') {
          result = await runBacktest(this.merchantId, this.currentSeed);
        } else {
          result = await fetchDashboard(this.merchantId, this.currentSeed);
        }
        this.apiData = result;
      } catch (err) {
        console.error('LoadingOverlay fetch error:', err);
      } finally {
        this.apiResolved = true;
        this.checkCompletion();
      }
    },
    runMessageCycle() {
      this.cleanup();
      this.timer = setInterval(() => {
        if (this.currentStepIndex < this.messages.length - 1) {
          this.currentStepIndex++;
        } else {
          // Reached last message
          this.cycleCompleted = true;
          clearInterval(this.timer);
          this.timer = null;
          this.checkCompletion();
        }
      }, this.stepDuration);
    },
    checkCompletion() {
      // Complete only when BOTH the response has resolved AND the message cycle has finished
      if (this.cycleCompleted && this.apiResolved) {
        // Small delay to let user view final message before fading
        setTimeout(() => {
          this.visible = false;
          this.$emit('complete', this.apiData);
        }, 200);
      }
    },
    cleanup() {
      if (this.timer) {
        clearInterval(this.timer);
        this.timer = null;
      }
    }
  }
};
</script>

<style scoped>
.loading-overlay-backdrop {
  position: fixed;
  inset: 0;
  z-index: 9999;
  background: rgba(7, 11, 20, 0.88);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  transition: opacity 0.35s ease, backdrop-filter 0.35s ease;
}

.loading-container {
  max-width: 580px;
  width: 90%;
  background: var(--bg-panel, #0E1422);
  border: 1px solid var(--border-color, #1D2738);
  box-shadow: 0 12px 48px rgba(0, 0, 0, 0.6), 0 0 20px rgba(124, 252, 106, 0.1);
}

.spinner-wrapper {
  position: relative;
  width: 72px;
  height: 72px;
  margin: 0 auto;
}

.radar-outer-ring {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  border: 2px solid rgba(124, 252, 106, 0.2);
  border-top-color: var(--accent-green, #7CFC6A);
  animation: spin 1.2s linear infinite;
  display: flex;
  align-items: center;
  justify-content: center;
}

.radar-inner-ring {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  border: 1px dashed rgba(124, 252, 106, 0.4);
  border-bottom-color: var(--accent-green, #7CFC6A);
  animation: spin-reverse 1.8s linear infinite;
  display: flex;
  align-items: center;
  justify-content: center;
}

.radar-center-core {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: var(--accent-green, #7CFC6A);
  box-shadow: 0 0 12px var(--accent-green, #7CFC6A);
  animation: core-pulse 1.2s infinite alternate ease-in-out;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

@keyframes spin-reverse {
  from { transform: rotate(360deg); }
  to { transform: rotate(0deg); }
}

@keyframes core-pulse {
  from { transform: scale(0.8); opacity: 0.6; }
  to { transform: scale(1.2); opacity: 1; }
}

.badge-stage-counter {
  background: rgba(108, 122, 156, 0.15);
  border: 1px solid var(--border-color, #1D2738);
  padding: 2px 8px;
  color: var(--text-bright, #F0F4FC);
}

.status-message-wrapper {
  min-height: 38px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.status-message {
  color: var(--text-bright, #F0F4FC);
  letter-spacing: -0.01em;
}

.progress-bar-track {
  width: 100%;
  max-width: 320px;
  height: 4px;
  background: #070B14;
  border: 1px solid var(--border-color, #1D2738);
  overflow: hidden;
}

.progress-bar-fill {
  height: 100%;
  background-color: var(--accent-green, #7CFC6A);
  box-shadow: 0 0 8px var(--accent-green, #7CFC6A);
  transition: width 0.35s ease;
}

/* Transitions */
.terminal-fade-enter-active,
.terminal-fade-leave-active {
  transition: opacity 0.3s ease;
}

.terminal-fade-enter-from,
.terminal-fade-leave-to {
  opacity: 0;
}

.status-slide-enter-active,
.status-slide-leave-active {
  transition: all 0.2s ease;
}

.status-slide-enter-from {
  opacity: 0;
  transform: translateY(6px);
}

.status-slide-leave-to {
  opacity: 0;
  transform: translateY(-6px);
}

.fs-7 { font-size: 0.75rem; }
.fs-8 { font-size: 0.7rem; }
</style>
