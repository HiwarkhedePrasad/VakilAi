import os
import hashlib
from typing import List, Dict
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
import requests

class LegalRetriever:
    def __init__(self):
        # Gemini API key and model
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        self.gemini_embed_url = "https://generativelanguage.googleapis.com/v1beta/models/embedding-001:embedText"
        self.dim = 768  # Gemini embedding dimension

        # Initialize Qdrant (cloud or local)
        qdrant_url = os.getenv("QDRANT_URL")
        qdrant_api_key = os.getenv("QDRANT_API_KEY")

        if qdrant_url:
            self.client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)
        else:
            self.client = QdrantClient(":memory:")

        self.collection_name = "indian_legal_acts"

        # Create collection if not exists
        try:
            self.client.get_collection(self.collection_name)
        except:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=self.dim, distance=Distance.COSINE)
            )
            self._seed_legal_database()

    def _get_embedding(self, text: str):
        """Fetch text embedding from Gemini API"""
        try:
            response = requests.post(
                f"{self.gemini_embed_url}?key={self.gemini_api_key}",
                json={"text": text},
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            return data["embedding"]["values"]
        except Exception as e:
            print(f"Embedding error: {e}")
            return [0.0] * self.dim  # fallback zero vector

    def _seed_legal_database(self):
        """Seed with sample Indian legal acts (expandable)"""
        legal_corpus = [
            {
                "text": "Compensation for breach of contract: When a contract is broken, the party who suffers by such breach is entitled to receive compensation for any loss or damage caused.",
                "act": "Indian Contract Act, 1872",
                "section": "73",
                "url": "https://www.indiacode.nic.in/handle/123456789/2187"
            },
            {
                "text": "Agreement without consideration is void, unless in writing and registered, or is a promise to compensate for something done.",
                "act": "Indian Contract Act, 1872",
                "section": "25",
                "url": "https://www.indiacode.nic.in/handle/123456789/2187"
            },
            {
                "text": "Every person is competent to contract who is of the age of majority and of sound mind.",
                "act": "Indian Contract Act, 1872",
                "section": "11",
                "url": "https://www.indiacode.nic.in/handle/123456789/2187"
            }
        ]

        points = []
        for i, doc in enumerate(legal_corpus):
            vector = self._get_embedding(doc["text"])
            points.append(PointStruct(id=i, vector=vector, payload=doc))
        self.client.upsert(collection_name=self.collection_name, points=points)

    def search_legal_references(self, query: str, top_k: int = 1) -> List[Dict]:
        try:
            vector = self._get_embedding(query)
            hits = self.client.search(
                collection_name=self.collection_name,
                query_vector=vector,
                limit=top_k
            )
            return [hit.payload for hit in hits]
        except Exception as e:
            print(f"Retrieval error: {e}")
            return []
