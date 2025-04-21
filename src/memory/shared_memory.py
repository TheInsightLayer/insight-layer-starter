
from .insight_layer_memory import InsightLayerMemory

class SharedMemoryVault:
    def __init__(self):
        self.vaults = {}

    def get_agent_memory(self, agent_id):
        if agent_id not in self.vaults:
            self.vaults[agent_id] = InsightLayerMemory(vault_path=f"data/memory_{agent_id}.db")
        return self.vaults[agent_id]
