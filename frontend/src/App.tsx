import Layout from "./components/Layout";
import SignalCard from "./components/SignalCard";
import type {Signal} from "./types";

const mockSignal: Signal = {
    id: "1",
    market_id: "Will Bitcoin hit $1m before GTA VI?",
    signal_type: "volume_spike",
    confidence: 0.85,
    detected_at: new Date().toISOString(),
    metadata: {
        current_volume: 50000,
        avg_volume: 3000,
        std_dev: 1200,
        z_score: 4.25,
    },
};

function App() {
    return (
        <Layout>
            <h2 className="text-lg font-semibold mb-4">Active Signals</h2>
            <SignalCard signal={mockSignal}/>
        </Layout>
    )
}

export default App;
