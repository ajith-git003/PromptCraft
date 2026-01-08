import React from "react";
import PromptInput from "../components/PromptInput";
import { useTheme } from "../context/ThemeContext";

export default function Home() {
  const { theme, toggleTheme } = useTheme();
  
  return (
    <div className="min-h-screen bg-beige-50 dark:bg-midnight-900 text-gray-900 dark:text-white overflow-hidden selection:bg-warm-blue selection:text-white dark:selection:bg-neon-blue transition-colors duration-300 flex">
      {/* Left Sidebar - History */}
      <aside className="w-64 bg-beige-100 dark:bg-midnight-800 border-r border-beige-300 dark:border-white/10 flex-shrink-0 overflow-hidden flex flex-col">
        <div className="p-4">
          <button className="w-full px-4 py-3 bg-beige-50 dark:bg-midnight-900 hover:bg-white dark:hover:bg-midnight-700 rounded-lg border border-beige-300 dark:border-white/10 text-left font-medium text-gray-900 dark:text-white transition-all flex items-center gap-2">
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 4v16m8-8H4" />
            </svg>
            New Prompt
          </button>
        </div>
        
        <div className="px-4 pb-2">
          <h3 className="text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider flex items-center gap-2">
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" />
            </svg>
            Library
          </h3>
        </div>

        <div className="flex-1 overflow-y-auto px-2">
          {/* History items will be rendered by PromptInput component */}
          <div id="history-sidebar-content"></div>
        </div>

      </aside>

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Background Effects */}
        <div className="fixed inset-0 overflow-hidden pointer-events-none">
          <div className="absolute top-0 left-1/4 w-96 h-96 bg-warm-blue/10 dark:bg-neon-blue/20 rounded-full blur-3xl animate-blob"></div>
          <div className="absolute top-1/4 right-1/4 w-96 h-96 bg-warm-purple/10 dark:bg-neon-purple/20 rounded-full blur-3xl animate-blob animation-delay-2000"></div>
          <div className="absolute -bottom-32 left-1/3 w-96 h-96 bg-warm-pink/10 dark:bg-neon-pink/20 rounded-full blur-3xl animate-blob animation-delay-4000"></div>
        </div>

        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20 overflow-y-auto flex-1 w-full">
        {/* Theme Toggle Button */}
        <div className="absolute top-8 right-8">
          <button
            onClick={toggleTheme}
            className="p-3 rounded-full bg-gray-800/10 dark:bg-white/10 hover:bg-gray-800/20 dark:hover:bg-white/20 border border-gray-800/20 dark:border-white/10 backdrop-blur-sm transition-all duration-300 group"
            aria-label="Toggle theme"
          >
            {theme === 'dark' ? (
              <svg className="w-5 h-5 text-yellow-300" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 2a1 1 0 011 1v1a1 1 0 11-2 0V3a1 1 0 011-1zm4 8a4 4 0 11-8 0 4 4 0 018 0zm-.464 4.95l.707.707a1 1 0 001.414-1.414l-.707-.707a1 1 0 00-1.414 1.414zm2.12-10.607a1 1 0 010 1.414l-.706.707a1 1 0 11-1.414-1.414l.707-.707a1 1 0 011.414 0zM17 11a1 1 0 100-2h-1a1 1 0 100 2h1zm-7 4a1 1 0 011 1v1a1 1 0 11-2 0v-1a1 1 0 011-1zM5.05 6.464A1 1 0 106.465 5.05l-.708-.707a1 1 0 00-1.414 1.414l.707.707zm1.414 8.486l-.707.707a1 1 0 01-1.414-1.414l.707-.707a1 1 0 011.414 1.414zM4 11a1 1 0 100-2H3a1 1 0 000 2h1z" clipRule="evenodd" />
              </svg>
            ) : (
              <svg className="w-5 h-5 text-gray-700" fill="currentColor" viewBox="0 0 20 20">
                <path d="M17.293 13.293A8 8 0 016.707 2.707a8.001 8.001 0 1010.586 10.586z" />
              </svg>
            )}
          </button>
        </div>

        {/* Hero Section */}
        <div className="text-center mb-16 animate-float">
          <div className="inline-block mb-4 px-4 py-1.5 rounded-full border border-gray-800/20 dark:border-white/10 bg-gray-800/5 dark:bg-white/5 backdrop-blur-sm">
            <span className="text-sm font-medium text-amber-700 dark:text-amber-500">✨ AI-Powered Prompt Engineering</span>
          </div>
          <h1 className="text-6xl md:text-7xl font-bold mb-6 tracking-tight">
            <span className="bg-clip-text text-transparent bg-gradient-to-r from-gray-900 via-gray-700 to-gray-600 dark:from-white dark:via-gray-200 dark:to-gray-400">
              AI Prompt
            </span>
            <span className="bg-clip-text text-transparent bg-gradient-to-r from-amber-600 to-amber-800 dark:from-amber-500 dark:to-amber-700">
              Studio
            </span>
          </h1>
          <p className="text-xl text-gray-600 dark:text-gray-400 max-w-2xl mx-auto mb-8 leading-relaxed">
            Transform simple ideas into professional, high-performance prompts for Coding, Art, and Writing.
          </p>
        </div>

        {/* Main Component */}
        <PromptInput />

        {/* Features Section */}
        <div className="mt-32 grid grid-cols-1 md:grid-cols-3 gap-8">
          {[
            {
              icon: "🚀",
              title: "Instant Expansion",
              desc: "Turn one-liners into comprehensive, structured prompts instantly."
            },
            {
              icon: "🎨",
              title: "Multi-Modal Support",
              desc: "Specialized templates for Code, Image Generation (Midjourney/DALL-E), and Creative Writing."
            },
            {
              icon: "⚡",
              title: "Production Ready",
              desc: "Optimized for LLMs like GPT, Claude, and Gemini."
            }
          ].map((feature, idx) => (
            <div key={idx} className="group p-8 rounded-2xl bg-beige-200/50 dark:bg-white/5 border border-beige-300 dark:border-white/10 hover:bg-beige-200/70 dark:hover:bg-white/10 transition duration-300 backdrop-blur-sm">
              <div className="text-4xl mb-4 group-hover:scale-110 transition duration-300">{feature.icon}</div>
              <h3 className="text-xl font-bold mb-3 text-gray-900 dark:text-white">{feature.title}</h3>
              <p className="text-gray-600 dark:text-gray-400 leading-relaxed">
                {feature.desc}
              </p>
            </div>
          ))}
        </div>

        </div>
      </div>
    </div>
  );
}
