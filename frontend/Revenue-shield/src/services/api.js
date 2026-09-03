/**
 * Revenue Shield AI - API Client Layer
 * Handles communication with backend endpoints with resilient fallback
 */

import { MERCHANTS, generateDashboardPayload } from './simulator';

const API_BASE = import.meta.env.VITE_API_BASE || '';

export async function fetchMerchants() {
  try {
    const res = await fetch(`${API_BASE}/api/merchants/`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    if (Array.isArray(data) && data.length > 0) {
      return data;
    }
  } catch (err) {
    console.warn('Backend merchants API unreachable, using simulated merchants list:', err.message);
  }
  return MERCHANTS;
}

export async function fetchDashboard(merchantId = 'MERCH_001', seed = 42) {
  try {
    const res = await fetch(`${API_BASE}/api/dashboard/?merchant_id=${encodeURIComponent(merchantId)}&seed=${encodeURIComponent(seed)}`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    if (data && data.merchantContext) {
      return data;
    }
  } catch (err) {
    console.warn('Backend dashboard API unreachable, computing payload locally:', err.message);
  }
  return generateDashboardPayload(merchantId, seed);
}

export async function runBacktest(merchantId = 'MERCH_001', seed = null) {
  const effectiveSeed = seed !== null ? seed : Math.floor(Math.random() * 10000);
  try {
    const res = await fetch(`${API_BASE}/api/backtest/run/?merchant_id=${encodeURIComponent(merchantId)}&seed=${encodeURIComponent(effectiveSeed)}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    });
    if (!res.ok) {
      // Try GET if POST is not permitted
      const getRes = await fetch(`${API_BASE}/api/backtest/run/?merchant_id=${encodeURIComponent(merchantId)}&seed=${encodeURIComponent(effectiveSeed)}`);
      if (!getRes.ok) throw new Error(`HTTP ${getRes.status}`);
      const data = await getRes.json();
      if (data && data.merchantContext) return data;
    } else {
      const data = await res.json();
      if (data && data.merchantContext) return data;
    }
  } catch (err) {
    console.warn('Backend backtest API unreachable, simulating backtest run:', err.message);
  }
  return generateDashboardPayload(merchantId, effectiveSeed);
}
