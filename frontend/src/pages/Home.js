import React from "react";
import PromptInput from "../components/PromptInput";

export default function Home() {
  return (
    <div className="min-h-screen bg-midnight-900 text-white overflow-hidden selection:bg-neon-blue selection:text-white">
      {/* Background Effects */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-0 left-1/4 w-96 h-96 bg-neon-blue/20 rounded-full blur-3xl animate-blob"></div>
        <div className="absolute top-1/4 right-1/4 w-96 h-96 bg-neon-purple/20 rounded-full blur-3xl animate-blob animation-delay-2000"></div>
        <div className="absolute -bottom-32 left-1/3 w-96 h-96 bg-neon-pink/20 rounded-full blur-3xl animate-blob animation-delay-4000"></div>
      </div>

      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        {/* Hero Section */}
        <div className="text-center mb-16 animate-float">
          <div className="inline-block mb-4 px-4 py-1.5 rounded-full border border-white/10 bg-white/5 backdrop-blur-sm">
            <span className="text-sm font-medium text-neon-blue">✨ AI-Powered Prompt Engineering</span>
          </div>
          <h1 className="text-6xl md:text-7xl font-bold mb-6 tracking-tight">
            <span className="bg-clip-text text-transparent bg-gradient-to-r from-white via-gray-200 to-gray-400">
              Prompt
            </span>
            <span className="bg-clip-text text-transparent bg-gradient-to-r from-neon-blue to-neon-purple">
              Cowboy
            </span>
          </h1>
          <p className="text-xl text-gray-400 max-w-2xl mx-auto mb-8 leading-relaxed">
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
              desc: "Optimized for LLMs like GPT-4, Claude 3, and Gemini."
            }
          ].map((feature, idx) => (
            <div key={idx} className="group p-8 rounded-2xl bg-white/5 border border-white/10 hover:bg-white/10 transition duration-300 backdrop-blur-sm">
              <div className="text-4xl mb-4 group-hover:scale-110 transition duration-300">{feature.icon}</div>
              <h3 className="text-xl font-bold mb-3 text-white">{feature.title}</h3>
              <p className="text-gray-400 leading-relaxed">
                {feature.desc}
              </p>
            </div>
          ))}
        </div>

        {/* Footer */}
        <div className="mt-20 text-center text-gray-600 text-sm">
          <p>Built for AI/ML Engineering Portfolio</p>
        </div>
      </div>
    </div>
  );
}
