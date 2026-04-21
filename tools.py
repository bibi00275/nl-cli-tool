import os
import requests
import ollama
from dotenv import load_dotenv
from ddgs import DDGS

load_dotenv()
MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")


def calculate(expression: str) -> str:
    """Safely evaluate a math expression."""
    try:
        allowed = set("0123456789+-*/(). ")
        if not all(c in allowed for c in expression):
            return "Error: Expression contains invalid characters. Only numbers and + - * / ( ) are allowed."
        result = eval(expression)
        return f"Result: {result}"
    except ZeroDivisionError:
        return "Error: Division by zero."
    except Exception as e:
        return f"Calculation error: {str(e)}"





def search_web(query: str) -> str:
    """Search using DuckDuckGo (no API key needed)."""
    try:
        results = []
        with DDGS() as ddgs:
            # Try text search with explicit parameters
            search_results = ddgs.text(
                query,
                max_results=5,
                region="wt-wt",      # worldwide
                safesearch="moderate"
            )
            results = list(search_results)

        if not results:
            return f"No search results found for '{query}'. DuckDuckGo may be rate-limiting. Try again in a minute or rephrase your query."

        # Build snippets from results
        snippets = []
        for r in results:
            title = r.get("title", "")
            body = r.get("body", "")
            href = r.get("href", "")
            snippets.append(f"- {title}\n  {body}\n  Source: {href}")

        combined = "\n\n".join(snippets)

        # Ask Ollama to summarize
        summary = ollama.chat(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful assistant. Use the search results below to answer the user's question clearly. Mention sources when relevant. If the results don't contain enough info, say so."},
                {"role": "user", "content": f"Question: {query}\n\nSearch Results:\n{combined}\n\nProvide a clear, factual answer based on these results."}
            ]
        )
        return summary["message"]["content"]

    except Exception as e:
        return f"Search error: {str(e)}"

def direct_answer(query: str) -> str:
    """Answer directly using Ollama's built-in knowledge."""
    response = ollama.chat(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful assistant. Answer the user's question clearly and concisely."},
            {"role": "user", "content": query}
        ]
    )
    return response["message"]["content"]