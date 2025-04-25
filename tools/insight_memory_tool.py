from typing import List, Dict, Optional
from langchain.tools import Tool
from src.memory.insight_layer_memory import InsightLayerMemory
from src.memory.summarizer import summarize_and_normalize
from src.utils.normalize_fields import normalize_insight  # You can create this

class InsightMemoryTool:
    def __init__(self, vault_path: Optional[str] = None):
        self.memory = InsightLayerMemory(vault_path=vault_path) if vault_path else InsightLayerMemory()

    def load_context(self, task_meta: Dict) -> List[Dict]:
        return self.memory.load_context(task_meta)

    def save_output_as_insight(self, agent_output: str, task_meta: Dict, normalize: bool = True) -> Dict:
        """Converts agent output into an InsightUnit, optionally normalizes, then saves."""
        # Step 1: Convert raw output into insight dict
        insight = summarize_and_normalize(agent_output, task_meta)

        # Step 2: Normalize field names if requested
        if normalize:
            insight = normalize_insight(insight)

        # Step 3: Inject additional task_meta properties (e.g., audience, visibility)
        if "audience" in task_meta:
            insight.setdefault("audience_profiles", []).append(task_meta["audience"])
        if "confidentiality" in task_meta:
            insight["confidentiality"] = task_meta["confidentiality"]

        # Step 4: Save into memory
        self.memory.save_context(insight)
        return insight

    def as_langchain_tools(self):
        return [
            Tool.from_function(
                func=lambda meta: self.load_context(meta),
                name="load_context",
                description="Retrieve relevant insights for a task using task metadata"
            ),
            Tool.from_function(
                func=lambda x: self.save_output_as_insight(x['output'], x['meta']),
                name="save_output_as_insight",
                description="Convert agent output into a reusable insight and save it"
            )
        ]
