import os
import torch
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Fake News Detection API")

# Load AI Model (mrm8488/bert-tiny-finetuned-fake-news-detection)
MODEL_ID = os.getenv("SHORT_MODEL_NAME", "mrm8488/bert-tiny-finetuned-fake-news-detection")

try:
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_ID)
    print("✅ AI Model Loaded Successfully")
except Exception as e:
    print(f"❌ Error loading model: {e}")

class NewsRequest(BaseModel):
    text: str

@app.post("/analyze")
async def analyze_news(request: NewsRequest):
    if not request.text:
        raise HTTPException(status_code=400, detail="Text is required")
    
    # Tokenize and Predict
    inputs = tokenizer(request.text, return_tensors="pt", truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
        probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
        confidence, prediction = torch.max(probs, dim=-1)
    
    # Map result (0 = Fake, 1 = Real - Verify based on your specific model)
    label = "Real" if prediction.item() == 1 else "Fake"
    
    return {
        "label": label,
        "confidence": float(confidence.item()),
        "status": "success"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)