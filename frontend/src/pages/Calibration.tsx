import { useCalibration } from "../hooks/useCalibration";
import BrierScoreCard from "../components/BrierScoreCard";
import CalibrationChart from "../components/CalibrationChart";
import CategoryTable from "../components/CategoryTable";

export default function Calibration() {
    const {data, isLoading, error} = useCalibration()

    if (isLoading) {
        return <div className="text-gray-500 text-sm py-8 text-center">Loading calibration data...</div>
    }

    if (error) {
        return (
            <div className="text-red-400 text-sm py-4 bg-red-500/10 rounded-lg px-4">
                Failed to load calibration data: {error.message}
            </div>
        )
    }

    if (!data || data.market_count === 0) {
        return (
        <div className="text-gray-500 text-sm py-8 text-center">No resolved markets yet. Calibration data will appear here as tracked market resolve.</div>
    )
    }

    return (
        <div className="space-y-8">
            <section>
                <p className="text-center text-yellow-200">This is a new feature so data will take time to populate as markets resolve.</p>
                <div className="flex items-center justify-between mb-4">
                    <h2 className="text-lg font-semibold">Calibration Analysis</h2>
                    <span className="text-xs text-gray-500">Auto refreshes every 5 mins</span>
                </div>
                <BrierScoreCard brierScore={data.brier_score} marketCount={data.market_count} />
            </section>

            <section>
                <h3 className="text-md font-semibold mb-4">Calibration Curve - How well do market prices predict outcomes? </h3>
                <p className="text-xs text-gray-500 mb-4">
                    The dashed line represents perfect calibration.
                </p>
                <CalibrationChart bins={data.calibration_curve} />
            </section>

            <section>
                <h3 className="text-md font-semibold mb-4">Category Breakdown</h3>
                <CategoryTable categories={data.category_breakdown} />
            </section>
        </div>
    )
}