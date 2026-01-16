import { fetchStandingsData } from "@/lib/api";
import { DriverCard } from "@/components/driver-card";

// Mark as dynamic to skip during static export
export const dynamic = 'error';

export default async function DriverInfoPage() {
    try {
        const { drivers } = await fetchStandingsData();

        return (
            <main className="min-h-screen bg-bmb-bg flex flex-col pt-24 pb-10">
                <div className="text-center mb-10 px-4">
                    <h1 className="text-4xl md:text-6xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-white to-neutral-400 mb-4 tracking-tighter">
                        PILOT DATABASE
                    </h1>
                    <p className="text-neutral-500 text-lg max-w-2xl mx-auto">
                        Complete driver roster and performance analytics.
                    </p>
                </div>

                <div className="w-full max-w-7xl mx-auto px-6 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                    {drivers.map((driver, index) => (
                        <DriverCard key={driver.driver_number} driver={driver} index={index} />
                    ))}
                </div>

                <footer className="w-full py-8 text-center text-neutral-700 text-sm mt-auto">
                    <p>&copy; {new Date().getFullYear()} Box Machi Box. Data via OpenF1.</p>
                </footer>
            </main>
        );
    } catch (error) {
        return (
            <main className="min-h-screen bg-bmb-bg flex flex-col items-center justify-center pt-24 pb-10 px-4">
                <h1 className="text-4xl font-bold text-white mb-4">Driver Database</h1>
                <p className="text-neutral-400 text-center max-w-md">
                    This page requires runtime data fetching. Please deploy to a platform with server-side rendering support (Vercel, Netlify, etc.) or visit during development.
                </p>
            </main>
        );
    }
}
