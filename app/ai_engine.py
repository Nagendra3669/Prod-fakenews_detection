import os
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from dotenv import load_dotenv

load_dotenv()

class FakeNewsEngine:
    def __init__(self):
        # Use the names from your .env
        short_id = os.getenv("SHORT_MODEL_NAME")
        
        try:
            print(f"🔄 Loading AI Model: {short_id}...")
            # We add token=False to tell Hugging Face we are accessing a PUBLIC model
            self.tokenizer = AutoTokenizer.from_pretrained(short_id, token=False)
            self.model = AutoModelForSequenceClassification.from_pretrained(short_id, token=False)
            print("✅ AI Engine Ready.")
        except Exception as e:
            print(f"❌ Error loading model {short_id}: {e}")
            # Fallback to a guaranteed public model if the one in .env fails
            print("🔄 Attempting fallback to bert-base-uncased...")
            self.tokenizer = AutoTokenizer.from_pretrained("google-bert/bert-base-uncased")
            self.model = AutoModelForSequenceClassification.from_pretrained("google-bert/bert-base-uncased")