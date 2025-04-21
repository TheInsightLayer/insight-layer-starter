
from langchain.memory.chat_memory import BaseMemory
from typing import Dict, List, Any
from src.memory.insight_layer_vector_memory import InsightLayerVectorMemory

class InsightLangChainMemory(BaseMemory):
    def __init__(self):
        self.insight_memory = InsightLayerVectorMemory()

    @property
    def memory_variables(self) -> List[str]:
        return ["context"]

    def load_memory_variables(self, inputs: Dict[str, Any]) -> Dict[str, str]:
        task = inputs.get("input", "")
        task_meta = self._infer_meta(task)
        insights = self.insight_memory.load_context(task_meta)
        insight_text = "\n".join(
            [f"- {i['who']} did {i['what']} (Outcome: {i['outcome']})" for i in insights]
        )
        return {"context": insight_text}

    def save_context(self, inputs: Dict[str, Any], outputs: Dict[str, Any]) -> None:
        task = inputs.get("input", "")
        task_meta = self._infer_meta(task)
        summary = {
            "who": "Agent",
            "what": outputs.get("output", "Generated output"),
            "why": task_meta.get("purpose", "unspecified"),
            "when": task_meta.get("quarter", "now"),
            "outcome": "Pending",
            "source": outputs.get("output", "")
        }
        self.insight_memory.save_context(summary)

    def clear(self):
        pass  # Optional: implement if needed

    def _infer_meta(self, task: str) -> Dict:
        return {
            "purpose": "general",
            "topic": "retention" if "retention" in task.lower() else "general",
            "quarter": "Q3" if "Q3" in task else "unknown"
        }
