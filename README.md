
# ContextFind

> **Search conversations by meaning, not wording.**

ContextFind is a semantic search engine for messy group conversations. It answers questions such as:

- "When did we decide on the trip?"
- "What did Priya say about the budget?"
- "What did we discuss last month?"

Unlike traditional keyword search, ContextFind uses multilingual semantic embeddings to retrieve messages based on **meaning**, even when the query and matching message have little or no word overlap.

---

## 🚀 Why ContextFind?

Normal keyword search struggles with conversational data.

**Query**
```text
When did we decide on the trip?
```

**Actual message**
```text
Rahul: Manali it is. Friday evening departure, tickets final.
```

The answer is clearly relevant even though it may share zero important words with the query.

ContextFind solves this using:

1. **Semantic search** — understands meaning.
2. **Query understanding** — detects intent, person, and time.
3. **Hybrid ranking** — combines embeddings with structured signals.
4. **Context reconstruction** — shows surrounding messages.
5. **Evaluation** — measures normal and hard zero-word-overlap queries.

---

# ✨ Features

### 🔎 Semantic Search
Uses sentence embeddings to find messages with similar meaning instead of relying only on exact keywords.

Supports English, Hinglish, and code-mixed conversation text.

### 🧠 Query Understanding
The query parser identifies:

- Intent
- Participant/sender
- Time range
- Decision-related intent

Example:

```text
"What did Priya say about the budget last month?"
```

can be interpreted as:

```text
Person: Priya
Time range: last month
Intent: information
```

### 🏆 Hybrid Ranking
Candidates are ranked using:

```text
Semantic similarity
        +
Person match
        +
Temporal match
        +
Decision signals
        +
Context signals
```

### 📌 Decision Detection
Decision queries give additional weight to messages containing language such as:

```text
final
confirmed
fixed
locked
done
decided
settled
pakka
book
booking
```

### 🧵 Context Reconstruction
The system does not return an isolated message. It displays nearby conversation:

```text
Message -2
Message -1
🎯 Matched message
Message +1
Message +2
```

### 📊 Evaluation
The project includes:

- 4,000+ synthetic messages
- 40 labelled queries
- At least 8 hard zero-word-overlap queries
- Overall accuracy
- Hard-query accuracy

---

# 🏗️ Architecture

```text
                         ┌─────────────────────┐
                         │      React UI       │
                         │  Search Interface   │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │     FastAPI API     │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │    Query Parser     │
                         │                     │
                         │ Intent              │
                         │ Person              │
                         │ Time Range          │
                         │ Decision Intent     │
                         └──────────┬──────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    ▼                               ▼
          ┌──────────────────┐             ┌──────────────────┐
          │ Sentence         │             │ Metadata /       │
          │ Transformer      │             │ Heuristic Signals│
          │ Embeddings       │             │                  │
          └────────┬─────────┘             └────────┬─────────┘
                   │                                │
                   ▼                                │
          ┌──────────────────┐                       │
          │      FAISS       │                       │
          │ Vector Retrieval │                       │
          └────────┬─────────┘                       │
                   │                                │
                   └───────────────┬────────────────┘
                                   ▼
                         ┌─────────────────────┐
                         │  Hybrid Reranker    │
                         │                     │
                         │ Semantic            │
                         │ Person              │
                         │ Temporal            │
                         │ Decision            │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │ Context             │
                         │ Reconstruction      │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │ Ranked Search       │
                         │ Results             │
                         └─────────────────────┘
```

---

# 🔄 How the Search Works

### 1. User enters a query

```text
When did we decide on the trip?
```

### 2. Query analysis

```text
Intent        → Decision
Person        → None
Time range    → None
Decision      → Yes
```

### 3. Generate embedding

The query is converted into a vector using:

```text
sentence-transformers/
paraphrase-multilingual-MiniLM-L12-v2
```

### 4. FAISS retrieval

FAISS searches the vector index and retrieves the most semantically similar candidate messages.

### 5. Hybrid reranking

A starting scoring model is:

