import json
import os
from datetime import datetime
from router import route_question
from tools import calculate, search_web, direct_answer


def process_question(question: str) -> dict:
    """Pipeline: route → execute → return structured response."""

    decision = route_question(question)
    tool = decision["tool"]
    query = decision["query"]

    if tool == "calculate":
        result = calculate(query)
    elif tool == "search":
        result = search_web(query)
    elif tool == "answer":
        result = direct_answer(query)
    else:
        result = "Unknown tool selected by router."

    return {
        "timestamp": datetime.now().isoformat(),
        "question": question,
        "tool_used": tool,
        "reasoning": decision["reasoning"],
        "processed_query": query,
        "answer": result
    }


def save_to_history(response: dict):
    """Append every interaction to history.json for review."""
    history_file = "history.json"
    history = []

    if os.path.exists(history_file):
        try:
            with open(history_file, "r") as f:
                history = json.load(f)
        except json.JSONDecodeError:
            history = []

    history.append(response)

    with open(history_file, "w") as f:
        json.dump(history, f, indent=2)


def main():
    print("\n" + "=" * 60)
    print("  Natural Language CLI Tool (Powered by Ollama)")
    print(f"  Model: {os.getenv('OLLAMA_MODEL', 'llama3.2')}")
    print("  Type 'quit' to exit")
    print("=" * 60 + "\n")

    while True:
        try:
            question = input("Ask: ").strip()

            if question.lower() in ["quit", "exit", "q"]:
                print("Goodbye!")
                break

            if not question:
                continue

            print("\nThinking...\n")
            response = process_question(question)
            save_to_history(response)

            print("-" * 60)
            print(f"Tool chosen  : {response['tool_used']}")
            print(f"Reasoning    : {response['reasoning']}")
            print(f"Query passed : {response['processed_query']}")
            print("-" * 60)
            print(f"Answer:\n{response['answer']}")
            print("-" * 60 + "\n")

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}\n")


if __name__ == "__main__":
    main()