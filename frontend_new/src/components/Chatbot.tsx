"use client";

import React, { useState, useRef, useEffect } from 'react';
import { MessageSquare, Send, X, Bot, User, Loader2 } from 'lucide-react';
import { Button } from "@/components/ui/button";
import { Card, CardHeader, CardTitle, CardContent, CardFooter } from "@/components/ui/card";
import { Input } from "@/components/ui/input";

interface Message {
    role: 'user' | 'bot';
    content: string;
}

interface ChatbotProps {
    sessionId: string | null;
    currentPhase: number;
    isOpen: boolean;
    setIsOpen: (open: boolean) => void;
    initialInput?: string;
}

export default function Chatbot({ sessionId, currentPhase, isOpen, setIsOpen, initialInput }: ChatbotProps) {
    const [messages, setMessages] = useState<Message[]>([
        { role: 'bot', content: "Hi! I'm your Codebasics Data Factory Assistant. How can I help you with this data challenge?" }
    ]);
    const [input, setInput] = useState(initialInput || '');
    const [loading, setLoading] = useState(false);
    const scrollRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        if (initialInput) setInput(initialInput);
    }, [initialInput]);

    useEffect(() => {
        if (scrollRef.current) {
            scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
        }
    }, [messages]);

    const handleSend = async () => {
        if (!input.trim()) return;

        const userMsg = input.trim();
        setInput('');
        setMessages(prev => [...prev, { role: 'user', content: userMsg }]);
        setLoading(true);

        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    session_id: sessionId || '',
                    message: userMsg,
                    phase: currentPhase.toString()
                })
            });

            if (!response.ok) throw new Error('Chat failed');
            const data = await response.json();
            setMessages(prev => [...prev, { role: 'bot', content: data.response }]);
        } catch (error) {
            setMessages(prev => [...prev, { role: 'bot', content: "Sorry, I'm having trouble connecting right now." }]);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="fixed bottom-6 right-6 z-50">
            {isOpen ? (
                <Card className="w-80 sm:w-96 h-[500px] shadow-2xl border-2 border-blue-100 flex flex-col animate-in slide-in-from-bottom-5">
                    <CardHeader className="bg-gradient-to-r from-blue-600 to-purple-600 text-white p-4">
                        <div className="flex justify-between items-center">
                            <div className="flex items-center gap-2">
                                <Bot size={20} />
                                <CardTitle className="text-lg">Factory Assistant</CardTitle>
                            </div>
                            <Button variant="ghost" size="icon" className="text-white hover:bg-white/20" onClick={() => setIsOpen(false)}>
                                <X size={20} />
                            </Button>
                        </div>
                    </CardHeader>
                    <CardContent className="flex-1 overflow-y-auto p-4 space-y-4" ref={scrollRef}>
                        {messages.map((msg, i) => (
                            <div key={i} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                                <div className={`max-w-[80%] p-3 rounded-2xl text-sm ${msg.role === 'user'
                                    ? 'bg-blue-600 text-white rounded-tr-none'
                                    : 'bg-slate-100 text-slate-800 rounded-tl-none'
                                    }`}>
                                    {msg.content}
                                </div>
                            </div>
                        ))}
                        {loading && (
                            <div className="flex justify-start">
                                <div className="bg-slate-100 p-3 rounded-2xl rounded-tl-none">
                                    <Loader2 size={16} className="animate-spin text-blue-600" />
                                </div>
                            </div>
                        )}
                    </CardContent>
                    <CardFooter className="p-3 border-t bg-slate-50">
                        <form
                            className="flex w-full gap-2"
                            onSubmit={(e) => { e.preventDefault(); handleSend(); }}
                        >
                            <Input
                                placeholder="Ask me anything..."
                                value={input}
                                onChange={(e) => setInput(e.target.value)}
                                className="bg-white"
                            />
                            <Button type="submit" size="icon" disabled={loading || !input.trim()}>
                                <Send size={18} />
                            </Button>
                        </form>
                    </CardFooter>
                </Card>
            ) : (
                <Button
                    onClick={() => setIsOpen(true)}
                    className="w-14 h-14 rounded-full shadow-lg bg-gradient-to-r from-blue-600 to-purple-600 hover:scale-110 transition-transform"
                >
                    <MessageSquare size={24} />
                </Button>
            )}
        </div>
    );
}
