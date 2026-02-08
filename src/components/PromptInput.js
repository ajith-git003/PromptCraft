import React from "react";

export default function PromptInput({
  prompt,
  setPrompt,
  onGenerate,
  result,
  loading,
  error,
}) {
  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
  };

  return (
    <div className="w-full max-w-7xl mx-auto">
      {/* Input Section */}
      <div className="relative group mb-12">
        <div className="absolute -inset-1 bg-gradient-to-r from-warm-blue via-warm-purple to-warm-pink dark:from-neon-blue dark:via-neon-purple dark:to-neon-pink rounded-xl blur opacity-15 dark:opacity-25 group-hover:opacity-40 dark:group-hover:opacity-75 transition duration-1000 group-hover:duration-200"></div>
        <div className="relative bg-beige-100 dark:bg-midnight-800 rounded-xl p-4 md:p-6 ring-1 ring-beige-300 dark:ring-white/10">
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Enter your basic idea
          </label>
          <div className="relative">
            <textarea
              className="w-full bg-white/60 dark:bg-midnight-900/50 text-gray-900 dark:text-white p-3 md:p-4 rounded-lg border border-beige-300 dark:border-gray-700 focus:border-warm-blue dark:focus:border-neon-blue focus:ring-1 focus:ring-warm-blue dark:focus:ring-neon-blue transition-all resize-none placeholder-gray-400 dark:placeholder-gray-500"
              rows="3"
              placeholder="e.g., A cyberpunk city in rain... (Press Enter to submit, Ctrl+Enter for new line)"
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter" && !e.ctrlKey && !e.shiftKey) {
                  e.preventDefault();
                  onGenerate();
                }
              }}
              disabled={loading}
            />
            <button
              onClick={onGenerate}
              disabled={loading || !prompt.trim()}
              className="absolute bottom-3 right-3 bg-amber-700 dark:bg-amber-800 hover:bg-amber-800 dark:hover:bg-amber-700 text-white p-3 rounded-lg font-medium disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-lg flex items-center justify-center"
              aria-label="Generate prompt"
            >
              {loading ? (
                <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                  <circle
                    className="opacity-25"
                    cx="12"
                    cy="12"
                    r="10"
                    stroke="currentColor"
                    strokeWidth="4"
                    fill="none"
                  />
                  <path
                    className="opacity-75"
                    fill="currentColor"
                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                  />
                </svg>
              ) : (
                <svg
                  className="h-5 w-5"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                  strokeWidth="2"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    d="M13 7l5 5m0 0l-5 5m5-5H6"
                  />
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
            <div className="bg-beige-200/60 dark:bg-midnight-800/50 rounded-xl p-4 md:p-6 border border-beige-300 dark:border-white/5">
              <h3 className="text-gray-600 dark:text-gray-400 text-sm font-medium uppercase tracking-wider mb-4">
                Original
              </h3>
              <p className="text-gray-800 dark:text-gray-300 font-mono text-sm">
                {result.original_prompt}
              </p>
              <div className="mt-4 flex gap-2">
                <span className="px-2 py-1 rounded text-xs bg-beige-300 dark:bg-gray-700 text-gray-700 dark:text-gray-300">
                  Intent: {result.intent}
                </span>
              </div>
            </div>

            {/* Suggestions */}
            {result.suggestions && (
              <div className="bg-beige-200/60 dark:bg-midnight-800/50 rounded-xl p-4 md:p-6 border border-beige-300 dark:border-white/5">
                <h3 className="text-gray-600 dark:text-gray-400 text-sm font-medium uppercase tracking-wider mb-4">
                  Suggestions
                </h3>
                <ul className="space-y-3">
                  {result.suggestions.map((suggestion, idx) => (
                    <li
                      key={idx}
                      className="flex items-start text-sm text-gray-700 dark:text-gray-400"
                    >
                      <span className="text-warm-blue dark:text-neon-blue mr-2 mt-1">
                        •
                      </span>
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
              <div className="relative bg-beige-100 dark:bg-midnight-800 rounded-xl p-6 md:p-8 border border-beige-300 dark:border-white/10 h-full">
                <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-6 md:mb-8 gap-4 md:gap-0">
                  <h3 className="text-xl md:text-2xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-warm-purple to-warm-pink dark:from-neon-purple dark:to-neon-pink">
                    ✨ Enhanced Prompt
                  </h3>
                  <button
                    onClick={() => copyToClipboard(result.enhanced_prompt)}
                    className="flex items-center gap-2 px-4 py-2 rounded-lg bg-beige-200 dark:bg-white/5 hover:bg-beige-300 dark:hover:bg-white/10 text-gray-700 dark:text-gray-300 transition-all border border-beige-300 dark:border-white/5 self-end md:self-auto"
                  >
                    <svg
                      className="w-4 h-4"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth="2"
                        d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"
                      />
                    </svg>
                    Copy Full Prompt
                  </button>
                </div>

                {/* STOK Framework Display */}
                <div className="space-y-6">
                  {/* Situation */}
                  <div className="bg-blue-50 dark:bg-white/5 rounded-lg p-4 border-l-4 border-blue-500">
                    <h4 className="text-blue-600 dark:text-blue-400 font-bold mb-2 uppercase text-xs tracking-wider">
                      Situation
                    </h4>
                    <p className="text-gray-800 dark:text-gray-200 leading-relaxed whitespace-pre-wrap">
                      {result.structured_prompt.situation}
                    </p>
                  </div>

                  {/* Task */}
                  <div className="bg-purple-50 dark:bg-white/5 rounded-lg p-4 border-l-4 border-purple-500">
                    <h4 className="text-purple-600 dark:text-purple-400 font-bold mb-2 uppercase text-xs tracking-wider">
                      Task
                    </h4>
                    <p className="text-gray-800 dark:text-gray-200 leading-relaxed whitespace-pre-wrap">
                      {result.structured_prompt.task}
                    </p>
                  </div>

                  {/* Objective */}
                  <div className="bg-pink-50 dark:bg-white/5 rounded-lg p-4 border-l-4 border-pink-500">
                    <h4 className="text-pink-600 dark:text-pink-400 font-bold mb-2 uppercase text-xs tracking-wider">
                      Objective
                    </h4>
                    <p className="text-gray-800 dark:text-gray-200 leading-relaxed whitespace-pre-wrap">
                      {result.structured_prompt.objective}
                    </p>
                  </div>

                  {/* Knowledge */}
                  <div className="bg-yellow-50 dark:bg-white/5 rounded-lg p-4 border-l-4 border-yellow-500">
                    <h4 className="text-yellow-600 dark:text-yellow-400 font-bold mb-2 uppercase text-xs tracking-wider">
                      Knowledge
                    </h4>
                    <p className="text-gray-800 dark:text-gray-200 leading-relaxed whitespace-pre-wrap">
                      {result.structured_prompt.knowledge}
                    </p>
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
