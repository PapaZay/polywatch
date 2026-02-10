import type {Signal} from "../types.ts";
import SignalCard from "./SignalCard.tsx";

interface SignalListProps {
    signals: Signal[];
    isLoading: boolean;
    error: Error | null;
}

export default function SignalList({signals, isLoading, error}: SignalListProps){
    if (isLoading) {
        return (
            <div className="text-gray-500 text-sm py-8 text-center">
                Loading signals...
            </div>
        );
    }

    if (error) {
        return (
            <div className="text-red-400 text-sm py-4 bg-red-500/10 rounded-lg px-4">
                Failed to load signals: {error.message}
            </div>
        );
    }

    if (signals.length === 0) {
        return (
            <div className="text-gray-500 text-sm py-8 text-center border border-dashed border-gray-800 rounded-lg">
                No active signals detected
            </div>
        );
    }

    return (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {signals.map((signal) => (
                <SignalCard key={signal.id} signal={signal} />
            ))}
        </div>
    )
}