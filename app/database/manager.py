import os
from pinecone import Pinecone
from dotenv import load_dotenv

load_dotenv()

class DatabaseManager:
    def __init__(self):
        self.pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        self.index = self.pc.Index(host=os.getenv("PINECONE_INDEX_HOST"))

    def save_news(self, news_id, vector, text, label, source):
        """Saves everything into Pinecone metadata."""
        self.index.upsert(
            vectors=[{
                "id": news_id,
                "values": vector,
                "metadata": {
                    "text": text[:500], # Store first 500 chars for reference
                    "label": label,     # e.g., "Real" or "Fake"
                    "source": source,   # The URL
                    "date_added": "2026-01-21"
                }
            }]
        )

    def search_news(self, vector):
        """Searches for similar news and returns the metadata."""
        results = self.index.query(
            vector=vector, 
            top_k=1, 
            include_metadata=True
        )
        return results['matches']