import os
import json
import ollama
from dotenv import load_dotenv

load_dotenv()
MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")


def route_question(question: str) -> dict:
    """
    Ask the local Ollama model to decide: search, calculate, or answer directly.
    Returns a dictionary with the decision.
    """

    system_prompt = """You are a routing assistant. Your job is to classify user questions 
and respond ONLY with valid JSON — no other text, no explanations outside the JSON.

Available tools:
1. "calculate" - for math problems (arithmetic, equations, conversions, percentages)
2. "search" - for current events, recent news, live data, or facts that change over time
3. "answer" - for general knowledge, definitions, explanations, how-to, coding help

You MUST respond in this EXACT JSON format and nothing else:
{"tool": "calculate" | "search" | "answer", "reasoning": "brief explanation", "query": "cleaned query"}

Examples:
User: "What's 145 * 23?"
{"tool": "calculate", "reasoning": "arithmetic problem", "query": "145 * 23"}

User: "Who is the current CEO of Google?"
{"tool": "search", "reasoning": "needs current info that changes", "query": "current CEO of Google"}

User: "What is photosynthesis?"
{"tool": "answer", "reasoning": "general knowledge question", "query": "explain photosynthesis"}

User: "Convert 50 miles to kilometers"
{"tool": "calculate", "reasoning": "unit conversion is math", "query": "50 * 1.60934"}

Remember: output ONLY the JSON object, nothing else."""

    response = ollama.chat(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}
        ],
        format="json",  # Forces Ollama to return valid JSON
        options={"temperature": 0}  # Makes output consistent
    )

    content = response["message"]["content"]

    try:
        decision = json.loads(content)
        # Validate required keys exist
        if "tool" not in decision:
            decision["tool"] = "answer"
        if "reasoning" not in decision:
            decision["reasoning"] = "default routing"
        if "query" not in decision:
            decision["query"] = question
        return decision
    except json.JSONDecodeError:
        # Fallback if model misbehaves
        return {
            "tool": "answer",
            "reasoning": "router failed to return JSON, defaulting to direct answer",
            "query": question
        }