import type {Market} from "../types";
import MarketRow from "./MarketRow.tsx";

interface MarketTableProps {
    markets: Market[];
    isLoading: boolean;
    error: Error | null;
    page: number;
    totalPages: number;
    onPageChange: (page: number) => void;
}

export default function MarketTable({markets, isLoading, error, page, totalPages, onPageChange}: MarketTableProps){
    if (isLoading){
        return <div className="text-gray-500 text-sm py-8 text-center">Loading markets...</div>;
    }

    if (error) {
        return (
            <div className="text-red-400 text-sm py-4 bg-red-500/10 rounded-lg px-4">
                Failed to load markets: {error.message}
            </div>
        );
    }

    if (markets.length === 0){
        return <div className="text-gray-500 text-sm py-8 text-center">No markets found</div>;
    }

    return (
        <div>
        <div className="overflow-x-auto">
            <table className="w-full">
                <thead>
                <tr className="border-b border-gray-700 text-left text-xs text-gray-500 uppercase tracking-wider">
                    <th className="py-3 px-4">Market</th>
                    <th className="py-3 px-4">Category</th>
                    <th className="py-3 px-4 text-right">Yes Price</th>
                    <th className="py-3 px-4 text-right">No Price</th>
                    <th className="py-3 px-4 text-right">Volume</th>
                </tr>
                </thead>
                <tbody>
                {markets.map((market) => (
                    <MarketRow key={market.id} market={market} />
                ))}
                </tbody>
            </table>
        </div>
        {totalPages > 1 && (
            <div className="flex items-center justify-between mt-4 text-sm text-gray-400">
            <button 
                onClick={() => onPageChange(page - 1)}
                disabled={page === 1}
                className="px-3 py-1.5 rounded bg-gray-800 hover:bg-gray-700 disabled:opacity-40 disabled:cursor-not-allowed cursor-pointer">
                Previous
                </button>
                <span>Page {page} of {totalPages}</span>
                <button
                    onClick={() => onPageChange(page + 1)}
                    disabled={page === totalPages}
                    className="px-3 py-1.5 rounded bg-gray-800 hover:bg-gray-700 disabled:opacity-40 disabled:cursor-not-allowed cursor-pointer">
                        Next
                    </button>
            </div>
       )}
       </div>
    );
}