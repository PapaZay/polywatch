export interface VolumeSpikeMeta {
    current_volume: number;
    avg_volume: number;
    std_dev: number;
    z_score: number;
}

export interface PriceMomentumMeta {
    current_price: number;
    earlier_price: number;
    change: number;
    direction: "up" | "down"
}

export type SignalMetadata = VolumeSpikeMeta | PriceMomentumMeta;

export interface Signal {
    id: string;
    market_id: string;
    title?: string;
    signal_type: "volume_spike" | "price_momentum";
    confidence: number | null;
    detected_at: string | null;
    metadata: SignalMetadata | null;
}

export interface Market {
    id: string;
    question: string;
    category: string | null;
    volume: string;
    outcomePrices: string;
}