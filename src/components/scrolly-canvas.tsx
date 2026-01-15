"use client";

import { useEffect, useRef, useState, useCallback } from "react";
import { useMotionValueEvent, MotionValue } from "framer-motion";

const FRAME_COUNT = 32;
const IMAGES_DIR = "/car-sequence";

function currentFrame(index: number) {
    return `${IMAGES_DIR}/ezgif-frame-${index.toString().padStart(3, "0")}.jpg`;
}

interface ScrollyCanvasProps {
    scrollProgress: MotionValue<number>;
}

export const ScrollyCanvas = ({ scrollProgress }: ScrollyCanvasProps) => {
    const canvasRef = useRef<HTMLCanvasElement>(null);
    const [images, setImages] = useState<HTMLImageElement[]>([]);
    const [isLoaded, setIsLoaded] = useState(false);

    // Preload images
    useEffect(() => {
        let loadedCount = 0;
        const imgs: HTMLImageElement[] = [];

        for (let i = 1; i <= FRAME_COUNT; i++) {
            const img = new Image();
            img.src = currentFrame(i);
            img.onload = () => {
                loadedCount++;
                if (loadedCount === FRAME_COUNT) {
                    setIsLoaded(true);
                }
            };
            imgs.push(img);
        }
        setImages(imgs);
    }, []);

    // Draw Logic
    const drawImage = useCallback((index: number) => {
        const canvas = canvasRef.current;
        const ctx = canvas?.getContext("2d");
        const img = images[index];

        if (!canvas || !ctx || !img) return;

        // Responsive Canvas Dims
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;

        // Object Fit: Contain Logic
        const hRatio = canvas.width / img.width;
        const vRatio = canvas.height / img.height;
        const ratio = Math.min(hRatio, vRatio);

        // Scale slightly (e.g. 0.8) if you want margins, or 1.0 for fill
        const scale = ratio * 0.9;

        const centerShift_x = (canvas.width - img.width * scale) / 2;
        const centerShift_y = (canvas.height - img.height * scale) / 2;

        ctx.clearRect(0, 0, canvas.width, canvas.height);
        // Optional: Draw background here if needed, but we rely on CSS bg

        ctx.drawImage(
            img,
            0,
            0,
            img.width,
            img.height,
            centerShift_x,
            centerShift_y,
            img.width * scale,
            img.height * scale
        );
    }, [images]);

    // Sync with scroll
    useMotionValueEvent(scrollProgress, "change", (latest) => {
        if (!isLoaded || images.length === 0) return;

        // Map 0-1 to 0-(total-1)
        const frameIndex = Math.min(
            FRAME_COUNT - 1,
            Math.floor(latest * FRAME_COUNT)
        );

        requestAnimationFrame(() => drawImage(frameIndex));
    });

    // Handle Resize
    useEffect(() => {
        const handleResize = () => {
            // Redraw current frame on resize
            const currentScroll = scrollProgress.get();
            const frameIndex = Math.min(
                FRAME_COUNT - 1,
                Math.floor(currentScroll * FRAME_COUNT)
            );
            if (isLoaded) drawImage(frameIndex);
        }
        window.addEventListener('resize', handleResize);
        return () => window.removeEventListener('resize', handleResize);
    }, [isLoaded, scrollProgress, drawImage]);

    // Initial Draw
    useEffect(() => {
        if (isLoaded) drawImage(0);
    }, [isLoaded, drawImage]);

    return (
        <div className="relative w-full h-full flex items-center justify-center">
            {!isLoaded && (
                <div className="absolute inset-0 flex items-center justify-center text-bmb-text">
                    Loading Simulation Model...
                </div>
            )}
            <canvas ref={canvasRef} className="block w-full h-full object-contain" />
        </div>
    );
};
