# Insight Layer Roadmap

A maturity model for evolving your Insight Layer from prototype to org-wide intelligence infrastructure.

---

## Starter – Just Getting Started
**Focus:** Minimal setup to show value quickly.

Features:
- Ingest markdown or PDFs  
- Extract insights via LLM (or fallback logic)  
- Store to JSON + SQLite  
- Basic Streamlit UI with keyword/tag filters

*Purpose:* Demonstrates core concept. Great for individual contributors or pilot teams.

---

## Pro – Operational Use
**Focus:** Usability, flexibility, and team-wide adoption.

Suggested Enhancements:
- Inline tag editing in the UI  
- Manual insight entry form  
- Re-run LLM on selected insights  
- Tag dropdowns with auto-complete  
- CSV export of filtered results  
- Author/source tracking for insights  
- Use SQLite or Postgres with a full schema

*Purpose:* Gives power users tools to refine, reuse, and scale value across small teams.

---

## Scalable Org – Insight as Infrastructure
**Focus:** Integration, automation, and collaboration across tools and teams.

Advanced Capabilities:
- API access for retrieval (MS Copilot, Notion, etc.)  
- Semantic search (vector DB + embedding)  
- Power Automate or Zapier pipelines  
- InsightUnit schema (decision, context, impact)  
- Permissions and roles  
- Insight timeline visualization  
- Shared tagging, notifications, and approvals  
- Metrics on reuse and impact

*Purpose:* Treat insights as a long-term memory layer, powering decisions across orgs.