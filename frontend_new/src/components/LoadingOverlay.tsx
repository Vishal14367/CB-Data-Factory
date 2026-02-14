"use client";

import React, { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Search } from 'lucide-react';

interface LoadingOverlayProps {
    isLoading: boolean;
    messages?: string[];
}

const DEFAULT_MESSAGES = [
    "Analyzing your domain...",
    "Searching for relevant problem statements...",
    "Evaluating best matches...",
    "Finalizing results..."
];

export default function LoadingOverlay({ isLoading, messages = DEFAULT_MESSAGES }: LoadingOverlayProps) {
    const [currentMessageIndex, setCurrentMessageIndex] = useState(0);

    useEffect(() => {
        if (!isLoading) {
            setCurrentMessageIndex(0);
            return;
        }

        const interval = setInterval(() => {
            setCurrentMessageIndex((prev) => (prev + 1) % messages.length);
        }, 2000); // Rotate every 2 seconds

        return () => clearInterval(interval);
    }, [isLoading, messages]);

    return (
        <AnimatePresence>
            {isLoading && (
                <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                    transition={{ duration: 0.3 }}
                    className="fixed inset-0 z-50 flex items-center justify-center bg-white/80 backdrop-blur-sm"
                    role="status"
                    aria-live="polite"
                    aria-label="Loading content"
                >
                    <div className="flex flex-col items-center">
                        {/* Animated Search Icon */}
                        <div className="relative mb-8">
                            <motion.div
                                animate={{ scale: [1, 1.2, 1] }}
                                transition={{ repeat: Infinity, duration: 1.5, ease: "easeInOut" }}
                                className="relative z-10 p-4 bg-white rounded-full shadow-xl border-2 border-blue-100"
                            >
                                <Search className="w-8 h-8 text-blue-600" />
                            </motion.div>
                            {/* Pulsing Waves */}
                            <motion.div
                                animate={{ scale: [1, 2], opacity: [0.5, 0] }}
                                transition={{ repeat: Infinity, duration: 1.5, ease: "easeOut" }}
                                className="absolute inset-0 bg-blue-400 rounded-full opacity-20"
                            />
                            <motion.div
                                animate={{ scale: [1, 3], opacity: [0.3, 0] }}
                                transition={{ repeat: Infinity, duration: 1.5, ease: "easeOut", delay: 0.2 }}
                                className="absolute inset-0 bg-blue-300 rounded-full opacity-20"
                            />
                        </div>

                        {/* Dynamic Text */}
                        <motion.p
                            key={currentMessageIndex}
                            initial={{ opacity: 0, y: 10 }}
                            animate={{ opacity: 1, y: 0 }}
                            exit={{ opacity: 0, y: -10 }}
                            transition={{ duration: 0.3 }}
                            className="text-lg font-medium text-slate-700 text-center min-w-[300px]"
                        >
                            {messages[currentMessageIndex]}
                        </motion.p>
                    </div>
                </motion.div>
            )}
        </AnimatePresence>
    );
}
