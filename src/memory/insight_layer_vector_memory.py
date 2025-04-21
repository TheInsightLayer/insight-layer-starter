
from langchain_core.memory import BaseMemory
from langchain_core.runnables import RunnableConfig
from typing import Dict, List, Any
from src.memory.vector_store import VectorStore
from src.memory.insight_layer_memory import InsightLayerMemory


class InsightLayerVectorMemory(BaseMemory):
    def __init__(self, vault_path="data/memory.db"):
        self.memory = InsightLayerMemory(vault_path=vault_path)
        self.vault_path = vault_path

    def load_memory_variables(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        task_meta = {
            "purpose": inputs.get("purpose", "general"),
            "topic": inputs.get("topic", ""),
            "quarter": inputs.get("quarter", "")
        }
        insights = self.memory.load_context(task_meta)
        insight_text = "\n".join(
            [f"- {i['who']} did {i['what']} because {i['why']} (Outcome: {i['outcome']})" for i in insights]
        )
        return {"insights": insight_text}

    def save_context(self, inputs: Dict[str, Any], outputs: Dict[str, Any], config: RunnableConfig = None) -> None:
        summary = {
            "who": "Insight Agent",
            "what": inputs.get("task", "Unknown task"),
            "when": inputs.get("timestamp", "unknown"),
            "why": inputs.get("purpose", "unknown"),
            "how": "Generated with LangChain Insight LayerMemory",
            "outcome": outputs.get("result", "Pending"),
            "source": outputs.get("result", "")
        }
        self.memory.save_context(summary)

    def clear(self) -> None:
        # Not implemented; optional
        pass
