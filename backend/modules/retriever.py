# modules/retriever.py
import os
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
from sentence_transformers import SentenceTransformer
from typing import List, Dict
import hashlib

class LegalRetriever:
    def __init__(self):
        # Initialize embedding model
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.dim = 384

        # Initialize Qdrant (cloud or local)
        qdrant_url = os.getenv("QDRANT_URL")
        qdrant_api_key = os.getenv("QDRANT_API_KEY")

        if qdrant_url:
            self.client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)
        else:
            # Fallback to in-memory/local (for Render free tier)
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
            vector = self.model.encode(doc["text"]).tolist()
            points.append(PointStruct(
                id=i,
                vector=vector,
                payload=doc
            ))
        self.client.upsert(collection_name=self.collection_name, points=points)

    def search_legal_references(self, query: str, top_k: int = 1) -> List[Dict]:
        try:
            vector = self.model.encode(query).tolist()
            hits = self.client.search(
                collection_name=self.collection_name,
                query_vector=vector,
                limit=top_k
            )
            return [hit.payload for hit in hits]
        except Exception as e:
            print(f"Retrieval error: {e}")
            return []