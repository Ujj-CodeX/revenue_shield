/**
 * Revenue Shield AI - Mock Data Engine
 * Seed: 42
 * Run ID: BT_20250512_1042
 */

export const merchantContext = {
  merchantName: "NETFLIX INDIA",
  merchantId: "NETFLIX_IND_001",
  industry: "Streaming",
  plan: "Premium",
  status: "ACTIVE",
  onboardedDate: "12 Jan 2025",
  seed: 42,
  backtestRunId: "BT_20250512_1042",
  dataAsOf: "12 May 2025, 10:31 AM IST",
  dateRange: "06 May 2025 - 12 May 2025"
};

export const kpiMetrics = {
  revenueAtRisk: "₹4,83,21,000",
  revenueAtRiskSubtitle: "Across 45,812 failed payments",
  recoverableRevenue: "₹2,92,18,400",
  recoverableRevenueSubtitle: "Expected from soft declines",
  recoveryRate: "34.2%",
  recoveryRateSubtitle: "(Recovered / Recoverable)",
  uselessRetriesAvoided: "12,842",
  uselessRetriesAvoidedSubtitle: "Vs naive retry everything"
};

export const failedPaymentsData = [
  {
    customerId: "CUST_98371",
    reasonCode: "INSUFFICIENT_FUNDS",
    bucket: "SOFT",
    confidence: "0.82",
    retryDate: "06 May 2025, 10:30 AM",
    status: "RETRY RECOMMENDED",
    expectedRecovery: "₹38,420"
  },
  {
    customerId: "CUST_98372",
    reasonCode: "BANK_TIMEOUT",
    bucket: "SOFT",
    confidence: "0.74",
    retryDate: "06 May 2025, 09:15 AM",
    status: "RETRY RECOMMENDED",
    expectedRecovery: "₹11,200"
  },
  {
    customerId: "CUST_98373",
    reasonCode: "CARD_EXPIRED",
    bucket: "HARD",
    confidence: "0.96",
    retryDate: "-",
    status: "NO RETRY",
    expectedRecovery: "₹0"
  },
  {
    customerId: "CUST_98374",
    reasonCode: "MANDATE_REVOKED",
    bucket: "HARD",
    confidence: "0.98",
    retryDate: "-",
    status: "NO RETRY",
    expectedRecovery: "₹0"
  },
  {
    customerId: "CUST_98375",
    reasonCode: "NETWORK_ERROR",
    bucket: "SOFT",
    confidence: "0.69",
    retryDate: "07 May 2025, 11:00 AM",
    status: "RETRY RECOMMENDED",
    expectedRecovery: "₹7,980"
  },
  {
    customerId: "CUST_98376",
    reasonCode: "ACCOUNT_CLOSED",
    bucket: "HARD",
    confidence: "0.97",
    retryDate: "-",
    status: "NO RETRY",
    expectedRecovery: "₹0"
  },
  {
    customerId: "CUST_98377",
    reasonCode: "UPI_LIMIT_EXCEEDED",
    bucket: "SOFT",
    confidence: "0.61",
    retryDate: "07 May 2025, 09:30 AM",
    status: "RETRY RECOMMENDED",
    expectedRecovery: "₹6,480"
  },
  {
    customerId: "CUST_98378",
    reasonCode: "INVALID_MANDATE",
    bucket: "HARD",
    confidence: "0.99",
    retryDate: "-",
    status: "NO RETRY",
    expectedRecovery: "₹0"
  },
  {
    customerId: "CUST_98379",
    reasonCode: "UNKNOWN_REASON_CODE",
    bucket: "UNCERTAIN",
    confidence: "0.42",
    retryDate: "-",
    status: "MANUAL REVIEW",
    expectedRecovery: "-"
  },
  {
    customerId: "CUST_98380",
    reasonCode: "SALARY_DELAYED",
    bucket: "SOFT",
    confidence: "0.76",
    retryDate: "08 May 2025, 10:30 AM",
    status: "RETRY RECOMMENDED",
    expectedRecovery: "₹18,400"
  }
];

export const bucketSummaryData = {
  hardDeclines: { count: "18,765", percentage: "40.9%" },
  softDeclines: { count: "21,634", percentage: "47.2%" },
  uncertain: { count: "5,413", percentage: "11.8%" },
  scheduledRetries: "8,921",
  resolvedRecovered: "4,203",
  resolvedNotRecovered: "3,591",
  skippedByEvGate: "12,842"
};

export const hardDeclineReportData = {
  hardDeclinesCount: "18,765",
  expectedRevenueLoss: "₹1,83,14,000",
  fileName: "Netflix_Hard_Declines_12May2025.csv",
  fileSize: "15.2 MB",
  topReasons: [
    { reasonCode: "CARD_EXPIRED", count: "6,842", percentage: "36.4%" },
    { reasonCode: "MANDATE_REVOKED", count: "4,281", percentage: "22.8%" },
    { reasonCode: "ACCOUNT_CLOSED", count: "3,921", percentage: "20.9%" },
    { reasonCode: "CUSTOMER_BLOCKED", count: "1,872", percentage: "10.0%" },
    { reasonCode: "OTHERS", count: "1,849", percentage: "9.9%" }
  ]
};

export const backtestData = {
  policyRecoveredRevenue: "₹1,27,31,860",
  policyRetries: "8,921",
  naiveRetryRecoveredRevenue: "₹78,64,210",
  naiveRetries: "21,763",
  improvement: "₹48,67,650",
  improvementPercentage: "+63%",
  retriesAvoided: "12,842",
  retriesAvoidedPercentage: "45.6%",
  seed: 42,
  runId: "BT_20250512_1042",
  baselineDescription: "Baseline: Naive retry everything on same data set"
};
