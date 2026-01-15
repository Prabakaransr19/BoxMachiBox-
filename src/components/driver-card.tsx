"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import { DriverStanding } from "@/lib/api";

export const DriverCard = ({ driver, index }: { driver: DriverStanding; index: number }) => {
    return (
        <Link href={`/driver-info/${driver.driver_number}`}>
            <motion.div
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.4, delay: index * 0.05 }}
                className="group relative overflow-hidden rounded-xl border border-neutral-800 bg-neutral-900/40 backdrop-blur-sm transition-all duration-300 hover:border-neutral-600 hover:-translate-y-1"
            >
                {/* Team Color Strip */}
                <div
                    className="absolute left-0 top-0 bottom-0 w-1.5 z-10"
                    style={{ backgroundColor: driver.team_colour }}
                />

                <div className="p-6 pl-8">
                    <div className="flex justify-between items-start mb-4">
                        <div>
                            <span className="font-mono text-xs text-neutral-500 uppercase tracking-widest">
                                {driver.team_name}
                            </span>
                            <h3 className="text-xl font-bold text-white mt-1 group-hover:text-bmb-accent-cyan transition-colors">
                                {driver.driver_name}
                            </h3>
                        </div>
                        <div className="text-3xl font-black text-neutral-800 group-hover:text-neutral-700 transition-colors">
                            {driver.driver_number}
                        </div>
                    </div>

                    <div className="flex items-end justify-between mt-6">
                        <div>
                            <div className="text-xs text-neutral-500 font-mono">RANK</div>
                            <div className="text-2xl font-bold text-white">P{driver.position}</div>
                        </div>
                        <div className="text-right">
                            <div className="text-xs text-neutral-500 font-mono">PTS</div>
                            <div className="text-2xl font-bold text-bmb-accent-cyan">{driver.points}</div>
                        </div>
                    </div>
                </div>

                {/* Hover Gradient */}
                <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/5 to-transparent -translate-x-full group-hover:animate-shine pointer-events-none" />
            </motion.div>
        </Link>
    );
};
