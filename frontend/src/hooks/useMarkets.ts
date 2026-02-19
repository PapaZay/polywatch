import {useQuery} from "@tanstack/react-query";
import {fetchMarkets} from "../lib/api.ts";

export function useMarkets(page= 1, pageSize = 20) {
    return useQuery({
        queryKey: ["markets", page, pageSize],
        queryFn: () => fetchMarkets(page, pageSize),
        refetchInterval: 60_000,
    });
}