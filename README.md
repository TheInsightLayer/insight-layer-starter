# Insight Layer Framework: Contextual Memory Intelligence for Agents & Teams

This framework empowers AI agents and organizations to:
- **Remember** past insights and decisions
- **Reuse** context across time, tools, and roles
- **Refine** what matters with scoring and review
- **Route** insight to the right task, person, or workflow

---

##  Core Features

-  **InsightUnit schema** – structured memory with metadata, links, badges, and usage tracking
-  **Role-based onboarding bundles** for learning journeys
-  **Adaptive importance scoring** – factors in use, impact, links, and recency
-  **Grounding verification** – check supporting files, dashboards, SQL
-  **Review pipeline** – sensitivity, confidence, and approval scoring
-  **Badges** – highlight critical or cautionary insights
-  **User completion tracking** – for onboarding progress
-  **Bundle admin UI** – curate reusable insight packs

---

##  Project Directory Structure

```
.
├── insight_layer_app/              # Streamlit multi-page UI
│   ├── Home.py                     # Landing screen
│   └── pages/
│       ├── 1_Run_Insight_Agent.py
│       ├── 2_Bundle_Viewer.py
│       ├── 3_Bundle_Admin.py
│       ├── 4_Onboarding_Insights.py
│       ├── 5_Importance_Scoring.py
│       ├── 6_Insight_Graph.py
│       └── 7_Grounding_Checks.py
├── src/
│   ├── graph/                      # Task parsing, prompt building, insight writing
│   ├── memory/                     # Vector memory, schema, logging
│   ├── utils/                      # Scoring, review tools, insight pushers
├── agents/                         # LangGraph agent pipelines
├── tools/                          # LangChain-compatible insight tools
├── configs/                        # Agent input, thresholds, graph layout
├── data/
│   ├── insights/                   # Individual InsightUnits (JSON)
│   ├── bundles/                    # Role-specific and topic-specific groupings
│   ├── trace_logs/                 # Run history and memory trace summaries
│   ├── embeddings/                 # (Optional) local embedding cache
│   ├── memory.db                   # SQLite metadata DB
│   ├── sample_report.csv           # File-based reference (for grounding)
│   └── user_completion.json        # Tracks onboarding completion
├── notebooks/                      # Workflow demos and graph visualizations
├── docs/                           # Architecture and flow diagrams
├── scripts/                        # CLI agents, Neo4j exporter, refactor tools
├── .env.example                    # OpenAI key, toggles, and trace config
├── requirements.txt                # All required packages
├── README.md                       # You are here
└── streamlit_run_insight_agent.py  # CLI runner to invoke full agent graph
```

---

##  Installation

```bash
pip install -r requirements.txt
streamlit run insight_layer_app/Home.py
```

Ensure you configure your `.env` with your `OPENAI_API_KEY`.

---

## Getting Started

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-repo/cmi-langgraph-prototype.git
   cd cmi-langgraph-prototype
   ```

---

##  Workflow Overview

1. A user enters a task or query
2. Relevant insights are retrieved from vector memory
3. A prompt is constructed dynamically (LLM optional)
4. The agent executes and returns structured output
5. A new insight is summarized, scored, reviewed, and stored
6. Trace logs and bundles are optionally updated

---

##  Feature Progress


## Streamlit Interfaces

| Component         | Status         | Notes                                                                 |
|------------------|----------------|-----------------------------------------------------------------------|
| Onboarding Viewer | ✅ Implemented | Users can view role-relevant insights and mark them as read.         |
| Bundle Admin UI   | ✅ Implemented | Admins can create/edit insight bundles.                              |
| Importance Scorer | ✅ Implemented | Users can adjust weights (used, links, outcome) and view sorted insights. |
| Grounding Check   | ✅ Implemented | Verifies presence of watch_sources (files, URLs, SQL).               |
| Graph View        | 🟡 Placeholder | Static PyVis display works; Neo4j/dynamic edges planned.             |
| Agent Runner      | ✅ Implemented | Executes LangGraph agent with memory injection + summarizer.         |

---

## Agent & Memory Logic

| Component                        | Status         | Notes                                                                 |
|----------------------------------|----------------|-----------------------------------------------------------------------|
| LangGraph Full Agent             | ✅ Implemented | Modular pipeline: task → memory → summary → bundle.                  |
| LangChain InsightRecommender Tool| ✅ Implemented | Can be used inside LangChain agents.                                 |
| LLM Task Parser Fallback         | ✅ Implemented | Regex fallback if LLM fails or is disabled.                          |
| LLM Summarizer Fallback          | ✅ Implemented | Uses basic summary logic if LLM fails.                               |
| Vector Search (FAISS)            | ✅ Implemented | Used for memory retrieval based on semantic similarity.              |
| Embedding Cache                  | ✅ Implemented | Prevents redundant OpenAI embedding API calls.                       |
| Vault Abstraction                | 🟡 Stubbed     | `vault.py` exists but not yet integrated.                            |

---

## Insight Management

| Component                   | Status         | Notes                                                                 |
|----------------------------|----------------|-----------------------------------------------------------------------|
| Insight Schema (v4)        | ✅ Implemented | Includes roles, badges, confidence, watch_sources, references.       |
| Memory Trace Logging       | ✅ Implemented | Saves agent input/output/insight trace logs.                         |
| Trace Summary Folder       | ✅ Implemented | Stores insight summaries separately from trace.                      |
| Auto-Bundling by Topic     | ✅ Implemented | New insights grouped into reusable bundles.                          |
| Role-Based Filtering       | ✅ Implemented | Filters insights by role in UI + memory.                             |
| Confidentiality Filters    | ✅ Implemented | Toggle to only include `team_only` insights.                         |
| Auto-Linking Similar Insights | 🟡 WIP Logic Added | Uses reference and topic similarity.                                 |

---

## Evaluation & Review

| Component                    | Status         | Notes                                                                 |
|-----------------------------|----------------|-----------------------------------------------------------------------|
| Importance Scoring          | ✅ Implemented | Based on usage, recency, links, outcome, impact.                     |
| Auto-Review Classifier      | ✅ Implemented | Flags sensitivity, confidence, and sets review_status.               |
| Prompt Performance Tracking | ✅ Implemented | Records success/failure outcomes per prompt.                         |
| Prompt Templates YAML       | ✅ Implemented | Dynamically loads structured prompt designs.                         |
| Config: Confidence Thresholds | ✅ Implemented | YAML-based config for ingestion/review rules.                        |
| Unit Tests: Parser + Summarizer | ✅ Implemented | Covers fallback logic and schema issues.                             |

---

## Infrastructure & Dev Tools

| Component                    | Status         | Notes                                                                 |
|-----------------------------|----------------|-----------------------------------------------------------------------|
| .env Config + Toggle        | ✅ Implemented | API key + config toggles.                                            |
| README & Medium Post        | ✅ Complete    | Docs for use, install, and design.                                   |
| Neo4j Export                | 🟡 Partial     | Script works but not auto-run or connected.                          |
| Visual Architecture Diagram | 🟡 In Progress | PyVis graph placeholder; Neo4j planned.                              |
| LangGraph Playground JSON Viewer | 🛠️ Planned | Schema complete; no interactive viewer yet.                          |
| CI/CD or Dockerization      | 🛠️ Planned    | Needed for deployment or multi-user setup.                           |

---

##  Requirements

```
openai
faiss-cpu
langchain
streamlit
pydantic
pyvis
neo4j
tqdm
python-dotenv
sentence-transformers
pytest
pyyaml
torch
pytest-mock
neo4j-driver
```
---