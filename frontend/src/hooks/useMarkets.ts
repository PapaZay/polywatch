import {useQuery} from "@tanstack/react-query";
import {fetchMarkets} from "../lib/api.ts";

export function useMarkets(page= 1, pageSize = 20, search = "") {
    return useQuery({
        queryKey: ["markets", page, pageSize, search],
        queryFn: () => fetchMarkets(page, pageSize, search),
        refetchInterval: 60_000,
    });
}