import React from "react";
import PromptInput from "../components/PromptInput";

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        {/* Hero Section */}
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold text-gray-900 mb-4">
            ✨ PromptCraft
          </h1>
          <p className="text-xl text-gray-600 mb-2">
            Analyze and optimize your AI prompts instantly
          </p>
          <p className="text-sm text-gray-500">
            Powered by advanced NLP · Get instant feedback on prompt quality
          </p>
        </div>

        {/* Main Component */}
        <PromptInput />

        {/* Features Section */}
        <div className="mt-16 grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="bg-white rounded-lg shadow p-6 text-center">
            <div className="text-4xl mb-4">🎯</div>
            <h3 className="font-bold text-lg mb-2">Precision Analysis</h3>
            <p className="text-gray-600 text-sm">
              Get detailed scores on clarity, specificity, structure, and
              completeness
            </p>
          </div>
          <div className="bg-white rounded-lg shadow p-6 text-center">
            <div className="text-4xl mb-4">💡</div>
            <h3 className="font-bold text-lg mb-2">Smart Suggestions</h3>
            <p className="text-gray-600 text-sm">
              Receive actionable recommendations to improve your prompts
            </p>
          </div>
          <div className="bg-white rounded-lg shadow p-6 text-center">
            <div className="text-4xl mb-4">⚡</div>
            <h3 className="font-bold text-lg mb-2">Instant Results</h3>
            <p className="text-gray-600 text-sm">
              Real-time analysis powered by spaCy NLP engine
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
