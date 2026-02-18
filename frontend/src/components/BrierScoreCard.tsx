interface BrierScoreCardProps {
    brierScore: number | null;
    marketCount: number;
}

export default function BrierScoreCard({brierScore, marketCount}: BrierScoreCardProps) {
    const color = brierScore === null ? "border-gray-700 bg-gray-900" : brierScore < 0.1 ? "border-green-500 bg-green-500/10" 
    : brierScore < 0.2 ? "border-yellow-500 bg-yellow-500/10"
    : "border-red-500 bg-red-500/10"

    return (
        <div className={`rounded-lg border p-6 ${color}`}>
            <h3 className="text-xs font-semibold uppercase tracking-wider text-gray-400 mb-2">
                Brier Score
            </h3>
            <p className="text-3xl font-bold">
                {brierScore !== null ? brierScore.toFixed(4) : "N/A"}
            </p>
            <p className="text-xs text-gray-500 mt-2">
                {marketCount} resolved market{marketCount !== 1 ? "s" : ""}
            </p>
            <p className="text-xs text-gray-600 mt-1">
                Lower is better. 0 = perfect, 0.25 = random
            </p>
        </div>
    )
}