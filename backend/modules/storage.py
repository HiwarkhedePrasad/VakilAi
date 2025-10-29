# modules/storage.py
import os
from supabase import create_client, Client
from typing import Dict, Any

class StorageManager:
    def __init__(self):
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_ANON_KEY")
        if url and key:
            self.supabase: Client = create_client(url, key)
            self.enabled = True
        else:
            self.enabled = False
            print("⚠️ Supabase not configured. Results will not persist.")

    def save_analysis(self, job_id: str, result: Dict[Any, Any]) -> bool:
        if not self.enabled:
            return False
        try:
            self.supabase.table("analyses").upsert({
                "job_id": job_id,
                "result": result,
                "created_at": result["analyzed_at"]
            }).execute()
            return True
        except Exception as e:
            print(f"Supabase save error: {e}")
            return False

    def get_analysis(self, job_id: str) -> Dict[Any, Any]:
        if not self.enabled:
            return {}
        try:
            response = self.supabase.table("analyses").select("result").eq("job_id", job_id).single().execute()
            return response.data.get("result", {}) if response.data else {}
        except Exception:
            return {}