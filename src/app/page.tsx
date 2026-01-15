import { ScrollSequence } from "@/components/scroll-sequence";
import { NarrativeBridge } from "@/components/narrative-bridge";
import { FeatureNavigation } from "@/components/feature-navigation";
import { EasterEgg } from "@/components/easter-egg";


export default function Home() {
  return (
    <main className="flex min-h-screen flex-col bg-bmb-bg">
      <ScrollSequence />
      <NarrativeBridge />
      <FeatureNavigation />
      <EasterEgg />


      <footer className="w-full py-8 border-t border-neutral-900 text-center text-neutral-600 text-sm">
        <p>&copy; {new Date().getFullYear()} Box Machi Box. All rights reserved.</p>
      </footer>
    </main>
  );
}
