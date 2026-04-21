# 🤖 Natural Language CLI Tool

A command-line AI agent that takes natural language questions and intelligently decides whether to **search the web**, **calculate**, or **answer directly** using a local LLM via Ollama.

Built entirely with local AI — no cloud API keys required for the core functionality. Privacy-friendly, free to run, and fully customizable.

---

## ✨ Features

- 🧠 **Smart Routing** — An LLM decides the best tool for each question
- 🔢 **Math Calculator** — Evaluates arithmetic and unit conversions safely
- 🔍 **Web Search** — Pulls current information from DuckDuckGo
- 💬 **Direct Answers** — Uses local LLM knowledge for general questions
- 📝 **History Logging** — Every interaction is saved to `history.json`
- 🏠 **100% Local** — Runs entirely on your machine via Ollama
- 📦 **Structured Output** — Returns JSON-style responses with reasoning

---

## 🏗️ Architecture

```
┌──────────────────────┐
│  User Question       │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│  Router (LLM)        │   Decides: calculate / search / answer
│  router.py           │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│  Tool Execution      │   Runs the chosen tool
│  tools.py            │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│  Structured Response │   Returns formatted answer + metadata
│  main.py             │
└──────────────────────┘
```

This is a classic **inference pipeline** pattern used in AI agents.

---

## 📋 Requirements

