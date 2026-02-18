import {Routes, Route} from "react-router-dom";
import Layout from "./components/Layout";
import Dashboard from "./pages/Dashboard.tsx";
import Calibration from "./pages/Calibration.tsx";

function App() {
    return (
        <Layout>
            <Routes>
                <Route path="/" element={<Dashboard />} />
                <Route path="/calibration" element={<Calibration />} />
            </Routes>
        </Layout>
    )
}

export default App;
