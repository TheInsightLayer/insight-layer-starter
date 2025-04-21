import os
from typing import List

def check_watch_sources(insight: dict, update: bool = False) -> List[str]:
    """
    Checks and summarizes the grounding sources referenced in an insight.

    Parameters:
        insight (dict): The structured insight containing a list of `watch_sources`.
        update (bool): If True, adds grounding status and result messages to the insight.

    Returns:
        List[str]: Human-readable status messages for each source (file, URL, SQL, etc.)
    """

    status = []         # Store messages about what was found/missing
    valid_sources = 0   # Counter for sources that are valid (found or assumed okay)

    # Iterate over all watch sources in the insight
    for ws in insight.get("watch_sources", []):
        
        # File-based grounding check (e.g., CSV, PDF, etc.)
        if ws["type"] == "file" and ws.get("path"):
            exists = os.path.exists(ws["path"])
            if exists:
                status.append(f"File found: {ws['path']}")
                valid_sources += 1
            else:
                status.append(f"Missing file: {ws['path']}")

        # URL-based source (not live-checked here, just acknowledged)
        elif ws["type"] == "url" and ws.get("url"):
            status.append(f"URL: {ws['url']}")
            valid_sources += 1  # Counted as valid (could later verify via HTTP)

        # SQL query reference (not executed — just displayed)
        elif ws["type"] == "sql" and ws.get("query"):
            status.append(f"SQL query: `{ws['query']}` (not executed)")
            valid_sources += 1

        # Any other or malformed source
        else:
            status.append("Unknown or incomplete watch source")

    # Optionally update the insight in-place with grounding results
    if update:
        insight["grounding_status"] = "verified" if valid_sources else "unverified"
        insight["grounding_checks"] = status

    return status
