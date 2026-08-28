# PayShield Payment Intelligence Dashboard - Vue 3 Components

Modular, typed Vue 3 Single File Components (SFCs) ready to import into any Vue 3 / Vite / Nuxt / Bootstrap-Vue application.

## Directory Structure
```
vue-components/
├── PaymentIntelligenceDashboard.vue     # Full root dashboard view
└── components/
    ├── AiShieldEngine.vue               # Standalone Decision Flow Node Graph
    ├── ActionCenter.vue                 # Recommendation cards & approval actions
    ├── HardDeclineIntelligence.vue      # Reason breakdown & CSV exporter
    ├── BacktestLab.vue                  # Policy vs Naive comparison simulation
    ├── AiCopilot.vue                    # Contextual chat query engine
    ├── SystemicPatterns.vue             # Multi-tab filter (Banks/Gateways/Methods)
    ├── AuditTimeline.vue                # Real-time event log
    ├── KpiMetrics.vue                   # Top 5 KPI blocks with trends & sparklines
    ├── Sidebar.vue                      # Navigation & SVG circular health gauge
    └── TopHeader.vue                    # Merchant identity & theme/date toggles
```

## Quick Start (Vue 3 / Vite)
1. Copy the `vue-components/` directory into your `src/` directory.
2. In your `App.vue` or router:
```vue
<template>
  <PaymentIntelligenceDashboard />
</template>

<script setup lang="ts">
import PaymentIntelligenceDashboard from './vue-components/PaymentIntelligenceDashboard.vue';
</script>
```

## Layout Grid Overview
- **Row 1**: `<KpiMetrics />` (5-column summary metrics)
- **Row 2**: `<AiShieldEngine />` (**Standalone full-width row** for spacious node flow graph)
- **Row 3**: 4-Column Grid:
  - `<ActionCenter />`
  - `<HardDeclineIntelligence />`
  - `<BacktestLab />`
  - `<AiCopilot />`
- **Row 4**: 2-Column Grid:
  - `<SystemicPatterns />`
  - `<AuditTimeline />`
