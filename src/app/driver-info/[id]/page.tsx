import { fetchDriverProfile } from "@/lib/api";
import { DriverProfile } from "@/components/driver-profile";
import { notFound } from "next/navigation";

export default async function DriverProfilePage({ params }: { params: { id: string } }) {
    const driverNumber = parseInt(params.id);

    if (isNaN(driverNumber)) {
        notFound();
    }

    const profileData = await fetchDriverProfile(driverNumber);

    if (!profileData) {
        notFound();
    }

    // Unpack data
    // fetchDriverProfile returns { ...driverStanding, history }
    const { history, ...driver } = profileData;

    return (
        <main className="min-h-screen bg-bmb-bg flex flex-col pt-24 pb-10">
            <DriverProfile driver={driver} history={history} />
        </main>
    );
}
