import React, { useState } from "react";
import axios from "axios";

const API_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";

export default function PromptInput() {
  const [prompt, setPrompt] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const generatePrompt = async () => {
    if (!prompt.trim()) return;

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await axios.post(`${API_URL}/generate`, { prompt });
      setResult(response.data);
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
        <div className="absolute -inset-1 bg-gradient-to-r from-neon-blue via-neon-purple to-neon-pink rounded-xl blur opacity-25 group-hover:opacity-75 transition duration-1000 group-hover:duration-200"></div>
        <div className="relative bg-midnight-800 rounded-xl p-6 ring-1 ring-white/10">
          <label className="block text-sm font-medium text-gray-300 mb-2">
            Enter your basic idea
          </label>
          <div className="relative">
            <textarea
              className="w-full bg-midnight-900/50 text-white p-4 rounded-lg border border-gray-700 focus:border-neon-blue focus:ring-1 focus:ring-neon-blue transition-all resize-none placeholder-gray-500"
              rows="3"
              placeholder="e.g., A cyberpunk city in rain..."
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              disabled={loading}
            />
            <button
              onClick={generatePrompt}
              disabled={loading || !prompt.trim()}
              className="absolute bottom-3 right-3 bg-gradient-to-r from-neon-blue to-neon-purple hover:from-blue-500 hover:to-purple-500 text-white px-6 py-2 rounded-lg font-medium disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-lg shadow-blue-500/20 flex items-center gap-2"
            >
              {loading ? (
                <>
                  <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                  </svg>
                  Magic Working...
                </>
              ) : (
                <>
                  <span>✨</span> Magic Enhance
                </>
              )}
            </button>
          </div>
        </div>
      </div>

      {/* Error Message */}
      {error && (
        <div className="mt-6 bg-red-900/20 border border-red-500/50 text-red-200 px-4 py-3 rounded-lg backdrop-blur-sm">
          {error}
        </div>
      )}

      {/* Results Section */}
      {result && (
        <div className="animate-fade-in-up grid grid-cols-1 lg:grid-cols-12 gap-8">

          {/* Left Column: Original & Suggestions */}
          <div className="lg:col-span-4 space-y-6">
            {/* Original */}
            <div className="bg-midnight-800/50 rounded-xl p-6 border border-white/5">
              <h3 className="text-gray-400 text-sm font-medium uppercase tracking-wider mb-4">Original</h3>
              <p className="text-gray-300 font-mono text-sm">{result.original_prompt}</p>
              <div className="mt-4 flex gap-2">
                <span className="px-2 py-1 rounded text-xs bg-gray-700 text-gray-300">
                  Intent: {result.intent}
                </span>
              </div>
            </div>

            {/* Suggestions */}
            {result.suggestions && (
              <div className="bg-midnight-800/50 rounded-xl p-6 border border-white/5">
                <h3 className="text-gray-400 text-sm font-medium uppercase tracking-wider mb-4">Suggestions</h3>
                <ul className="space-y-3">
                  {result.suggestions.map((suggestion, idx) => (
                    <li key={idx} className="flex items-start text-sm text-gray-400">
                      <span className="text-neon-blue mr-2 mt-1">•</span>
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
              <div className="absolute -inset-0.5 bg-gradient-to-r from-neon-purple to-neon-pink rounded-xl blur opacity-20 group-hover:opacity-40 transition duration-500"></div>
              <div className="relative bg-midnight-800 rounded-xl p-8 border border-white/10 h-full">
                <div className="flex justify-between items-center mb-8">
                  <h3 className="text-2xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-neon-purple to-neon-pink">
                    ✨ Enhanced Prompt
                  </h3>
                  <button
                    onClick={() => copyToClipboard(result.enhanced_prompt)}
                    className="flex items-center gap-2 px-4 py-2 rounded-lg bg-white/5 hover:bg-white/10 text-gray-300 transition-all border border-white/5"
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
                  <div className="bg-white/5 rounded-lg p-4 border-l-4 border-blue-500">
                    <h4 className="text-blue-400 font-bold mb-2 uppercase text-xs tracking-wider">Situation</h4>
                    <p className="text-gray-200 leading-relaxed whitespace-pre-wrap">{result.structured_prompt.situation}</p>
                  </div>

                  {/* Task */}
                  <div className="bg-white/5 rounded-lg p-4 border-l-4 border-purple-500">
                    <h4 className="text-purple-400 font-bold mb-2 uppercase text-xs tracking-wider">Task</h4>
                    <p className="text-gray-200 leading-relaxed whitespace-pre-wrap">{result.structured_prompt.task}</p>
                  </div>

                  {/* Objective */}
                  <div className="bg-white/5 rounded-lg p-4 border-l-4 border-pink-500">
                    <h4 className="text-pink-400 font-bold mb-2 uppercase text-xs tracking-wider">Objective</h4>
                    <p className="text-gray-200 leading-relaxed whitespace-pre-wrap">{result.structured_prompt.objective}</p>
                  </div>

                  {/* Knowledge */}
                  <div className="bg-white/5 rounded-lg p-4 border-l-4 border-yellow-500">
                    <h4 className="text-yellow-400 font-bold mb-2 uppercase text-xs tracking-wider">Knowledge</h4>
                    <p className="text-gray-200 leading-relaxed whitespace-pre-wrap">{result.structured_prompt.knowledge}</p>
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
