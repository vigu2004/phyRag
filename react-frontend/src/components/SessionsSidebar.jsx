import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';

const SessionsSidebar = ({ onSessionSelect, activeSessionId }) => {
    const [sessions, setSessions] = useState([
        {
            id: 1,
            title: "Ohm's Law Discussion",
            lastQuery: "What is Ohm's Law?",
            timestamp: "2 hours ago",
            queryCount: 3
        },
        {
            id: 2,
            title: "Newton's Laws Research",
            lastQuery: "Explain Newton's three laws",
            timestamp: "1 day ago",
            queryCount: 5
        },
        {
            id: 3,
            title: "Quantum Mechanics Basics",
            lastQuery: "What is wave-particle duality?",
            timestamp: "3 days ago",
            queryCount: 2
        },
        {
            id: 4,
            title: "Electromagnetic Theory",
            lastQuery: "How do electric and magnetic fields interact?",
            timestamp: "1 week ago",
            queryCount: 4
        }
    ]);

    const handleNewSession = () => {
        const newSession = {
            id: Date.now(),
            title: "New Session",
            lastQuery: "Start a new search...",
            timestamp: "Just now",
            queryCount: 0
        };
        setSessions([newSession, ...sessions]);
        onSessionSelect(newSession.id);
    };

    return (
        <div className="w-80 bg-purple-900/50 backdrop-blur-sm border-r border-purple-700 h-screen overflow-y-auto">
            <div className="p-6">
                <div className="flex items-center justify-between mb-6">
                    <h2 className="text-xl font-semibold text-white">Sessions</h2>
                    <Button
                        onClick={handleNewSession}
                        className="bg-purple-600 hover:bg-purple-700 text-white px-3 py-1 text-sm"
                    >
                        + New
                    </Button>
                </div>

                <div className="space-y-3">
                    {sessions.map((session) => (
                        <Card
                            key={session.id}
                            className={`cursor-pointer transition-all duration-200 hover:bg-purple-800/50 ${activeSessionId === session.id
                                    ? 'bg-purple-600/20 border-purple-500/50'
                                    : 'bg-purple-800/30 border-purple-700'
                                }`}
                            onClick={() => onSessionSelect(session.id)}
                        >
                            <CardHeader className="pb-2">
                                <CardTitle className="text-sm font-medium text-white">
                                    {session.title}
                                </CardTitle>
                            </CardHeader>
                            <CardContent className="pt-0">
                                <p className="text-xs text-purple-300 mb-2 line-clamp-2">
                                    {session.lastQuery}
                                </p>
                                <div className="flex items-center justify-between">
                                    <span className="text-xs text-purple-400">
                                        {session.timestamp}
                                    </span>
                                    <span className="text-xs bg-purple-700 text-purple-200 px-2 py-1 rounded">
                                        {session.queryCount} queries
                                    </span>
                                </div>
                            </CardContent>
                        </Card>
                    ))}
                </div>
            </div>
        </div>
    );
};

export default SessionsSidebar; 