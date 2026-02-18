import {useQuery} from "@tanstack/react-query";
import { fetchCalibration } from "../lib/api";

export function useCalibration(category?: string){
    return useQuery({
        queryKey: ["calibration", category],
        queryFn: () => fetchCalibration(category),
        refetchInterval: 300_000,
    })
}