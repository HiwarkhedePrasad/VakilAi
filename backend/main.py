# main.py
import os
import tempfile
import hashlib
from datetime import datetime
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from modules.legal_agent import build_legal_agent
from modules.storage import StorageManager
import uvicorn 

app = FastAPI(title="MyLawyer AI - LangGraph Agent")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

storage = StorageManager()
agent = build_legal_agent()

@app.post("/analyze")
async def analyze_contract(file: UploadFile = File(...)):
    # Validate file
    if file.content_type not in ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "text/plain"]:
        raise HTTPException(400, "Only PDF, DOCX, TXT allowed")

    # Save to temp file
    job_id = hashlib.md5(f"{file.filename}{datetime.utcnow().isoformat()}".encode()).hexdigest()
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    # Initialize state
    initial_state = {
        "job_id": job_id,
        "file_name": file.filename,
        "file_path": tmp_path,
        "raw_text": "",
        "clauses": [],
        "status": "uploaded",
        "error": None
    }

    # Run LangGraph agent
    try:
        result = agent.invoke(initial_state)
    except Exception as e:
        raise HTTPException(500, f"Agent failed: {str(e)}")

    if result["status"] == "failed":
        raise HTTPException(500, result["error"])

    # Format final output
    output = {
        "job_id": job_id,
        "contract_name": file.filename,
        "analyzed_at": datetime.utcnow().isoformat(),
        "clauses": result["clauses"]
    }

    # Save to Supabase (if configured)
    storage.save_analysis(job_id, output)

    return {"success": True, "result": output}

if __name__ == "__main__":
    # Read port from environment (Render sets PORT automatically)
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)