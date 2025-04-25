# Insight Layer Framework: Contextual Memory Intelligence for Agents & Teams

[![DOI](https://zenodo.org/badge/969640251.svg)](https://doi.org/10.5281/zenodo.15262462)

This framework empowers AI agents and organizations to:
- **Remember** past insights and decisions
- **Reuse** context across time, tools, and roles
- **Refine** what matters with scoring and review
- **Route** insight to the right task, person, or workflow

---

##  Core Features

- **InsightUnit schema** – structured memory with metadata, narrative, reuse, fidelity, confidence, and references
- **LangGraph agent pipeline** – modular flow: retrieve → reason → summarize → store
- **Role-based onboarding bundles** – for team learning and ramp-up
- **Adaptive importance scoring** – based on usage, recency, impact, links, and outcome alignment
- **Grounding verification** – validates insight support via files, dashboards, or SQL (`watch_sources`)
- **Auto-linking** – builds contextual links between similar or related insights
- **Review pipeline** – uses GPT to classify sensitivity and confidence, applies thresholds from config
- **Prompt tracking** – logs success/failure and adds to insight metadata
- **Badges** – highlight key insights (`must_read`, `caution`, etc.)
- **User completion tracking** – for onboarding and learning progress
- **Bundle admin UI** – curate reusable insight packs
- **Vector memory with FAISS** – semantic memory retrieval
- **Embedding cache** – avoids redundant OpenAI API calls
- **Configurable prompt templates** – dynamically select prompts based on task metadata
- **Insight Wrappers (File, SQL, Notes)** – standardized functions that convert unstructured input into InsightUnits


---

##  Project Directory Structure

```
.
## Project Directory Structure

```
.
├── insight_layer_app/              # Streamlit multi-page UI
│   ├── Home.py                     # Landing screen
│   └── pages/
│   ├── 1_Run_Insight_Agent.py       # Run a LangGraph agent with memory injection and summarization
│   ├── 2_Bundle_Viewer.py           # View existing bundles of curated insights by topic or role
│   ├── 3_Bundle_Admin.py            # Create, edit, and manage InsightBundles (role- or topic-based)
│   ├── 4_Onboarding_Insights.py     # Role-specific onboarding experience with read tracking
│   ├── 5_Importance_Scoring.py      # Adjust weights and view ranked insights by importance
│   ├── 6_Insight_Graph.py           # Visualize relationships between insights (PyVis/Neo4j planned)
│   ├── 7_Grounding_Checks.py        # Check that insight references (files, URLs, SQL) are valid
│   ├── 8_Add_Insight_From_File.py   # Upload a file and generate a new insight from it
│   ├── 9_Add_Insight_From_SQL.py    # Paste a SQL query and generate a new insight
│   ├── 10_Add_Insight_From_Notes.py # Paste manual notes to convert into a structured InsightUnit
│   ├── 11_New_Insight_Sources.py    # Central UX hub for insight capture methods
├── src/
│   ├── graph/                      # Task parsing, prompt building, insight writing
│   ├── memory/                     # Vector memory, schema, logging
│   ├── utils/                      # Scoring, review tools, wrappers, insight pushers
│   │   ├── wrappers.py             # wrap_as_insight_unit_* helpers for file, SQL, notes
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
├── docs/                           # Architecture and schema references
├── scripts/                        # CLI agents, Neo4j exporter, refactor tools
├── .env.example                    # OpenAI key, toggles, and trace config
├── requirements.txt                # All required packages
├── README.md                       # You are here
└── streamlit_run_insight_agent.py  # CLI runner to invoke full agent graph
```

---

##  Installation

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
streamlit run insight_layer_app/Home.py
```

Ensure you configure your `.env` with your `OPENAI_API_KEY`.

---

## Getting Started

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/TheInsightLayer/insight-layer-starter.git
   cd insight-layer-starter
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

| Component                | Status         | Notes                                                                     |
| ------------------------ | -------------- | ------------------------------------------------------------------------- |
| Onboarding Viewer        | ✅ Implemented  | Users can view role-relevant insights and mark them as read.              |
| Bundle Admin UI          | ✅ Implemented  | Admins can create/edit insight bundles.                                   |
| Importance Scorer        | ✅ Implemented  | Users can adjust weights (used, links, outcome) and view sorted insights. |
| Grounding Check          | ✅ Implemented  | Verifies presence of watch\_sources (files, URLs, SQL).                   |
| Graph View               | 🟡 Placeholder | Static PyVis display works; Neo4j/dynamic edges planned.                  |
| Agent Runner             | ✅ Implemented  | Executes LangGraph agent with memory injection + summarizer.              |
| Add Insight from File    | ✅ Implemented  | Upload and summarize CSV/MD; wrapped in schema.                           |
| Add Insight from SQL     | ✅ Implemented  | Run a query and wrap output as InsightUnit.                               |
| Add Insight from Notes   | ✅ Implemented  | Free-text or pasted transcripts become structured insights.               |
| New Insight Sources Page | ✅ Implemented  | Central hub for manual insight creation (UX links to tools).              |


---

## Agent & Memory Logic

| Component                         | Status        | Notes                                                                 |
| --------------------------------- | ------------- | --------------------------------------------------------------------- |
| LangGraph Full Agent              | ✅ Implemented | Modular pipeline: retrieve → contextualize → run → summarize → store. |
| LangChain InsightRecommender Tool | ✅ Implemented | Can be used inside LangChain agents.                                  |
| LLM Task Parser Fallback          | ✅ Implemented | Regex fallback if LLM fails or is disabled.                           |
| LLM Summarizer Fallback           | ✅ Implemented | Uses basic summary logic if LLM fails.                                |
| Vector Search (FAISS)             | ✅ Implemented | Used for memory retrieval based on semantic similarity.               |
| Embedding Cache                   | ✅ Implemented | Prevents redundant OpenAI embedding API calls.                        |
| Vault Abstraction                 | 🟡 Stubbed    | `vault.py` exists but not yet integrated.                             |
                          |

---

## Insight Management

| Component                           | Status             | Notes                                                               |
| ----------------------------------- | ------------------ | ------------------------------------------------------------------- |
| InsightUnit Schema (v1.1)           | ✅ Implemented      | Includes narrative, fidelity, confidence, reuse, roles, references. |
| Insight Wrappers (File, SQL, Notes) | ✅ Implemented      | Standardized functions that wrap raw input into full schema.        |
| Memory Trace Logging                | ✅ Implemented      | Saves agent input/output/insight trace logs.                        |
| Trace Summary Folder                | ✅ Implemented      | Stores insight summaries separately from trace.                     |
| Auto-Bundling by Topic              | ✅ Implemented      | New insights grouped into reusable bundles.                         |
| Role-Based Filtering                | ✅ Implemented      | Filters insights by role in UI + memory.                            |
| Confidentiality Filters             | ✅ Implemented      | Toggle to only include `team_only` insights.                        |
| Auto-Linking Similar Insights       | 🟡 WIP Logic Added | Uses reference and topic similarity.                                |
                               |

---

## Evaluation & Review

| Component                       | Status        | Notes                                                   |
| ------------------------------- | ------------- | ------------------------------------------------------- |
| Importance Scoring              | ✅ Implemented | Based on usage, recency, links, outcome, impact.        |
| Auto-Review Classifier          | ✅ Implemented | Flags sensitivity, confidence, and sets review\_status. |
| Prompt Performance Tracking     | ✅ Implemented | Records success/failure outcomes per prompt.            |
| Prompt Templates YAML           | ✅ Implemented | Dynamically loads structured prompt designs.            |
| Config: Confidence Thresholds   | ✅ Implemented | YAML-based config for ingestion/review rules.           |
| Unit Tests: Parser + Summarizer | ✅ Implemented | Covers fallback logic and schema issues.                |
                            |

---

## Infrastructure & Dev Tools

| Component                        | Status         | Notes                                       |
| -------------------------------- | -------------- | ------------------------------------------- |
| .env Config + Toggle             | ✅ Implemented  | API key + config toggles.                   |
| README & Medium Post             | ✅ Complete     | Docs for use, install, and design.          |
| Neo4j Export                     | 🟡 Partial     | Script works but not auto-run or connected. |
| Visual Architecture Diagram      | 🟡 In Progress | PyVis graph placeholder; Neo4j planned.     |
| LangGraph Playground JSON Viewer | 🛠️ Planned    | Schema complete; no interactive viewer yet. |
| CI/CD or Dockerization           | 🛠️ Planned    | Needed for deployment or multi-user setup.  |

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

