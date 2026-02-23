import { useQuery } from "@tanstack/react-query";
import { fetchSignalHistory } from "../lib/api";

export function useSignalHistory(marketId: string){
    return useQuery({
        queryKey: ["signalHistory", marketId],
        queryFn: () => fetchSignalHistory(marketId),
        refetchInterval: 60_000,
        enabled: !!marketId,
    })
}