```text
Final Score =
    0.60 × Semantic Similarity
  + 0.15 × Person Match
  + 0.10 × Temporal Match
  + 0.10 × Decision Score
  + 0.05 × Context Signal
```

The weights can be tuned using the evaluation dataset.

### 6. Context reconstruction

The matched message is displayed with nearby messages:

```text
Priya: Manali sounds better.
Aman: Friday evening works for me.
Rahul: Manali it is. Friday evening departure, tickets final.  ← Match
Priya: Done 👍
```

### 7. Return ranked results

The API returns:

- Matched message
- Sender
- Timestamp
- Score
- Score breakdown
- Match reasons
- Surrounding context
- Query analysis

---

# 🧪 Example

**Query**
```text
When did we decide on the trip?
```

**Result**
```text
🎯 Rahul — 2026-04-18 19:42

"Manali it is. Friday evening departure, tickets final."
```

**Why it matched**
```text
✓ High semantic similarity
✓ Decision language detected
```

The important point is that the correct message can be retrieved even when it does not literally contain the query's important words.

---

# 📁 Project Structure

```text
ContextFind/
│
├── backend/
│   ├── data/
│   │   ├── messages.json
│   │   └── queries.json
│   │
│   ├── index/
│   │   ├── messages.faiss
│   │   └── id_map.json
│   │
│   ├── generator.py
│   ├── indexer.py
│   ├── query_parser.py
│   ├── search.py
│   ├── main.py
│   └── test_backend.py
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── ...
│
├── README.md
└── ...
```

---

# 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React |
| Build Tool | Vite |
| Backend | Python |
| API | FastAPI |
| Embeddings | Sentence Transformers |
| Vector Search | FAISS |
| Dataset | Synthetic JSON |
| Testing | pytest |
| Version Control | Git + GitHub |

### Why this stack?

- **React + Vite** — fast, simple search interface.
- **FastAPI** — lightweight Python API with strong ML/NLP compatibility.
- **Sentence Transformers** — semantic embeddings.
- **FAISS** — fast local vector similarity search.
- **JSON** — simple and portable synthetic corpus.

---

# 📦 Dataset

ContextFind uses a completely **synthetic group-chat dataset**.

The corpus is designed to contain realistic messaging behaviour:

- 4,000+ messages
- 8 participants
- 6 months of conversation
- English
- Hinglish
- Code-mixed messages
- Typos
- One-word replies
- Short reactions
- Forwarded-style messages
- Media-placeholder messages
- Long conversation threads
- Concrete decisions

No real private chat data is included.

---

# ⚙️ Getting Started

## Prerequisites

Install:

- Python 3.10+
- Node.js 18+
- npm
- Git

## 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd ContextFind
```

## 2. Create Python environment

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

macOS/Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

## 3. Install backend dependencies

```bash
pip install -r backend/requirements.txt
```

If a requirements file is not present:

```bash
pip install fastapi uvicorn sentence-transformers faiss-cpu numpy pytest
```

## 4. Generate the dataset

```bash
python backend/generator.py
```

## 5. Build the FAISS index

```bash
python backend/indexer.py
```

This creates:

```text
backend/index/messages.faiss
backend/index/id_map.json
```

## 6. Start the backend

```bash
uvicorn backend.main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

API docs:

```text
http://127.0.0.1:8000/docs
```

## 7. Start the frontend

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

Open the URL displayed by Vite, usually:

```text
http://localhost:5173
```

---

# 🔌 API

Example search request:

```http
GET /search?q=When%20did%20we%20decide%20on%20the%20trip?&mode=hybrid
```

Example response:

```json
{
  "query": "When did we decide on the trip?",
  "mode": "hybrid",
  "query_analysis": {
    "intent": "decision",
    "person": null,
    "time_range": null
  },
  "results": [
    {
      "rank": 1,
      "message_id": "msg_1234",
      "sender": "Rahul",
      "text": "Manali it is. Friday evening departure, tickets final.",
      "score": 0.91,
      "score_breakdown": {
        "semantic": 0.94,
        "person": 0,
        "temporal": 0,
        "decision": 1,
        "context": 0
      },
      "reasons": [
        "High semantic similarity",
        "Decision language detected"
      ]
    }
  ]
}
```

