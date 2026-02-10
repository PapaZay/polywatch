import {useQuery} from "@tanstack/react-query";
import {fetchMarkets} from "../lib/api.ts";

export function useMarkets(limit = 20) {
    return useQuery({
        queryKey: ["markets", limit],
        queryFn: () => fetchMarkets(limit),
        refetchInterval: 60_000,
    });
}