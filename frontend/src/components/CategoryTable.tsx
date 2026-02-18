import type { CategoryBreakdown } from "../types";

interface CategoryTableProps {
    categories: CategoryBreakdown[];
}

export default function CategoryTable({categories}: CategoryTableProps) {
    if (categories.length === 0) {
        return <div className="text-gray-500 text-sm py-8 text-center">No category data yet...</div>
    }

    return (
        <div className="overflow-x-auto">
            <table className="w-full">
                <thead>
                    <tr className="border-b border-gray-700 text-left text-xs text-gray-500 uppercase tracking-wider">
                        <th className="py-3 px-4">Category</th>
                        <th className="py-3 px-4 text-right">Brier Score</th>
                        <th className="py-3 px-4 text-right">Markets</th>
                    </tr>
                </thead>
                <tbody>
                    {categories.map((cat) => {
                        const color = cat.brier_score < 0.1 ? "text-green-400" : cat.brier_score < 0.2 ? "text-yellow-400" : "text-red-400"

                        return (
                            <tr key={cat.category} className="border-b border-gray-800">
                                <td className="py-3 px-4 text-sm">{cat.category}</td>
                                <td className={`py-3 px-4 text-sm text-right font-mono ${color}`}>
                                    {cat.brier_score.toFixed(4)}
                                </td>
                                <td className="py-3 px-4 text-sm text-right text-gray-400">
                                    {cat.count}
                                </td>
                            </tr>
                        )
                     })}
                </tbody>
            </table>
        </div>
    )
}