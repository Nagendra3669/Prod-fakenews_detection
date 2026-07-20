import os
from pinecone import Pinecone
from dotenv import load_dotenv

load_dotenv()

class DatabaseManager:
    def __init__(self):
        # 1. Connect to Pinecone using API Key
        self.pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        
        # 2. Connect to the specific index using your HOST URL
        # This is faster than connecting by name in production
        self.index = self.pc.Index(host=os.getenv("PINECONE_INDEX_HOST"))

    def check_connection(self):
        try:
            stats = self.index.describe_index_stats()
            return {"status": "connected", "vector_count": stats['total_vector_count']}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def search_fact(self, vector):
        """Search the cloud database for a matching fact."""
        return self.index.query(vector=vector, top_k=1, include_metadata=True)