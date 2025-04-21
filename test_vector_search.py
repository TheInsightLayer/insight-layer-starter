
from src.memory.insight_layer_memory import InsightLayerMemory

if __name__ == "__main__":
    memory = InsightLayerMemory()

    task = {
        "purpose": "campaign planning",
        "quarter": "Q3",
        "topic": "customer retention"
    }

    print("🔍 Searching for insights related to:")
    print(task)

    results = memory.load_context(task)
    print(f"✅ Retrieved {len(results)} relevant insights:")
    for r in results:
        print("-", r["what"], "→", r.get("outcome", "N/A"))
