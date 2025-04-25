from insight_layer.models import InsightUnit

def load_insightunit(filepath):
    with open(filepath) as f:
        raw = json.load(f)
    return InsightUnit(**raw["InsightUnit"])
