import {useActiveSignals} from "../hooks/useSignals.ts";
import {useMarkets} from "../hooks/useMarkets.ts";
import SignalList from "../components/SignalList.tsx";
import MarketTable from "../components/MarketTable.tsx";

export default function Dashboard(){
    const signals = useActiveSignals(20);
    const markets = useMarkets(20);

    return (
        <div className="space-y-8">
            <section>
                <div className="flex items-center justify-between mb-4">
                    <h2 className="text-lg font-semibold">Active Signals</h2>
                    <span className="text-xs text-gray-500">
                        Auto-refreshes every 30s
                    </span>
                </div>
                <SignalList signals={signals.data ?? []} isLoading={signals.isLoading}
                            error={signals.error}
                />
            </section>

            <section>
                <div className="flex items-center justify-between mb-4">
                    <h2 className="text-lg font-semibold">Markets</h2>
                    <span className="text-xs text-gray-500">
                        {markets.data?.length ?? 0} markets
                    </span>
                </div>
                <MarketTable markets={markets.data ?? []} isLoading={markets.isLoading}
                             error={markets.error}
                />
            </section>
        </div>
    )
}