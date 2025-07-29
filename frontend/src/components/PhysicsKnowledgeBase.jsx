import React, { useState } from 'react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import SessionsSidebar from './SessionsSidebar';

const PhysicsKnowledgeBase = () => {
    const [searchQuery, setSearchQuery] = useState('');
    const [searchResults, setSearchResults] = useState([]);
    const [isSearching, setIsSearching] = useState(false);
    const [activeSessionId, setActiveSessionId] = useState(1);
    const [sidebarOpen, setSidebarOpen] = useState(true);

    // Mock search results for demonstration
    const mockSearchResults = {
        "ohm's law": [
            {
                id: 1,
                title: "Ohm's Law Fundamentals",
                excerpt: "Ohm's Law states that the current through a conductor between two points is directly proportional to the voltage across the two points. The mathematical relationship is V = IR, where V is voltage, I is current, and R is resistance.",
                source: "Physics Textbook - Chapter 18: Electric Circuits"
            },
            {
                id: 2,
                title: "Resistance and Current",
                excerpt: "When a voltage is applied across a resistor, the current that flows through it is inversely proportional to the resistance. This fundamental relationship forms the basis of Ohm's Law and is essential for understanding electrical circuits.",
                source: "Physics Textbook - Chapter 18: Electric Circuits"
            },
            {
                id: 3,
                title: "Practical Applications",
                excerpt: "Ohm's Law is used extensively in circuit analysis, allowing engineers to calculate voltage drops, current flow, and power dissipation in electrical systems. It's the foundation of electrical engineering principles.",
                source: "Physics Textbook - Chapter 18: Electric Circuits"
            }
        ],
        "newton's laws": [
            {
                id: 4,
                title: "Newton's First Law - Inertia",
                excerpt: "An object at rest stays at rest and an object in motion stays in motion with the same speed and in the same direction unless acted upon by an unbalanced force. This is the law of inertia.",
                source: "Physics Textbook - Chapter 4: Newton's Laws of Motion"
            },
            {
                id: 5,
                title: "Newton's Second Law - Force and Acceleration",
                excerpt: "The acceleration of an object is directly proportional to the net force acting on it and inversely proportional to its mass. F = ma is the mathematical expression of this law.",
                source: "Physics Textbook - Chapter 4: Newton's Laws of Motion"
            },
            {
                id: 6,
                title: "Newton's Third Law - Action and Reaction",
                excerpt: "For every action, there is an equal and opposite reaction. When one object exerts a force on a second object, the second object exerts an equal force in the opposite direction on the first object.",
                source: "Physics Textbook - Chapter 4: Newton's Laws of Motion"
            }
        ],
        "quantum mechanics": [
            {
                id: 7,
                title: "Wave-Particle Duality",
                excerpt: "Quantum mechanics reveals that particles can exhibit both wave-like and particle-like properties. This duality is fundamental to understanding the behavior of matter at the atomic and subatomic levels.",
                source: "Physics Textbook - Chapter 25: Quantum Physics"
            },
            {
                id: 8,
                title: "Heisenberg Uncertainty Principle",
                excerpt: "It is impossible to simultaneously know both the position and momentum of a particle with absolute precision. The more precisely we know one, the less precisely we can know the other.",
                source: "Physics Textbook - Chapter 25: Quantum Physics"
            },
            {
                id: 9,
                title: "Quantum Superposition",
                excerpt: "A quantum system can exist in multiple states simultaneously until measured. This superposition principle is the basis for quantum computing and many quantum phenomena.",
                source: "Physics Textbook - Chapter 25: Quantum Physics"
            }
        ]
    };

    const handleSearch = () => {
        if (!searchQuery.trim()) return;

        setIsSearching(true);

        // Simulate API call delay
        setTimeout(() => {
            const query = searchQuery.toLowerCase();
            let results = [];

            // Search through mock data
            Object.keys(mockSearchResults).forEach(key => {
                if (key.includes(query) || query.includes(key)) {
                    results = [...results, ...mockSearchResults[key]];
                }
            });

            setSearchResults(results);
            setIsSearching(false);
        }, 500);
    };

    const handleKeyPress = (e) => {
        if (e.key === 'Enter') {
            handleSearch();
        }
    };

    const handleSessionSelect = (sessionId) => {
        setActiveSessionId(sessionId);
        setSearchResults([]);
        setSearchQuery('');
    };

    const toggleSidebar = () => {
        setSidebarOpen(!sidebarOpen);
    };

    return (
        <div className="flex h-screen bg-gradient-to-br from-indigo-900 via-purple-800 to-violet-900">
            {/* Sessions Sidebar */}
            <div className={`transition-all duration-300 ease-in-out ${sidebarOpen ? 'w-80' : 'w-0'
                }`}>
                <div className={`h-full ${sidebarOpen ? 'block' : 'hidden'}`}>
                    <SessionsSidebar
                        onSessionSelect={handleSessionSelect}
                        activeSessionId={activeSessionId}
                    />
                </div>
            </div>

            {/* Main Content */}
            <div className="flex-1 overflow-y-auto relative">
                {/* Toggle Button */}
                <button
                    onClick={toggleSidebar}
                    className="absolute top-4 left-4 z-10 bg-purple-800/80 hover:bg-purple-700/80 text-white p-2 rounded-lg border border-purple-600 transition-all duration-200 backdrop-blur-sm"
                >
                    {sidebarOpen ? (
                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 19l-7-7 7-7m8 14l-7-7 7-7" />
                        </svg>
                    ) : (
                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 5l7 7-7 7M5 5l7 7-7 7" />
                        </svg>
                    )}
                </button>

                <div className="max-w-4xl mx-auto px-6 py-8">
                    {/* Header */}
                    <div className="text-center mb-8">
                        <h1 className="text-4xl font-bold text-white mb-2">
                            📘 Physics Knowledge Base
                        </h1>
                        <p className="text-purple-200">
                            Search through physics textbook excerpts and concepts
                        </p>
                    </div>

                    {/* Search Section */}
                    <div className="bg-gray-900/80 backdrop-blur-sm rounded-lg shadow-lg border border-gray-700 p-6 mb-8">
                        <div className="flex gap-4">
                            <Input
                                type="text"
                                placeholder="What is Ohm's Law?"
                                value={searchQuery}
                                onChange={(e) => setSearchQuery(e.target.value)}
                                onKeyPress={handleKeyPress}
                                className="flex-1 bg-gray-800 border-gray-600 text-gray-100 placeholder-gray-400 focus:border-yellow-500 focus:ring-yellow-500"
                            />
                            <Button
                                onClick={handleSearch}
                                disabled={isSearching || !searchQuery.trim()}
                                className="px-6 bg-yellow-600 hover:bg-yellow-700 text-gray-900 font-semibold"
                            >
                                {isSearching ? 'Searching...' : 'Search'}
                            </Button>
                        </div>
                    </div>

                    {/* Results Section */}
                    {searchResults.length > 0 && (
                        <div className="space-y-4">
                            <h2 className="text-2xl font-semibold text-white mb-4">
                                Search Results ({searchResults.length})
                            </h2>
                            {searchResults.map((result) => (
                                <Card key={result.id} className="bg-purple-900/50 backdrop-blur-sm border-purple-700 shadow-lg hover:shadow-xl transition-shadow">
                                    <CardHeader>
                                        <CardTitle className="text-lg text-purple-300">
                                            {result.title}
                                        </CardTitle>
                                    </CardHeader>
                                    <CardContent>
                                        <p className="text-purple-200 mb-3 leading-relaxed">
                                            {result.excerpt}
                                        </p>
                                        <p className="text-sm text-purple-400 italic">
                                            Source: {result.source}
                                        </p>
                                    </CardContent>
                                </Card>
                            ))}
                        </div>
                    )}

                    {/* No results message */}
                    {searchQuery && searchResults.length === 0 && !isSearching && (
                        <div className="text-center py-8">
                            <p className="text-purple-300 text-lg">
                                No results found for "{searchQuery}". Try searching for terms like "Ohm's Law", "Newton's Laws", or "Quantum Mechanics".
                            </p>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default PhysicsKnowledgeBase; 