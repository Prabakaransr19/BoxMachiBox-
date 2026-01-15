"use client";

import { motion } from "framer-motion";

export const NarrativeBridge = () => {
    return (
        <section className="relative w-full bg-bmb-bg py-24 md:py-32 flex flex-col items-center justify-center border-t border-neutral-900/50">
            <div className="container mx-auto px-6 max-w-[1000px] text-center">
                {/* Title */}
                <motion.h2
                    initial={{ opacity: 0 }}
                    whileInView={{ opacity: 1 }}
                    transition={{ duration: 0.8, delay: 0 }}
                    viewport={{ once: true, margin: "-100px" }}
                    className="text-3xl md:text-4xl font-bold text-white mb-6 md:mb-8 tracking-tight"
                >
                    After the Chequered Flag
                </motion.h2>

                {/* Subtitle */}
                <motion.p
                    initial={{ opacity: 0 }}
                    whileInView={{ opacity: 1 }}
                    transition={{ duration: 0.8, delay: 0.2 }}
                    viewport={{ once: true }}
                    className="text-lg md:text-xl font-medium text-neutral-400 mb-8 md:mb-10"
                >
                    When the race ends, the analysis begins.
                </motion.p>

                {/* Body Copy */}
                <motion.p
                    initial={{ opacity: 0 }}
                    whileInView={{ opacity: 1 }}
                    transition={{ duration: 0.8, delay: 0.4 }}
                    viewport={{ once: true }}
                    className="text-base md:text-lg text-neutral-300 max-w-[700px] mx-auto leading-relaxed mb-12 md:mb-16"
                >
                    Every lap, stint, and position change is preserved in telemetry. We break it down to reveal pace, consistency, and decisions that shaped the result.
                </motion.p>

                {/* Three Pillars */}
                <motion.div
                    initial={{ opacity: 0 }}
                    whileInView={{ opacity: 1 }}
                    transition={{ duration: 0.8, delay: 0.6 }}
                    viewport={{ once: true }}
                    className="flex flex-col md:flex-row items-center justify-center gap-4 md:gap-8 text-sm text-neutral-500 font-mono tracking-widest uppercase"
                >
                    <span>Pace</span>
                    <span className="hidden md:inline text-neutral-700">•</span>
                    <span>Strategy</span>
                    <span className="hidden md:inline text-neutral-700">•</span>
                    <span>Consistency</span>
                </motion.div>
            </div>
        </section>
    );
};
