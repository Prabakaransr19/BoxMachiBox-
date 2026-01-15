import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

import { Navigation } from "@/components/navigation";
import { Header } from "@/components/header";

const inter = Inter({ subsets: ["latin"], variable: "--font-inter" });

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
      <body className={`${inter.variable} font-sans antialiased bg-bmb-bg text-bmb-text`}>
        <Header />
        <Navigation />
        {children}
      </body>
    </html>
  );
}
