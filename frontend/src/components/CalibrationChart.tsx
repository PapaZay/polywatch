import { ComposedChart, Line, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine } from "recharts";
import type { CalibrationBin } from "../types";

interface CalibrationChartProps {
    bins: CalibrationBin[];
}

export default function CalibrationChart({bins}: CalibrationChartProps) {
    const data = bins.filter((b) => b.actual_frequency !== null).map((b) => ({
        predicted: b.avg_predicted,
        actual: b.actual_frequency,
        count: b.count,
        label: `${(b.bin_start * 100).toFixed(0)}-${(b.bin_end * 100).toFixed(0)}%`
    }))

    if (data.length === 0) {
        return (
            <div className="text-gray-500 text-sm py-8 text-center">
                Not enough data for calibration curve
            </div>
        )
    }

    return (
        <ResponsiveContainer width="100%" height={400}>
            <ComposedChart data={data} margin={{ top: 20, right: 20, bottom: 20, left: 20}}>
                <CartesianGrid stroke="#1f2937" strokeDasharray="3 3" />
                <XAxis
                    dataKey="predicted"
                    type="number"
                    domain={[0,1]}
                    tickFormatter={(v: number) => `${(v * 100).toFixed(0)}%`}
                    label={{ value: "Predicted Probability", position: "bottom", fill: "#9ca3af", fontSize: 12}}
                    tick={{ fill: "#9ca3af", fontSize: 12}}
                />
                <YAxis
                    yAxisId="left"
                    type="number"
                    domain={[0, 1]}
                    tickFormatter={(v: number) => `${(v * 100).toFixed(0)}%`}
                    label={{value: "Actual Frequency", angle: -90, position: "insideLeft", fill: "#9ca3af", fontSize: 12}}
                    tick={{fill: "#9ca3af", fontSize: 12}}
                />
                <YAxis
                    yAxisId="right"
                    orientation="right"
                    tick={{fill: "#6b7280", fontSize: 11}}
                    label={{value: "Markets", angle: 90, position: "insideRight", fill: "#6b7280", fontSize: 12}}
                />
                <Tooltip
                    contentStyle={{ backgroundColor: "#111827", border: "1px solid #374151", borderRadius: "8px"}}
                    labelFormatter={(v) => `Predicted: ${(Number(v) * 100).toFixed(0)}%`}
                    formatter={(value, name) =>
                        name === "actual"
                        ? [`${(Number(value) * 100).toFixed(1)}%`, "Actual Frequency"] : [value, "Markets"]
                    
                    }
                />
                <ReferenceLine yAxisId="left" segment={[{ x: 0, y: 0}, { x: 1, y: 1}]} stroke="#4b5563" strokeDasharray="6 4" />
                <Bar yAxisId="right" dataKey="count" fill="#374151" opacity={0.5} barSize={30} />
                <Line yAxisId="left" type="monotone" dataKey="actual" stroke="#22d3ee" strokeWidth={2} dot={{fill: "#22d3ee", r: 5}} />
            </ComposedChart>
        </ResponsiveContainer>
    )
}