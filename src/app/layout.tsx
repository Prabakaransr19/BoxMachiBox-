import type { Metadata } from "next";
import "./globals.css";

import { Navigation } from "@/components/navigation";
import { Header } from "@/components/header";

export const metadata: Metadata = {
  title: "Box Machi Box | F1 Analysis Platform",
  description: "Advanced Formula 1 analysis and prediction platform.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="font-sans antialiased bg-bmb-bg text-bmb-text">
        <Header />
        <Navigation />
        {children}
      </body>
    </html>
  );
}
