import {useQuery} from "@tanstack/react-query";
import {fetchActiveSignals} from "../lib/api.ts";

export function useActiveSignals(limit = 20, signalType?: string){
    return useQuery({
        queryKey: ["signals", "active", limit, signalType],
        queryFn: () => fetchActiveSignals(limit, signalType),
        refetchInterval: 30_000,
    });
}