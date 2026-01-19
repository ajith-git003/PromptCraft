# 🎓 PromptCraft - Interview Guide & Technical Documentation

## 🚀 Project Overview
**PromptCraft** is an AI-powered prompt engineering tool that transforms simple, one-line ideas into professional, systematic prompts for LLMs (like GPT-4, Claude, Gemini) and Image Generators (Midjourney, DALL-E).

**Tech Stack:**
-   **Frontend**: React.js, Tailwind CSS (Glassmorphism/Neon design)
-   **Backend**: FastAPI (Python), spaCy (NLP)
-   **Deployment**: Docker, Vercel/Railway (Ready)

---

## 🧠 Code Logic & Algorithms (How it works)

### 1. Intent Recognition (Backend)
**File**: `backend/app/prompt_engine.py`

We use **Set Theory** and **NLP** to understand what the user wants.

```python
# Logic: Set Intersection
# We convert the user's prompt into a set of tokens (words) and check for overlap with keyword sets.
tokens = {token.lemma_ for token in doc}

if tokens & coding_keywords:  # Intersection check
    return "coding"
```

*   **Why Set Intersection?**: It's O(1) (constant time) on average, making it extremely fast compared to iterating through lists O(n).
*   **NLP (spaCy)**: We use `token.lemma_` to get the base form of words (e.g., "running" -> "run"), making the matching more robust.

### 2. Systematic Generation (Backend)
**File**: `backend/app/prompt_engine.py`

We use a **Rule-Based Expert System** approach.

```python
# Logic: Conditional Control Flow (If-Elif-Else)
if intent == "coding":
    enhanced = generate_coding_prompt(prompt)
elif intent == "image":
    enhanced = generate_image_prompt(prompt)
# ...
```

*   **Why Rule-Based?**: For an MVP, it's deterministic, free (no API costs), and fast. It mimics how an expert would structure a prompt.
*   **Scalability**: This structure is the *precursor* to an Agentic workflow. You can easily replace `generate_coding_prompt` with an LLM call later.

### 3. Asynchronous Frontend (React)
**File**: `frontend/src/components/PromptInput.js`

We use **Async/Await** for non-blocking API calls.

```javascript
const generatePrompt = async () => {
  setLoading(true); // Update UI state
  try {
    // Await the Promise (doesn't freeze the browser)
    const response = await axios.post(...);
    setResult(response.data);
  } catch (err) {
    setError(...);
  } finally {
    setLoading(false); // Always run this
  }
};
```

---

## 🎤 Interview Q&A Preparation

### Q1: "Tell me about the architecture of this project."
**Answer**: "It follows a decoupled **Client-Server architecture**. The frontend is a React SPA (Single Page Application) that communicates via REST API with a FastAPI backend. I chose FastAPI because of its high performance (Starlette) and automatic validation with Pydantic. The application is containerized using Docker for consistent deployment."

### Q2: "How did you handle the prompt generation? Did you use an LLM?"
**Answer**: "For this version, I implemented a **deterministic NLP engine** using spaCy. I analyze the semantic intent of the user's input (classifying it as Coding, Writing, or Image generation) using lemma matching. Then, I apply expert-designed templates to structure the prompt. This ensures high-quality structure without the latency or cost of an LLM call for every request. However, the system is designed to be 'LLM-ready'—I can swap the template functions for API calls to OpenAI or Gemini easily."

### Q3: "Why did you use Tailwind CSS?"
**Answer**: "I wanted a highly custom, premium 'Dark Mode' aesthetic. Tailwind's utility-first approach allowed me to rapidly prototype complex designs like glassmorphism (background blur) and gradients without fighting against a component library's defaults. It also ensures the CSS bundle size is minimal in production."

### Q4: "How would you scale this?"
**Answer**:
1.  **Caching**: Implement Redis to cache results for common prompts.
2.  **Rate Limiting**: Use `fastapi-limiter` to prevent abuse.
3.  **LLM Integration**: Connect to a vector database (RAG) to retrieve successful prompt examples to use as few-shot context for generation."

### Q5: "What was the most challenging part?"
**Answer**: "Designing the intent recognition logic to be accurate without a heavy ML model. I had to carefully curate the keyword sets and use lemmatization to handle different word variations effectively."

---

## 🛠️ Key Programming Concepts Used
1.  **Sets & Hash Maps**: For O(1) keyword lookups.
2.  **Control Flow**: `if/elif/else` for intent routing.
3.  **String Manipulation**: f-strings for template injection.
4.  **HTTP Protocols**: POST requests, JSON payloads, CORS headers.
5.  **State Management**: React `useState` hooks for UI reactivity.
