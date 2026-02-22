import { useQuery } from "@tanstack/react-query";
import { fetchSnapshots } from "../lib/api";

export function useSnapshots(marketId: string){
    return useQuery({
        queryKey: ["snapshots", marketId],
        queryFn: () => fetchSnapshots(marketId),
        refetchInterval: 60_000,
        enabled: !!marketId,
    })
}