

# 🧑‍⚖️ MyLawyer AI – Legal Document Analyzer

> **AI-powered backend that reviews contracts, flags risky clauses, suggests user-friendly edits, and cites Indian legal references — all using free-tier services.**

Built with **LangGraph**, **FastAPI**, **Google Gemini**, **Qdrant**, and **Supabase**.  
✅ **100% deployable on free tiers** (Render, Railway, etc.)  
✅ No frontend — pure REST API  
✅ Production-ready & modular

---

## 🚀 Features

- 📄 **Upload** PDF, DOCX, or TXT legal documents
- 🔍 **Parse** into individual clauses
- ⚖️ **Analyze risk** per clause using **Google Gemini**
- 💡 **Suggest user-favorable rewrites**
- 📚 **Link to real Indian legal acts** (e.g., Indian Contract Act, 1872)
- 🧠 **LangGraph-based agent** for stateful, modular reasoning
- ☁️ **Persistent storage** via Supabase (optional)
- 🧪 **Vector search** via Qdrant (free cloud or in-memory fallback)

---

## 🛠️ Tech Stack

| Component       | Technology |
|-----------------|------------|
| **Backend**     | FastAPI |
| **AI Agent**    | LangGraph |
| **LLM**         | Google Gemini (`gemini-2.5-flash`) |
| **Embeddings**  | `all-MiniLM-L6-v2` (Sentence Transformers) |
| **Vector DB**   | Qdrant (Cloud or in-memory) |
| **Database**    | Supabase (PostgreSQL) |
| **Deployment**  | Render / Railway / Fly.io (free tier compatible) |

---

## 📦 Quick Start (Local)

### 1. Clone & Install
```bash
git clone https://github.com/your-username/mylawyer-ai.git
cd mylawyer-ai
pip install -r requirements.txt
```

### 2. Set Up Environment
```bash
cp .env.example .env
```

Edit `.env`:
```env
GEMINI_API_KEY=your_gemini_api_key_here
# Optional:
# SUPABASE_URL=...
# SUPABASE_ANON_KEY=...
# QDRANT_URL=...
# QDRANT_API_KEY=...
```

> 🔑 Get your **Gemini API key** at: [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)

### 3. Run Locally
```bash
uvicorn main:app --reload --port 8000
```

### 4. Test the API
Upload a contract:
```bash
curl -X POST http://localhost:8000/analyze \
  -F "file=@sample_contract.pdf"
```

---

## 🌐 Deployment (Render.com – Recommended)

1. Push code to a **GitHub repo**
2. Go to [https://render.com](https://render.com) → **New Web Service**
3. Connect your repo
4. Set **Build Command**: `pip install -r requirements.txt`
5. Set **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Add environment variables:
   - `GEMINI_API_KEY` (required)
   - `SUPABASE_URL`, `SUPABASE_ANON_KEY` (optional)
   - `QDRANT_URL`, `QDRANT_API_KEY` (optional)
7. Click **Create Web Service** ✅

> 💡 Render free tier sleeps after 15 mins of inactivity — perfect for demos!

---

## 📤 API Endpoints

### `POST /analyze`
Upload and analyze a legal document.

**Request**
- `file`: PDF, DOCX, or TXT (max ~10MB)

**Response**
```json
{
  "success": true,
  "result": {
    "job_id": "a1b2c3...",
    "contract_name": "nda.docx",
    "analyzed_at": "2025-10-30T12:00:00Z",
    "clauses": [
      {
        "id": 1,
        "text": "Either party may terminate without notice.",
        "risk": "high",
        "suggestion": "Change to: 'Either party may terminate with 30 days written notice.'",
        "legal_reference": {
          "act": "Indian Contract Act, 1872",
          "section": "73",
          "url": "https://www.indiacode.nic.in/handle/123456789/2187"
        }
      }
    ]
  }
}
```

---

## 🗃️ Optional Services

| Service | Benefit | Free Tier? |
|--------|--------|-----------|
| **Supabase** | Save analysis results permanently | ✅ 500MB |
| **Qdrant Cloud** | Faster legal reference retrieval | ✅ 512MB |
| **Gemini** | AI analysis & advice | ✅ 60 RPM, 1M tokens/day |

> If you skip Supabase/Qdrant, the app **still works** using in-memory fallbacks.

---

## 📁 Project Structure

```
mylawyer-ai/
├── main.py                 # FastAPI app + LangGraph integration
├── modules/
│   ├── ingestion.py        # PDF/DOCX/TXT parsing
│   ├── retriever.py        # Legal reference lookup (Qdrant)
│   ├── analyzer.py         # Risk analysis (Gemini)
│   ├── advisor.py          # User-friendly suggestions
│   ├── storage.py          # Supabase persistence
│   ├── state.py            # LangGraph state schema
│   ├── agent_nodes.py      # LangGraph node logic
│   └── legal_agent.py      # LangGraph workflow builder
├── requirements.txt
├── .env.example
└── README.md
```

---

## 📜 License

MIT License — feel free to use, modify, and deploy!

---

## 🙌 Need Help?

- [Gemini API Setup](https://aistudio.google.com/app/apikey)
- [Supabase Project Setup](https://supabase.com)
- [Qdrant Cloud](https://qdrant.tech)

> Built for **Indian legal context** — easily extendable to other jurisdictions.

---

