
from typing import List, Dict, Optional
from langchain.tools import Tool
from src.memory.insight_layer_memory import InsightLayerMemory
from src.graph.summarizer import summarize_output

class InsightMemoryTool:
    def __init__(self, vault_path: Optional[str] = None):
        self.memory = InsightLayerMemory(vault_path=vault_path) if vault_path else InsightLayerMemory()

    def load_context(self, task_meta: Dict) -> List[Dict]:
        """Returns relevant past insights based on task metadata."""
        return self.memory.load_context(task_meta)

    def save_output_as_insight(self, agent_output: str, task_meta: Dict) -> Dict:
        """Converts agent output into an InsightUnit and saves it."""
        insight = summarize_output(agent_output, task_meta)
        self.memory.save_context(insight)
        return insight

    def as_langchain_tools(self):
        """Returns Tool objects for LangGraph/CrewAI integration."""
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
