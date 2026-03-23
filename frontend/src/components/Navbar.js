import React from "react";

export default function Navbar({ onToggleSidebar }) {
  return (
    <nav className="bg-beige-200 dark:bg-gray-900 text-gray-900 dark:text-white px-4 py-3 transition-colors duration-300 flex items-center gap-3">
      <button
        className="md:hidden p-2 rounded-lg hover:bg-beige-300 dark:hover:bg-gray-700 transition-colors"
        onClick={onToggleSidebar}
        aria-label="Toggle sidebar"
      >
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 12h16M4 18h16" />
        </svg>
      </button>
      <h1 className="text-xl font-bold">PromptCraft</h1>
    </nav>
  );
}
