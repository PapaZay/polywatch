import Footer from "../components/Footer";

interface LayoutProps {
    children: React.ReactNode;
}

export default function Layout({children}: LayoutProps) {
    return (
        <div className="min-h-screen bg-gray-950 text-gray-100 flex flex-col">
            <header className="border-b border-gray-800 px-6 py-4">
                <div className="max-w-7xl mx-auto flex items-center justify-between">
                    <h1 className="text-xl font-bold tracking-tight">Polywatch</h1>
                    <nav className="flex gap-4 text-sm text-gray-400">
                        <a href="/" className="hover:text-white">Dashboard</a>
                        <a href="/calibration" className="hover:text-white">Calibration</a>
                    </nav>
                </div>
            </header>
            <main className="max-w-7xl mx-auto px-6 py-6 flex-1 w-full">
                {children}
            </main>
            <Footer />
        </div>
    );
}