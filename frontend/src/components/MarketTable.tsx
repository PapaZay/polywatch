import type {Market} from "../types";
import MarketRow from "./MarketRow.tsx";
import { useState } from "react";

interface MarketTableProps {
    markets: Market[];
    isLoading: boolean;
    error: Error | null;
    page: number;
    totalPages: number;
    onPageChange: (page: number) => void;
}

type SortKey = "volume" | "yes" | "no";
type SortDir = "asc" | "desc";

const SortIcon = ({col, sortKey, sortDir}: {col: SortKey; sortKey: SortKey; sortDir: SortDir}) => {
    if (sortKey !== col) return <span className="text-gray-600 ml-1">↕</span>
    return <span className="text-gray-300 ml-1">{sortDir === "asc" ? "↑": "↓"}</span>
}


export default function MarketTable({markets, isLoading, error, page, totalPages, onPageChange}: MarketTableProps){
    const [sortKey, setSortKey] = useState<SortKey>("volume")
    const [sortDir, setSortDir] = useState<SortDir>("desc");

    const handleSort = (key: SortKey) => {
        if (sortKey === key) {
            setSortDir(d => d === "asc" ? "desc" : "asc");
        } else {
            setSortKey(key);
            setSortDir("desc");
        }
    }

    const sorted = [...markets].sort((a,b) => {
        let aVal: number, bVal: number;
        if (sortKey === "volume") {
            aVal = parseFloat(a.volume) || 0;
            bVal = parseFloat(b.volume) || 0;
        } else {
            const idx = sortKey === "yes" ? 0 : 1;
            try {aVal = parseFloat(JSON.parse(a.outcomePrices)[idx]) || 0; } catch {aVal = 0;}
            try {bVal = parseFloat(JSON.parse(b.outcomePrices)[idx]) || 0; } catch {bVal = 0;}
        }
        return sortDir === "asc" ? aVal - bVal : bVal - aVal;
    })


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
                    <th className="py-3 px-4 text-right cursor-pointer hover:text-gray-300" onClick={() => handleSort("yes")}>
                        Yes Price <SortIcon col="yes" sortKey={sortKey} sortDir={sortDir} />
                    </th>
                    <th className="py-3 px-4 text-right cursor-pointer hover:text-gray-300" onClick={() => handleSort("no")}>
                        No Price <SortIcon col="no" sortKey={sortKey} sortDir={sortDir} />
                    </th>
                    <th className="py-3 px-4 text-right cursor-pointer hover:text-gray-300" onClick={() => handleSort("volume")}>
                        Volume <SortIcon col="volume" sortKey={sortKey} sortDir={sortDir} />
                    </th>
                </tr>
                </thead>
                <tbody>
                {sorted.map((market) => (
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