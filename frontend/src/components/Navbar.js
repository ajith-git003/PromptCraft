import React from "react";

export default function Navbar() {
  return (
    <nav className="bg-gray-900 text-white px-6 py-3 flex justify-between items-center">
      <h1 className="text-xl font-bold">PromptCraft</h1>
      <div className="space-x-4">
        <a href="/" className="hover:text-gray-300">Home</a>
        <a href="/about" className="hover:text-gray-300">About</a>
      </div>
    </nav>
  );
}