- **Python 3.9+**
- **[Ollama](https://ollama.com)** installed and running locally
- At least one Ollama model pulled (recommended: `qwen2.5:7b`)

---

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/nl-cli-tool.git
cd nl-cli-tool
```

### 2. Create a Virtual Environment

```bash
# Create venv
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Activate (Mac/Linux)
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Pull an Ollama Model

```bash
ollama pull qwen2.5:7b
```

Other good options: `llama3.1:8b`, `mistral`, `llama3.2`

### 5. Configure Environment Variables

Create a `.env` file in the project root:

```env
OLLAMA_MODEL=qwen2.5:7b
SERPER_API_KEY=your-serper-key-here
```

> **Note:** `SERPER_API_KEY` is optional. The tool uses DuckDuckGo by default. If you want to use Serper for better search quality, sign up at [serper.dev](https://serper.dev) for a free key.

---

## 💻 Usage

Make sure Ollama is running in the background, then:

```bash
python main.py
```

You'll see:

```
============================================================
  Natural Language CLI Tool (Powered by Ollama)
  Model: qwen2.5:7b
  Type 'quit' to exit
============================================================

Ask:
```

### Example Questions

```
Ask: What's 1234 * 567?
# → Uses the calculator tool

Ask: Who won the most recent Super Bowl?
# → Uses the search tool

Ask: Explain recursion in simple terms
# → Uses the direct answer tool

Ask: Convert 100 miles to kilometers
# → Uses the calculator tool
```

### Example Output

```
------------------------------------------------------------
Tool chosen  : calculate
Reasoning    : arithmetic problem
Query passed : 1234 * 567
------------------------------------------------------------
Answer:
Result: 699678
------------------------------------------------------------
```

---

## 📁 Project Structure

```
nl-cli-tool/
├── .venv/                # Virtual environment (not in git)
├── .env                  # Environment variables (not in git)
├── .gitignore            # Git ignore rules
├── requirements.txt      # Python dependencies
├── main.py               # CLI entry point & pipeline
├── router.py             # LLM-based tool router
├── tools.py              # Calculator, search, and answer tools
├── history.json          # Interaction log (auto-generated)
└── README.md             # This file
```

---

## 🧩 How It Works

### 1. Routing Phase (`router.py`)

The user's question is sent to the local LLM with a system prompt that instructs it to classify the question and respond in JSON:

```json
{
  "tool": "calculate",
  "reasoning": "arithmetic problem",
  "query": "1234 * 567"
}
```

Ollama's `format="json"` mode guarantees valid JSON output.

### 2. Execution Phase (`tools.py`)

Based on the router's decision, the appropriate tool is executed:

- **`calculate(expression)`** — Safely evaluates math using filtered `eval()`
- **`search_web(query)`** — Searches DuckDuckGo and summarizes results via LLM
- **`direct_answer(query)`** — Asks the LLM directly using its internal knowledge

### 3. Response Phase (`main.py`)

The tool's output is wrapped in a structured dictionary containing:

- The original question
- The tool that was used
- The LLM's reasoning
- The processed query
- The final answer
- A timestamp

This response is printed to the console and appended to `history.json`.

---

## 🔧 Configuration

### Switching Models

Edit `.env` and change the `OLLAMA_MODEL` value:

```env
OLLAMA_MODEL=llama3.1:8b
```

Models that work well for routing tasks:

| Model | Size | Routing Quality | Speed |
|-------|------|-----------------|-------|
| `qwen2.5:7b` | 4.7GB | Excellent ⭐ | Fast |
| `llama3.1:8b` | 4.9GB | Very Good | Fast |
| `mistral` | 4.4GB | Good | Fast |
| `qwen3.5:9b` | 6.6GB | Excellent | Slower |
| `llama3.2` | 2.0GB | Okay | Very Fast |

### Changing the Search Provider

By default, the tool uses DuckDuckGo (no API key required). To switch to Serper:

1. Get a free API key from [serper.dev](https://serper.dev)
2. Add it to `.env` as `SERPER_API_KEY=...`
3. Modify `search_web()` in `tools.py` to use the Serper API

---

## 📦 Dependencies

| Package | Purpose |
|---------|---------|
| `ollama` | Talk to local Ollama models |
| `python-dotenv` | Load environment variables from `.env` |
| `ddgs` | Search DuckDuckGo without an API key |
| `requests` | HTTP requests (for Serper or other APIs) |

Install with:

```bash
pip install -r requirements.txt
```

---

## 🛠️ Troubleshooting

### "ModuleNotFoundError"
Your virtual environment isn't active. Run `.venv\Scripts\activate` (Windows) or `source .venv/bin/activate` (Mac/Linux).

### "Connection refused" to Ollama
Ollama isn't running. Start it manually with `ollama serve` or check if it's running in your system tray.

### "No search results found"
DuckDuckGo may be rate-limiting. Wait a few minutes or switch to Serper.

### Router makes weird decisions
Try a larger model like `qwen2.5:7b` or `llama3.1:8b`. Smaller models (< 2GB) struggle with structured JSON output.

### Slow responses
Your model is too large for your hardware. Try a smaller model like `llama3.2` (2GB).

---

## 🗺️ Roadmap

Ideas for future improvements:

- [ ] Add conversation memory for multi-turn questions
- [ ] Add a weather tool using Open-Meteo API
- [ ] Add streaming output (word-by-word responses)
- [ ] Build a web UI with Gradio or Streamlit
- [ ] Add retry logic for failed API calls
- [ ] Support multiple languages
- [ ] Add unit tests
- [ ] Cache repeated questions

---

## 📚 What I Learned

This project taught me:

- How AI agents use **LLMs as routers** to decide which tool to invoke
- How to use **structured JSON output** from local LLMs
- **Defensive programming** when working with AI outputs
- The **inference pipeline** pattern used in production AI systems
- How to integrate **local models** with external tools
- **Environment management** with `venv` and `.env` files

---

## 🤝 Contributing

This is a learning project, but suggestions and improvements are welcome! Feel free to open issues or pull requests.

---

## 📄 License

MIT License — feel free to use this code for learning or as a starting point for your own projects.

---

## 🙏 Acknowledgments

- **[Ollama](https://ollama.com)** for making local LLMs easy to run
- **[Qwen Team](https://qwenlm.github.io/)** for the excellent qwen2.5 models
- **[DuckDuckGo](https://duckduckgo.com)** for free, privacy-respecting search

---

Made with ☕ and curiosity while learning AI from scratch.
