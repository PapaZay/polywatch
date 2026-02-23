import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";
import type {Snapshot} from "../types";

interface PriceChartProps {
    snapshots: Snapshot[];
}

export default function PriceChart({ snapshots }: PriceChartProps){
    const data = [...snapshots].reverse().map((s) => ({
        time: new Date(s.timestamp).toLocaleDateString("en-US", {month: "numeric", day: "numeric", hour: "2-digit", minute: "2-digit"}),
        price: parseFloat(s.price.toFixed(3)),
    }));

    if (data.length === 0){
        return <div className="text-gray-500 text-sm py-8 text-center">No price history available</div>
    }

    return (
        <ResponsiveContainer width="100%" height={300}>
            <LineChart data={data} margin={{ top: 10, right: 20, bottom: 20, left: 20}}>
                <CartesianGrid stroke="#1f2937" strokeDasharray="3 3" />
                <XAxis dataKey="time"
                tick={{fill: "#9ca3af", fontSize: 11}} 
                interval="preserveStartEnd"
                />
                <YAxis
                    domain={[0, 1]}
                    tickFormatter={(v: number) => `${(v * 100).toFixed(0)}¢`}
                    tick={{fill: "#9ca3af", fontSize: 11}}
                />
                <Tooltip
                    contentStyle={{backgroundColor: "#111827", border: "1px solid #374151", borderRadius: "8px"}}
                    formatter={(value) => [`${(Number(value) * 100).toFixed(1)}¢`, "Yes Price"]}
                />
                <Line type="monotone" dataKey="price" stroke="#22d3ee" strokeWidth={2} dot={false} />
            </LineChart>
        </ResponsiveContainer>
    )
}