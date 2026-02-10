import {type Signal, type VolumeSpikeMeta, type PriceMomentumMeta} from "../types.ts";

interface SignalCardProps{
    signal: Signal;
}

function formatRelativeTime(iso: string): string {
    const diff = Date.now() - new Date(iso).getTime();
    const minutes = Math.floor(diff / 60000);
    if (minutes < 60) return `${minutes}m ago`;
    const hours = Math.floor(minutes / 60);
    if (hours < 24) return `${hours}h ago`;
    return `${Math.floor(hours / 24)}d ago`;
}

export default function SignalCard({signal}: SignalCardProps) {
    const isVolume = signal.signal_type === "volume_spike";
    const meta = signal.metadata;

    const confidenceColor = signal.confidence && signal.confidence >= 0.7
            ? "border-red-500 bg-red-500/10"
            : signal.confidence && signal.confidence >= 0.4
            ? "border-yellow-500 bg-yellow-500/10"
            : "border-blue-500 bg-blue-500/10";

    const label = isVolume ? "Volume Spike" : "Price Momentum";

    const timeAgo = signal.detected_at ? formatRelativeTime(signal.detected_at) : "unknown";

    return (
        <div className={`rounded-lg border p-4 ${confidenceColor}`}>
            <div className="flex items-center justify-between mb-2">
                <span className="text-xs font-semibold uppercase tracking-wider">
                    {label}
                </span>
                <span className="text-xs text-gray-400">{timeAgo}</span>
            </div>

            <p className="text-sm text-gray-300 mb-2 truncate">
                {signal.title ?? signal.market_id}
            </p>

            {isVolume && meta && (
                <div className="text-xs text-gray-400 space-y-1">
                    <p>Z-Score: {(meta as VolumeSpikeMeta).z_score}</p>
                    <p>Avg Volume: {(meta as VolumeSpikeMeta).avg_volume.toLocaleString()}</p>
                </div>
            )}
            {!isVolume && meta && (
                <div className="text-xs text-gray-400 space-y-1">
                    <p>Direction: {(meta as PriceMomentumMeta).direction}</p>
                    <p>Change: {((meta as PriceMomentumMeta).change * 100).toFixed(1)}%</p>
                </div>
            )}

            <div className="mt-3">
                <div className="flex justify-between text-xs mb-1">
                    <span className="text-gray-500">Confidence</span>
                    <span>{signal.confidence ? (signal.confidence * 100).toFixed(0) + "%": "N/A"}</span>
                </div>
                <div className="w-full bg-gray-800 rounded-full h-1.5">
                    <div
                        className="h-1.5 rounded-full bg-current"
                        style={{width: `${(signal.confidence ?? 0) * 100}%`}}
                    />
                </div>
            </div>
        </div>
    );
}