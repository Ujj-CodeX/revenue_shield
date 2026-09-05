

export const MERCHANTS = [
  { id: 'MERCH_001', name: 'StreamFlix India', industry: 'Streaming', plan: 'Premium' },
  { id: 'MERCH_002', name: 'FitPro Subscriptions', industry: 'Fitness', plan: 'Growth' },
  { id: 'MERCH_003', name: 'CloudNote SaaS', industry: 'SaaS', plan: 'Enterprise' },
  { id: 'MERCH_004', name: 'DailyNews+', industry: 'Media', plan: 'Starter' },
  { id: 'MERCH_005', name: 'EduLearn Academy', industry: 'EdTech', plan: 'Growth' },
];

function seededRandom(seed) {
  let s = seed % 2147483647;
  if (s <= 0) s += 2147483646;
  return () => {
    s = (s * 16807) % 2147483647;
    return (s - 1) / 2147483646;
  };
}

export function generateDashboardPayload(merchantId = 'MERCH_001', seed = 42) {
  const merchant = MERCHANTS.find((m) => m.id === merchantId) || MERCHANTS[0];
  const rand = seededRandom(seed);

  const totalFailures = 80 + Math.floor(rand() * 60);
  const revenueAtRisk = Math.round(totalFailures * (300 + rand() * 900));
  const recoverable = Math.round(revenueAtRisk * (0.35 + rand() * 0.15));
  const recovered = Math.round(recoverable * (0.85 + rand() * 0.2));

  return {
    merchantContext: {
      merchantName: `${merchant.name} (offline preview)`,
      merchantId: merchant.id,
      industry: merchant.industry,
      plan: merchant.plan,
      status: 'ACTIVE',
      onboardedDate: '-',
      seed,
      backtestRunId: `LOCAL_${seed}`,
      dataAsOf: new Date().toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' }),
      dateRange: '200 customers / 4 months (simulated, backend unreachable)',
    },
    kpiMetrics: {
      revenueAtRisk: `₹${revenueAtRisk.toLocaleString('en-IN')}`,
      revenueAtRiskSubtitle: `Across ${totalFailures} failed payments`,
      recoverableRevenue: `₹${recoverable.toLocaleString('en-IN')}`,
      recoverableRevenueSubtitle: 'Expected from EV-positive retries',
      recoveryRate: `${((recovered / recoverable) * 100).toFixed(1)}%`,
      recoveryRateSubtitle: '(Recovered / Recoverable)',
      uselessRetriesAvoided: String(Math.round(totalFailures * 0.4)),
      uselessRetriesAvoidedSubtitle: 'Vs naive retry everything',
    },
    failedPaymentsData: [],
    bucketSummaryData: {
      hardDeclines: { count: '-', percentage: '-' },
      softDeclines: { count: '-', percentage: '-' },
      uncertain: { count: '-', percentage: '-' },
      scheduledRetries: '-',
      resolvedRecovered: '-',
      resolvedNotRecovered: '-',
      skippedByEvGate: '-',
    },
    hardDeclineReportData: { topReasons: [] },
    backtestData: {
      policyRecoveredRevenue: `₹${recovered.toLocaleString('en-IN')}`,
      policyRetries: '-',
      naiveRetryRecoveredRevenue: '-',
      naiveRetries: '-',
      improvement: '-',
      improvementPercentage: '-',
      retriesAvoided: '-',
      retriesAvoidedPercentage: '-',
      seed,
      runId: `LOCAL_${seed}`,
      baselineDescription: 'Backend unreachable — showing local simulated placeholder, not a real backtest.',
    },
  };
}