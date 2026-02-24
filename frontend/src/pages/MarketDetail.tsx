import { useSnapshots } from "../hooks/useSnapshots";
import { useParams, Link } from "react-router-dom";
import { useSignalHistory } from "../hooks/useSignalHistory";
import PriceChart from "../components/PriceChart";
import SignalCard from "../components/SignalCard";
export default function MarketDetail(){
    const {marketId} = useParams<{marketId: string}>();
    const snapshots = useSnapshots(marketId ?? "");
    const signalHistory = useSignalHistory(marketId ?? "");

    return (
        <div className="space-y-8">
            <div>
                <Link to="/" className="text-sm text-gray-400 hover:text-white transition-colors">
                    ← Back to Dashboard
                </Link>
            </div>

            <section>
                <h2 className="text-lg font-semibold mb-4">Price History</h2>
                {snapshots.isLoading && <div className="text-gray-500 text-sm py-8 text-center">Loading chart...</div>}
                {snapshots.error && <div className="text-red-400 text-sm py-4 bg-red-500/10 rounded-lg px-4">Failed to load snapshots</div>}
                {snapshots.data && <PriceChart snapshots={snapshots.data} />}
            </section>

            <section>
                <h2 className="text-lg font-semibold mb-4">Signal History</h2>
                {signalHistory.isLoading && <div className="text-gray-500 text-sm py-8 text-center">Loading signals...</div>}
                {signalHistory.error && <div className="text-red-400 text-sm py-4 bg-red-500/10 rounded-lg px-4">Failed to load signals</div>}
                {signalHistory.data?.length === 0 && <div className="text-gray-500 text-sm py-8 text-center">No signals for this market</div>}
                <div className="space-y-3">{signalHistory.data?.map((signal) => (<SignalCard key={signal.id} signal={signal} />))}</div>
            </section>

        </div>
    )

}