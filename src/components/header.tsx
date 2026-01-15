"use client";

import Link from "next/link";

export const Header = () => {
    return (
        <header className="fixed top-0 left-0 z-50 p-6 pointer-events-none">
            <Link href="/" className="flex items-center gap-3 pointer-events-auto group">
                <div className="w-10 h-10 bg-gradient-to-br from-bmb-white to-bmb-accent-cyan rounded-md shadow-lg shadow-bmb-accent-cyan/20 group-hover:scale-105 transition-transform duration-300" />
                <h1 className="text-xl font-bold tracking-tighter text-white drop-shadow-md">BOX MACHI BOX</h1>
            </Link>
        </header>
    );
};
