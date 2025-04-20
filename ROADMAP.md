# Insight Layer Roadmap

A maturity model for evolving your Insight Layer from a lightweight prototype into an org-wide intelligence infrastructure.

---

## Starter – Just Getting Started  
**Focus:** Minimal setup to show value quickly

**Features:**
- Ingest plain text (`.txt`) or Markdown documents  
- Extract insights via LLM (or fallback logic)  
- Store to JSON + SQLite  
- Basic Streamlit UI with keyword/tag filters  

*Purpose:* Demonstrates the core concept. Great for individual contributors, knowledge owners, or pilot teams.

---

## Pro – Operational Use  
**Focus:** Usability, flexibility, and team-wide adoption

**Suggested Enhancements:**
- Inline tag editing in the UI  
- Manual insight entry form  
- Re-run LLM on selected insights  
- Tag dropdowns with auto-complete  
- CSV export of filtered results  
- Author/source tracking for insights  
- Use SQLite or Postgres with a full schema  

*Purpose:* Empowers small teams to refine, reuse, and scale valuable knowledge across domains.

---

## Scalable Org – Insight as Infrastructure  
**Focus:** Integration, automation, and collaboration across tools and teams

**Advanced Capabilities:**
- API access for retrieval (MS Copilot, Notion, etc.)  
- Semantic search (vector DB + FAISS embeddings)  
- Power Automate, Zapier, or n8n pipelines  
- InsightUnit schema (e.g., decision, context, impact)  
- Permissions and roles  
- Insight timeline visualization  
- Shared tagging, notifications, and approvals  
- Metrics on reuse and impact  

*Purpose:* Treat insights as a **long-term memory layer**, enabling repeatable decisions, onboarding, and innovation at scale.

---

## Context Engine – Adaptive + Task-Aware  
**Focus:** Delivering the right insight at the right moment

**Future-State Capabilities:**
- Function: `get_relevant_insights_for(task_description)`  
- Context-aware prompts (e.g., “I’m writing a strategy doc…”)  
- Automatic insight matching based on user task or system state  
- Proactive surfacing inside productivity tools (Slack, Docs, VS Code)  
- Real-time context listener or lightweight agent  
- Embedded memory for ongoing conversations or workflows  
- Feedback loop to improve relevance over time  

*Purpose:* Moves beyond storage and search — toward **adaptive memory** that supports the flow of work, not just the documentation of it.