---

# 🧪 Testing

Run:

```bash
pytest backend/test_backend.py
```

For detailed output:

```bash
pytest backend/test_backend.py -s
```

The evaluation should report:

```text
Overall Accuracy
        +
Hard Zero-Word-Overlap Accuracy
```

The hard queries are especially important because they test whether the system understands meaning rather than relying on word overlap.

---

# 📈 Evaluation Strategy

ContextFind can compare three approaches.

### Keyword baseline

```text
Query
 ↓
Token overlap
 ↓
Rank messages
```

### Semantic search

```text
Query
 ↓
Embedding
 ↓
FAISS
 ↓
Rank messages
```

### Hybrid search

```text
Query
 ↓
Query analysis
 ↓
Embedding
 ↓
FAISS candidate retrieval
 ↓
Metadata + intent signals
 ↓
Hybrid reranking
 ↓
Context reconstruction
```

This makes it possible to demonstrate where semantic retrieval helps and why structured signals are still necessary.

---

# 🎯 Key Design Decision

Semantic similarity should not be the only ranking signal.

For example:

```text
"What did Priya say about the budget?"
```

A purely semantic system could retrieve a highly relevant budget message written by Rahul.

Because the query explicitly asks about Priya, sender information should influence ranking.

Similarly:

```text
"What did we discuss last month?"
```

requires temporal reasoning.

Therefore ContextFind combines:

```text
Semantic relevance
        +
Structured constraints
        +
Intent-specific signals
```

---

# 🧩 Supported Query Types

### Decision queries

```text
When did we decide on the trip?
Which hotel did we finally choose?
What was the final decision about the venue?
```

### Person queries

```text
What did Priya say about the budget?
What did Rahul suggest for the trip?
Who mentioned the new deadline?
```

### Time queries

```text
What did we discuss last month?
What happened around March?
What did we talk about during the first week?
```

---

# 🚧 Current Limitations

This is an MVP and intentionally keeps the architecture simple.

Current limitations:

- Synthetic dataset instead of real-world chat exports
- Rule-based query parsing
- Fixed ranking weights
- Basic temporal parsing
- Limited thread modelling
- Local FAISS index
- No authentication
- No persistent user-specific chat storage
- Basic context reconstruction
- No learning-to-rank model

---

# 🔮 Future Improvements

### 1. Better Query Understanding

Add a stronger NLP/LLM-based query understanding layer:

```json
{
  "intent": "decision",
  "person": "Priya",
  "topic": "budget",
  "time_range": null
}
```

### 2. Better Thread Reconstruction

Reconstruct the actual conversation thread rather than simply taking nearby messages.

```text
Question
 ↓
Replies
 ↓
Discussion
 ↓
Decision
```

### 3. Learning-to-Rank

Replace manually selected weights with a ranking model trained on labelled queries.

### 4. Advanced Temporal Search

Support expressions such as:

```text
last Friday
two weeks ago
around Diwali
during the first week of May
before the trip
after Priya joined
```

### 5. Topic Extraction

Automatically identify topics:

```text
Trip
Budget
College
Project
Placement
Events
Food
```

### 6. Conversation Summaries

Add a summary mode:

```text
Query:
"What happened with the Manali trip?"

Summary:
The group selected Manali, agreed on Friday evening departure,
and finalized the tickets.
```

### 7. Production Vector Database

For larger datasets, FAISS could be replaced or complemented by:

```text
Qdrant
Pinecone
Weaviate
pgvector
```

### 8. Real Chat Import

Future versions could support exported conversations from:

```text
WhatsApp
Telegram
Slack
Discord
```

Private conversations should never be committed to the public repository.

### 9. Multilingual Expansion

Improve support for:

```text
English
Hindi
Hinglish
Tamil
Bengali
Telugu
and other multilingual conversations
```

---
