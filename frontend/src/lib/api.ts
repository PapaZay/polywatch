import type {Signal, Market} from "../types";

const BASE_API_URL = "/api"

export async function fetchActiveSignals (
    limit: number = 20,
    signaltype?: string
): Promise<Signal[]> {
    const params = new URLSearchParams({ limit: String(limit) });
    if (signaltype) params.set("signal_type", signaltype);
    const res = await fetch(`${BASE_API_URL}/signals/active?${params}`);
    if (!res.ok) throw new Error(`Signals fetch failed: ${res.status}`);
    return res.json();
}

export async function fetchSignalHistory(
    marketId: string,
    limit: number = 50
): Promise<Signal[]> {
    const params = new URLSearchParams({ limit: String(limit) });
    const res = await fetch(`${BASE_API_URL}/signals/history/${marketId}?${params}`);
    if (!res.ok) throw new Error(`Signal history fetch failed: ${res.status}`);
    return res.json();
}

export async function fetchMarkets(limit: number = 20): Promise<Market[]> {
    const params = new URLSearchParams({limit: String(limit)});
    const res = await fetch(`${BASE_API_URL}/markets?${params}`);
    if (!res.ok) throw new Error(`Markets fetch failed: ${res.status}`);
    return res.json();
}