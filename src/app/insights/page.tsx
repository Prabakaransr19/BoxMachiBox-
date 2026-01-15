import { InsightsView } from "@/components/insights-view";

export default function InsightsPage() {
    return (
        <main className="min-h-screen bg-bmb-bg flex flex-col pt-24 pb-10">
            <InsightsView />

            <footer className="w-full py-8 text-center text-neutral-700 text-sm mt-auto">
                <p>&copy; {new Date().getFullYear()} Box Machi Box. Model Architecture Stats.</p>
            </footer>
        </main>
    );
}
