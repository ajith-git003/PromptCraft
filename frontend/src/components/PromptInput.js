import React, { useState, useEffect, useCallback } from "react";
import axios from "axios";

const API_URL = "https://promptcraft-tssy.onrender.com";

export default function PromptInput() {
  const [prompt, setPrompt] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [history, setHistory] = useState([]);

  // Load history from localStorage on mount
  useEffect(() => {
    const savedHistory = localStorage.getItem('promptHistory');
    if (savedHistory) {
      try {
        setHistory(JSON.parse(savedHistory));
      } catch (e) {
        console.error('Failed to load history:', e);
      }
    }
  }, []);

  const loadHistoryItem = useCallback((item) => {
    setPrompt(item.prompt);
    setResult(item.result);
  }, []);

  const deleteHistoryItem = useCallback((id) => {
    const newHistory = history.filter(item => item.id !== id);
    setHistory(newHistory);
    localStorage.setItem('promptHistory', JSON.stringify(newHistory));
  }, [history]);

  // Render history items into sidebar
  useEffect(() => {
    const sidebarContent = document.getElementById('history-sidebar-content');
    if (!sidebarContent) return;

    // Clear existing content
    sidebarContent.innerHTML = '';

    if (history.length === 0) {
      const emptyDiv = document.createElement('div');
      emptyDiv.className = 'text-center py-8 px-4';
      emptyDiv.innerHTML = '<p class="text-xs text-gray-500 dark:text-gray-400">No history yet</p>';
      sidebarContent.appendChild(emptyDiv);
    } else {
      history.forEach((item) => {
        // Create container for history item
        const container = document.createElement('div');
        container.className = 'relative mb-2 group';
        
        // Create the main button
        const button = document.createElement('button');
        button.className = 'w-full text-left px-3 py-2 pr-10 rounded-lg bg-beige-50 dark:bg-midnight-900/50 hover:bg-white dark:hover:bg-midnight-700 border border-transparent hover:border-warm-blue dark:hover:border-neon-blue transition-all';
        button.innerHTML = `<p class="text-sm text-gray-800 dark:text-gray-300 truncate">${item.prompt}</p>`;
        button.onclick = () => loadHistoryItem(item);
        
        // Create delete button
        const deleteBtn = document.createElement('button');
        deleteBtn.className = 'absolute right-2 top-1/2 -translate-y-1/2 p-1.5 rounded opacity-0 group-hover:opacity-100 bg-red-100 dark:bg-red-900/30 hover:bg-red-200 dark:hover:bg-red-900/50 transition-all';
        deleteBtn.innerHTML = `<svg class="w-4 h-4 text-red-600 dark:text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/></svg>`;
        deleteBtn.onclick = (e) => {
          e.stopPropagation();
          deleteHistoryItem(item.id);
        };
        
        container.appendChild(button);
        container.appendChild(deleteBtn);
        sidebarContent.appendChild(container);
      });
    }
  }, [history, deleteHistoryItem, loadHistoryItem]);

  const generatePrompt = async () => {
    if (!prompt.trim()) return;

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await axios.post(`${API_URL}/generate`, { prompt });
      setResult(response.data);
      
      // Save to history
      const historyItem = {
        id: Date.now(),
        timestamp: new Date().toISOString(),
        prompt: prompt,
        result: response.data
      };
      
      const newHistory = [historyItem, ...history].slice(0, 20); // Keep only last 20 items
      setHistory(newHistory);
      localStorage.setItem('promptHistory', JSON.stringify(newHistory));
    } catch (err) {
      setError(
        err.response?.data?.detail ||
        "Failed to generate prompt. Please check the backend connection."
      );
    } finally {
      setLoading(false);
    }
  };

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
  };

  return (
    <div className="w-full max-w-7xl mx-auto">
      {/* Input Section */}
      <div className="relative group mb-12">
        <div className="absolute -inset-1 bg-gradient-to-r from-warm-blue via-warm-purple to-warm-pink dark:from-neon-blue dark:via-neon-purple dark:to-neon-pink rounded-xl blur opacity-15 dark:opacity-25 group-hover:opacity-40 dark:group-hover:opacity-75 transition duration-1000 group-hover:duration-200"></div>
        <div className="relative bg-beige-100 dark:bg-midnight-800 rounded-xl p-6 ring-1 ring-beige-300 dark:ring-white/10">
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Enter your basic idea
          </label>
          <div className="relative">
            <textarea
              className="w-full bg-white/60 dark:bg-midnight-900/50 text-gray-900 dark:text-white p-4 rounded-lg border border-beige-300 dark:border-gray-700 focus:border-warm-blue dark:focus:border-neon-blue focus:ring-1 focus:ring-warm-blue dark:focus:ring-neon-blue transition-all resize-none placeholder-gray-400 dark:placeholder-gray-500"
              rows="3"
              placeholder="e.g., A cyberpunk city in rain... (Press Enter to submit, Ctrl+Enter for new line)"
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter' && !e.ctrlKey && !e.shiftKey) {
                  e.preventDefault();
                  generatePrompt();
                }
              }}
              disabled={loading}
            />
            <button
              onClick={generatePrompt}
              disabled={loading || !prompt.trim()}
              className="absolute bottom-3 right-3 bg-amber-700 dark:bg-amber-800 hover:bg-amber-800 dark:hover:bg-amber-700 text-white p-3 rounded-lg font-medium disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-lg flex items-center justify-center"
              aria-label="Generate prompt"
            >
              {loading ? (
                <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                </svg>
              ) : (
                <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="2">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M13 7l5 5m0 0l-5 5m5-5H6" />
                </svg>
              )}
            </button>
          </div>
        </div>
      </div>

      {/* Error Message */}
      {error && (
        <div className="mt-6 bg-red-100 dark:bg-red-900/20 border border-red-300 dark:border-red-500/50 text-red-700 dark:text-red-200 px-4 py-3 rounded-lg backdrop-blur-sm">
          {error}
        </div>
      )}

      {/* Results Section */}
      {result && (
        <div className="animate-fade-in-up grid grid-cols-1 lg:grid-cols-12 gap-8">

          {/* Left Column: Original & Suggestions */}
          <div className="lg:col-span-4 space-y-6">
            {/* Original */}
            <div className="bg-beige-200/60 dark:bg-midnight-800/50 rounded-xl p-6 border border-beige-300 dark:border-white/5">
              <h3 className="text-gray-600 dark:text-gray-400 text-sm font-medium uppercase tracking-wider mb-4">Original</h3>
              <p className="text-gray-800 dark:text-gray-300 font-mono text-sm">{result.original_prompt}</p>
              <div className="mt-4 flex gap-2">
                <span className="px-2 py-1 rounded text-xs bg-beige-300 dark:bg-gray-700 text-gray-700 dark:text-gray-300">
                  Intent: {result.intent}
                </span>
              </div>
            </div>

            {/* Suggestions */}
            {result.suggestions && (
              <div className="bg-beige-200/60 dark:bg-midnight-800/50 rounded-xl p-6 border border-beige-300 dark:border-white/5">
                <h3 className="text-gray-600 dark:text-gray-400 text-sm font-medium uppercase tracking-wider mb-4">Suggestions</h3>
                <ul className="space-y-3">
                  {result.suggestions.map((suggestion, idx) => (
                    <li key={idx} className="flex items-start text-sm text-gray-700 dark:text-gray-400">
                      <span className="text-warm-blue dark:text-neon-blue mr-2 mt-1">•</span>
                      {suggestion}
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>

          {/* Right Column: Enhanced STOK Prompt */}
          <div className="lg:col-span-8">
            <div className="relative group h-full">
              <div className="absolute -inset-0.5 bg-gradient-to-r from-warm-purple to-warm-pink dark:from-neon-purple dark:to-neon-pink rounded-xl blur opacity-10 dark:opacity-20 group-hover:opacity-25 dark:group-hover:opacity-40 transition duration-500"></div>
              <div className="relative bg-beige-100 dark:bg-midnight-800 rounded-xl p-8 border border-beige-300 dark:border-white/10 h-full">
                <div className="flex justify-between items-center mb-8">
                  <h3 className="text-2xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-warm-purple to-warm-pink dark:from-neon-purple dark:to-neon-pink">
                    ✨ Enhanced Prompt
                  </h3>
                  <button
                    onClick={() => copyToClipboard(result.enhanced_prompt)}
                    className="flex items-center gap-2 px-4 py-2 rounded-lg bg-beige-200 dark:bg-white/5 hover:bg-beige-300 dark:hover:bg-white/10 text-gray-700 dark:text-gray-300 transition-all border border-beige-300 dark:border-white/5"
                  >
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                    </svg>
                    Copy Full Prompt
                  </button>
                </div>

                {/* STOK Framework Display */}
                <div className="space-y-6">
                  {/* Situation */}
                  <div className="bg-blue-50 dark:bg-white/5 rounded-lg p-4 border-l-4 border-blue-500">
                    <h4 className="text-blue-600 dark:text-blue-400 font-bold mb-2 uppercase text-xs tracking-wider">Situation</h4>
                    <p className="text-gray-800 dark:text-gray-200 leading-relaxed whitespace-pre-wrap">{result.structured_prompt.situation}</p>
                  </div>

                  {/* Task */}
                  <div className="bg-purple-50 dark:bg-white/5 rounded-lg p-4 border-l-4 border-purple-500">
                    <h4 className="text-purple-600 dark:text-purple-400 font-bold mb-2 uppercase text-xs tracking-wider">Task</h4>
                    <p className="text-gray-800 dark:text-gray-200 leading-relaxed whitespace-pre-wrap">{result.structured_prompt.task}</p>
                  </div>

                  {/* Objective */}
                  <div className="bg-pink-50 dark:bg-white/5 rounded-lg p-4 border-l-4 border-pink-500">
                    <h4 className="text-pink-600 dark:text-pink-400 font-bold mb-2 uppercase text-xs tracking-wider">Objective</h4>
                    <p className="text-gray-800 dark:text-gray-200 leading-relaxed whitespace-pre-wrap">{result.structured_prompt.objective}</p>
                  </div>

                  {/* Knowledge */}
                  <div className="bg-yellow-50 dark:bg-white/5 rounded-lg p-4 border-l-4 border-yellow-500">
                    <h4 className="text-yellow-600 dark:text-yellow-400 font-bold mb-2 uppercase text-xs tracking-wider">Knowledge</h4>
                    <p className="text-gray-800 dark:text-gray-200 leading-relaxed whitespace-pre-wrap">{result.structured_prompt.knowledge}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>

        </div>
      )}
    </div>
  );
}
