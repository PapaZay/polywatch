import {useActiveSignals} from "../hooks/useSignals.ts";
import {useMarkets} from "../hooks/useMarkets.ts";
import SignalList from "../components/SignalList.tsx";
import MarketTable from "../components/MarketTable.tsx";
import {useState, useRef} from "react";

type SignalFilter = "all" | "volume_spike" | "price_momentum";

export default function Dashboard(){
    const [filter, setFilter] = useState<SignalFilter>("all");
    const signals = useActiveSignals(20, filter === "all" ? undefined: filter);
    const [page, setPage] = useState(1);
    const PAGE_SIZE = 20;
    const markets = useMarkets(page, PAGE_SIZE);
    const totalPages = markets.data ? Math.ceil(markets.data.total / PAGE_SIZE) : 1; 
    const marketsRef = useRef<HTMLElement>(null);
    const handlePageChange = (newPage: number) => {
        setPage(newPage);
        marketsRef.current?.scrollIntoView({behavior: "smooth"});
    }
    const filters: {value: SignalFilter; label: string}[] = [
        {value: "all", label: "All"},
        {value: "volume_spike", label: "Volume Spike"},
        {value: "price_momentum", label: "Price Momentum"},
    ];

    return (
        <div className="space-y-8">
            <section>
                <div className="flex items-center justify-between mb-4">
                    <h2 className="text-lg font-semibold">Active Signals</h2>
                    <span className="text-xs text-gray-500">
                        Auto-refreshes every 30s
                    </span>
                </div>
                <div className="flex gap-1 bg-gray-900 rounded-lg p-1 w-fit mb-4">
                    {filters.map((f) => (
                        <button key={f.value}
                        onClick={() => setFilter(f.value)}
                        className={`px-3 py-1.5 text-sm rounded-md transition-colors cursor-pointer ${
                            filter === f.value ? "bg-gray-700 text-white" : "text-gray-400 hover:text-gray-200"
                        }`}
                        >
                            {f.label}
                        </button>
                    ))}
                </div>
                <SignalList signals={signals.data ?? []} isLoading={signals.isLoading}
                            error={signals.error}
                />
            </section>

            <section ref={marketsRef}>
                <div className="flex items-center justify-between mb-4">
                    <h2 className="text-lg font-semibold">Markets</h2>
                    <span className="text-xs text-gray-500">
                        {markets.data?.total ?? 0} markets
                    </span>
                </div>
                <MarketTable
                    markets={markets.data?.markets ?? []}
                    isLoading={markets.isLoading}
                    error={markets.error}
                    page={page}
                    totalPages={totalPages}
                    onPageChange={handlePageChange}
                />
            </section>
        </div>
    )
}