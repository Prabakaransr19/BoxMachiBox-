"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { motion } from "framer-motion";

const navItems = [
    { name: "Home", path: "/" },
    { name: "Analysis", path: "/analyze" },
    { name: "Standings", path: "/standings" },
    { name: "Driver Info", path: "/driver-info" },
    { name: "Insights", path: "/insights" },
];

export const Navigation = () => {
    const pathname = usePathname();

    return (
        <nav className="fixed top-6 right-6 z-50 flex items-center gap-4">
            {navItems.map((item) => {
                const isActive = pathname === item.path;

                // Don't show the link if it's the active page
                if (isActive) return null;

                return (
                    <Link key={item.path} href={item.path}>
                        <motion.span
                            whileHover={{ scale: 1.05 }}
                            whileTap={{ scale: 0.95 }}
                            className="text-xs md:text-sm font-medium text-neutral-400 hover:text-white uppercase tracking-wider transition-colors cursor-pointer backdrop-blur-sm bg-neutral-900/30 px-3 py-1.5 rounded-full border border-neutral-800 hover:border-bmb-accent-cyan/50"
                        >
                            {item.name}
                        </motion.span>
                    </Link>
                );
            })}
        </nav>
    );
};
