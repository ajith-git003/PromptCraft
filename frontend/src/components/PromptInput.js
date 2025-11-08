import React, { useState } from "react";
import axios from "axios";

const API_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";

export default function PromptInput() {
  const [prompt, setPrompt] = useState("");
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const analyzePrompt = async () => {
    if (!prompt.trim()) {
      setError("Please enter a prompt to analyze");
      return;
    }

    setLoading(true);
    setError(null);
    setAnalysis(null);

    try {
      const response = await axios.post(`${API_URL}/analyze`, { prompt });
      setAnalysis(response.data);
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          "Failed to analyze prompt. Make sure the backend is running."
      );
    } finally {
      setLoading(false);
    }
  };

  const getScoreColor = (score) => {
    if (score >= 80) return "text-green-600";
    if (score >= 60) return "text-yellow-600";
    return "text-red-600";
  };

  const getSeverityBadge = (severity) => {
    const colors = {
      high: "bg-red-100 text-red-800",
      medium: "bg-yellow-100 text-yellow-800",
      low: "bg-blue-100 text-blue-800",
    };
    return colors[severity] || "bg-gray-100 text-gray-800";
  };

  return (
    <div className="max-w-4xl mx-auto">
      {/* Input Section */}
      <div className="bg-white rounded-lg shadow-md p-6 mb-6">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Enter your AI prompt
        </label>
        <textarea
          className="w-full p-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition"
          rows="6"
          placeholder="Example: Write a story about a robot learning emotions..."
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          disabled={loading}
        />
        <div className="flex items-center justify-between mt-4">
          <span className="text-sm text-gray-500">
            {prompt.length} characters
          </span>
          <button
            onClick={analyzePrompt}
            disabled={loading || !prompt.trim()}
            className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg font-medium disabled:opacity-50 disabled:cursor-not-allowed transition"
          >
            {loading ? (
              <span className="flex items-center">
                <svg
                  className="animate-spin -ml-1 mr-2 h-4 w-4 text-white"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                >
                  <circle
                    className="opacity-25"
                    cx="12"
                    cy="12"
                    r="10"
                    stroke="currentColor"
                    strokeWidth="4"
                  ></circle>
                  <path
                    className="opacity-75"
                    fill="currentColor"
                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                  ></path>
                </svg>
                Analyzing...
              </span>
            ) : (
              "Analyze Prompt"
            )}
          </button>
        </div>
      </div>

      {/* Error Message */}
      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-6">
          <div className="flex items-center">
            <svg
              className="w-5 h-5 mr-2"
              fill="currentColor"
              viewBox="0 0 20 20"
            >
              <path
                fillRule="evenodd"
                d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                clipRule="evenodd"
              />
            </svg>
            {error}
          </div>
        </div>
      )}

      {/* Results Section */}
      {analysis && (
        <div className="space-y-6">
          {/* Overall Score */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-xl font-bold mb-4">Overall Score</h3>
            <div className="flex items-center justify-center">
              <div
                className={`text-6xl font-bold ${ getScoreColor(
                  analysis.analysis.overall_score
                )}`}
              >
                {analysis.analysis.overall_score}
                <span className="text-3xl text-gray-400">/100</span>
              </div>
            </div>
          </div>

          {/* Score Breakdown */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-xl font-bold mb-4">Score Breakdown</h3>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              {[
                { label: "Clarity", score: analysis.analysis.clarity_score },
                {
                  label: "Specificity",
                  score: analysis.analysis.specificity_score,
                },
                { label: "Structure", score: analysis.analysis.structure_score },
                {
                  label: "Completeness",
                  score: analysis.analysis.completeness_score,
                },
              ].map((item) => (
                <div key={item.label} className="text-center">
                  <div className={`text-2xl font-bold ${getScoreColor(item.score)}`}>
                    {item.score}
                  </div>
                  <div className="text-sm text-gray-600">{item.label}</div>
                </div>
              ))}
            </div>
          </div>

          {/* Issues */}
          {analysis.analysis.issues.length > 0 && (
            <div className="bg-white rounded-lg shadow-md p-6">
              <h3 className="text-xl font-bold mb-4">Issues Found</h3>
              <div className="space-y-3">
                {analysis.analysis.issues.map((issue, index) => (
                  <div
                    key={index}
                    className="border-l-4 border-yellow-400 bg-yellow-50 p-4 rounded"
                  >
                    <div className="flex items-center justify-between mb-2">
                      <span className="font-medium">{issue.type}</span>
                      <span
                        className={`px-2 py-1 text-xs rounded-full ${getSeverityBadge(
                          issue.severity
                        )}`}
                      >
                        {issue.severity}
                      </span>
                    </div>
                    <p className="text-sm text-gray-700">{issue.message}</p>
                    <p className="text-xs text-gray-500 mt-1">{issue.details}</p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Suggestions */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-xl font-bold mb-4">💡 Suggestions</h3>
            <ul className="space-y-2">
              {analysis.analysis.suggestions.map((suggestion, index) => (
                <li key={index} className="flex items-start">
                  <svg
                    className="w-5 h-5 text-green-500 mr-2 mt-0.5 flex-shrink-0"
                    fill="currentColor"
                    viewBox="0 0 20 20"
                  >
                    <path
                      fillRule="evenodd"
                      d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                      clipRule="evenodd"
                    />
                  </svg>
                  <span className="text-gray-700">{suggestion}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* Metrics */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-xl font-bold mb-4">📊 Metrics</h3>
            <div className="grid grid-cols-3 gap-4 text-center">
              <div>
                <div className="text-3xl font-bold text-blue-600">
                  {analysis.analysis.metrics.word_count}
                </div>
                <div className="text-sm text-gray-600">Words</div>
              </div>
              <div>
                <div className="text-3xl font-bold text-blue-600">
                  {analysis.analysis.metrics.sentence_count}
                </div>
                <div className="text-sm text-gray-600">Sentences</div>
              </div>
              <div>
                <div className="text-3xl font-bold text-blue-600">
                  {analysis.analysis.metrics.unique_words}
                </div>
                <div className="text-sm text-gray-600">Unique Words</div>
              </div>
            </div>
          </div>

          {/* Optimized Prompt */}
          <div className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg shadow-md p-6">
            <h3 className="text-xl font-bold mb-4">✨ Optimized Version</h3>
            <p className="text-gray-800 leading-relaxed">
              {analysis.optimized_prompt}
            </p>
          </div>
        </div>
      )}
    </div>
  );
}
