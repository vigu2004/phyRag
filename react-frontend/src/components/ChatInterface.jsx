import React, { useState, useRef, useEffect } from 'react';
import { Send, Plus, Sun, Moon } from 'lucide-react';

const ChatInterface = ({ sidebarOpen, onToggleSidebar, isDarkMode, onToggleDarkMode }) => {
    const [messages, setMessages] = useState([]);
    const [inputValue, setInputValue] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!inputValue.trim() || isLoading) return;

        const userMessage = {
            id: Date.now(),
            role: 'user',
            content: inputValue,
            timestamp: new Date()
        };

        setMessages(prev => [...prev, userMessage]);
        setInputValue('');
        setIsLoading(true);

        try {
            // Send query to backend server - now searches all collections automatically
            const response = await fetch('http://localhost:5000/api/search', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    query: userMessage.content
                })
            });

            const data = await response.json();

            if (data.success) {
                const aiMessage = {
                    id: Date.now() + 1,
                    role: 'assistant',
                    content: data.answer,
                    queryOriginal: data.query_original,
                    queryRephrased: data.query_rephrased,
                    sources: data.sources || [],
                    timestamp: new Date()
                };
                setMessages(prev => [...prev, aiMessage]);
            } else {
                const errorMessage = {
                    id: Date.now() + 1,
                    role: 'assistant',
                    content: `Error: ${data.error}`,
                    timestamp: new Date()
                };
                setMessages(prev => [...prev, errorMessage]);
            }
        } catch (error) {
            const errorMessage = {
                id: Date.now() + 1,
                role: 'assistant',
                content: `Failed to connect to server. Please make sure the backend server is running.`,
                timestamp: new Date()
            };
            setMessages(prev => [...prev, errorMessage]);
        } finally {
            setIsLoading(false);
        }
    };

    const hasMessages = messages.length > 0;

    const formatCollectionName = (name) => {
        if (!name) return '';
        return name.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
    };

    return (
        <div className={`flex flex-col h-full ${hasMessages ? (isDarkMode ? 'bg-[#202123]' : 'bg-gray-50') : (isDarkMode ? 'bg-[#18191A]' : 'bg-white')}`}>
            {/* Header */}
            <div className={`flex items-center justify-between p-6 border-b ${isDarkMode ? 'border-[#2A2B32] bg-[#18191A]' : 'border-gray-200 bg-white'}`}>
                <div className="flex items-center space-x-4">
                    <h1 className={`text-xl font-semibold font-inter ${isDarkMode ? 'text-white' : 'text-gray-900'}`}>
                        Physics, Chemistry & Biology RAG
                    </h1>
                    <span className={`text-sm px-3 py-1 rounded-full ${isDarkMode ? 'bg-[#2A2B32] text-slate-300' : 'bg-gray-100 text-gray-600'}`}>
                        Searches all subjects
                    </span>
                </div>
                <div className="flex items-center space-x-3">
                    <button
                        onClick={onToggleDarkMode}
                        className={`p-2.5 rounded-xl transition-all duration-200 ${isDarkMode ? 'hover:bg-[#2A2B32] text-slate-300' : 'hover:bg-gray-100 text-gray-600'}`}
                    >
                        {isDarkMode ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
                    </button>
                    <button className={`p-2.5 rounded-xl transition-all duration-200 ${isDarkMode ? 'hover:bg-[#2A2B32] text-slate-300' : 'hover:bg-gray-100 text-gray-600'}`}>
                        <Plus className="w-5 h-5" />
                    </button>
                </div>
            </div>

            {/* Messages Area */}
            {hasMessages && (
                <div className="flex-1 overflow-y-auto p-6 space-y-6">
                    {messages.map((message) => (
                        <div
                            key={message.id}
                            className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
                        >
                            <div
                                className={`max-w-[85%] rounded-2xl px-6 py-4 shadow-sm ${message.role === 'user'
                                    ? isDarkMode
                                        ? 'bg-[#1A1B1E] text-white border border-[#2A2B32]'
                                        : 'bg-blue-500 text-white'
                                    : isDarkMode
                                        ? 'bg-[#1A1B1E] text-white border border-[#2A2B32]'
                                        : 'bg-white text-gray-900 border border-gray-200 shadow-sm'
                                    }`}
                            >
                                <p className="text-sm leading-relaxed font-inter">{message.content}</p>

                                {/* Extra info for AI responses */}
                                {message.role === 'assistant' && (
                                    <div className="mt-4 space-y-3">
                                        {/* Rephrased Query */}
                                        {message.queryRephrased && (
                                            <div className={`p-3 rounded-lg text-xs ${isDarkMode ? 'bg-[#2A2B32] text-slate-300' : 'bg-gray-100 text-gray-700'}`}>
                                                <p className="font-medium">Rephrased query</p>
                                                <p className="mt-1 italic">{message.queryRephrased}</p>
                                            </div>
                                        )}

                                        {/* Sources */}
                                        {Array.isArray(message.sources) && message.sources.length > 0 && (
                                            <div className={`p-3 rounded-lg ${isDarkMode ? 'bg-[#111214] border border-[#2A2B32]' : 'bg-gray-50 border border-gray-200'}`}>
                                                <p className={`text-sm font-semibold ${isDarkMode ? 'text-white' : 'text-gray-900'}`}>Sources</p>
                                                <div className="mt-2 space-y-3">
                                                    {message.sources.map((src, idx) => (
                                                        <div key={idx} className={`p-3 rounded-md ${isDarkMode ? 'bg-[#1A1B1E]' : 'bg-white'} border ${isDarkMode ? 'border-[#2A2B32]' : 'border-gray-200'}`}>
                                                            <div className="flex flex-wrap items-center gap-x-3 text-xs">
                                                                <span className={`font-medium ${isDarkMode ? 'text-slate-200' : 'text-gray-800'}`}>{formatCollectionName(src.collection)}</span>
                                                                {src.page !== undefined && src.page !== null && (
                                                                    <span className={`${isDarkMode ? 'text-slate-400' : 'text-gray-500'}`}>Page: {src.page}</span>
                                                                )}
                                                                {typeof src.rerank_score === 'number' && (
                                                                    <span className={`${isDarkMode ? 'text-slate-400' : 'text-gray-500'}`}>Rerank: {src.rerank_score.toFixed(3)}</span>
                                                                )}
                                                                {typeof src.distance === 'number' && (
                                                                    <span className={`${isDarkMode ? 'text-slate-400' : 'text-gray-500'}`}>Similarity: {(1 - src.distance).toFixed(3)}</span>
                                                                )}
                                                            </div>
                                                            <p className={`mt-2 text-sm ${isDarkMode ? 'text-slate-200' : 'text-gray-800'}`}>{src.text}</p>
                                                            {src.metadata && src.metadata.title && (
                                                                <p className={`mt-1 text-xs ${isDarkMode ? 'text-slate-400' : 'text-gray-500'}`}>Title: {src.metadata.title}</p>
                                                            )}
                                                        </div>
                                                    ))}
                                                </div>
                                            </div>
                                        )}
                                    </div>
                                )}

                                <p className={`text-xs mt-3 font-inter ${isDarkMode ? 'opacity-70' : 'text-gray-500'}`}>
                                    {message.timestamp.toLocaleTimeString()}
                                </p>
                            </div>
                        </div>
                    ))}

                    {isLoading && (
                        <div className="flex justify-start">
                            <div className={`rounded-2xl px-6 py-4 shadow-sm ${isDarkMode
                                ? 'bg-[#1A1B1E] border border-[#2A2B32]'
                                : 'bg-white border border-gray-200'
                                }`}>
                                <div className="flex space-x-2">
                                    <div className={`w-2.5 h-2.5 rounded-full animate-bounce ${isDarkMode ? 'bg-slate-400' : 'bg-gray-400'}`}></div>
                                    <div className={`w-2.5 h-2.5 rounded-full animate-bounce ${isDarkMode ? 'bg-slate-400' : 'bg-gray-400'}`} style={{ animationDelay: '0.1s' }}></div>
                                    <div className={`w-2.5 h-2.5 rounded-full animate-bounce ${isDarkMode ? 'bg-slate-400' : 'bg-gray-400'}`} style={{ animationDelay: '0.2s' }}></div>
                                </div>
                            </div>
                        </div>
                    )}

                    <div ref={messagesEndRef} />
                </div>
            )}

            {/* Input Area */}
            <div className={`p-6 ${!hasMessages ? 'flex-1 flex items-center justify-center' : ''}`}>
                <form onSubmit={handleSubmit} className={`flex space-x-4 ${!hasMessages ? 'w-full max-w-4xl' : 'max-w-4xl mx-auto'}`}>
                    <div className="flex-1 relative">
                        <textarea
                            value={inputValue}
                            onChange={(e) => setInputValue(e.target.value)}
                            placeholder="Ask about Physics, Chemistry, or Biology..."
                            className={`w-full px-6 py-4 border rounded-2xl resize-none focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent font-inter shadow-sm ${isDarkMode
                                ? 'border-[#2A2B32] bg-[#1A1B1E] text-white placeholder-slate-400'
                                : 'border-gray-300 bg-white text-gray-900 placeholder-gray-500'
                                }`}
                            rows="1"
                            style={{ minHeight: '56px', maxHeight: '120px' }}
                            onKeyDown={(e) => {
                                if (e.key === 'Enter' && !e.shiftKey) {
                                    e.preventDefault();
                                    handleSubmit(e);
                                }
                            }}
                        />
                    </div>
                    <button
                        type="submit"
                        disabled={!inputValue.trim() || isLoading}
                        className={`px-6 py-4 rounded-2xl transition-all duration-200 flex items-center justify-center shadow-sm hover:shadow-md ${!inputValue.trim() || isLoading
                            ? 'bg-gray-200 text-gray-400 cursor-not-allowed'
                            : 'bg-indigo-500 hover:bg-indigo-600 text-white hover:shadow-lg transform hover:scale-105'
                            }`}
                    >
                        <Send className="w-5 h-5" />
                    </button>
                </form>
            </div>
        </div>
    );
};

export default ChatInterface; 