import type {Market} from "../types";

interface MarketRowProps {
    market: Market;
}

export default function MarketRow({market}: MarketRowProps){
    let yesPrice: number | null = null;
    let noPrice: number | null = null;
    try {
        const prices = JSON.parse(market.outcomePrices);
        yesPrice = parseFloat(prices[0]);
        noPrice = prices[1] ? parseFloat(prices[1]) : null;
    } catch {

    }

    const volume = parseFloat(market.volume) || 0;

    return (
        <tr className="border-b border-gray-800 hover:bg-gray-900/50 transition-colors">
            <td className="py-3 px-4 text-sm max-w-md">
                <span className="text-gray-100">{market.question}</span>
            </td>
            <td className="py-3 px-4 text-sm">
                {market.category ? (
                    <span className="px-2 py-0.5 rounded-full bg-gray-800 text-gray-300 text-xs">
                        {market.category}
                    </span>
                ) : (
                    <span className="text-gray-600 text-xs">--</span>
                )}
            </td>
            <td className="py-3 px-4 text-sm text-right font-mono">
                {yesPrice !== null ? (
                    <span className="text-green-400">{(yesPrice * 100).toFixed(1)}c</span>
                ) : (
                    "--"
                )}
            </td>
            <td className="py-3 px-4 text-sm text-right font-mono">
                {noPrice !== null ? (
                    <span className="text-red-400">{(noPrice * 100).toFixed(1)}c</span>
                    ) : (
                        "--"
                    )}
            </td>
            <td className="py-3 px-4 text-sm text-right font-mono text-gray-400">
                ${volume >= 1_000_000 ? (volume / 1_000_000).toFixed(1) + "M"
                : volume >= 1_000 ? (volume / 1_000).toFixed(1) + "K"
                : volume.toFixed(0)}
            </td>
        </tr>
    );
}