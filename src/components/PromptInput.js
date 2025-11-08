import React, { useState } from "react";

export default function PromptInput() {
  const [prompt, setPrompt] = useState("");

  return (
    <div>
      <textarea
        style={{ width: "100%", padding: "12px", borderRadius: "6px", border: "1px solid #ccc", marginBottom: "12px" }}
        rows="5"
        placeholder="Enter your prompt here..."
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
      />
      <button style={{ backgroundColor: "#2563eb", color: "white", padding: "8px 16px", borderRadius: "6px", border: "none" }}>
        Analyze Prompt
      </button>
    </div>
  );
}
