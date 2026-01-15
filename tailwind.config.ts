import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "#101616",
        foreground: "#ededed",
        "bmb-bg": "#101616",
        "bmb-card": "#1a1f1f",
        "bmb-accent-red": "#cf3535",
        "bmb-accent-cyan": "#2a9d8f",
      },
      fontFamily: {
        sans: ["var(--font-inter)"],
      },
    },
  },
  plugins: [],
};
export default config;
