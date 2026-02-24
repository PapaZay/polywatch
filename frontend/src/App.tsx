import {Routes, Route} from "react-router-dom";
import Layout from "./components/Layout";
import Dashboard from "./pages/Dashboard.tsx";
import Calibration from "./pages/Calibration.tsx";
import MarketDetail from "./pages/MarketDetail.tsx";

function App() {
    return (
        <Layout>
            <Routes>
                <Route path="/" element={<Dashboard />} />
                <Route path="/calibration" element={<Calibration />} />
                <Route path="/markets/:marketId" element={<MarketDetail />} />
            </Routes>
        </Layout>
    )
}

export default App;
